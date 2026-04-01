#!/usr/bin/env python3
"""
update_etas.py  —  Recalculate ETAs using both OSRM and Valhalla, average the two.

OSRM:     router.project-osrm.org  (free, no key, fast batch table API)
Valhalla: valhalla1.openstreetmap.de  (free, no key, more realistic speeds)

Both use OpenStreetMap data but different speed models. Averaging the two gives
a better real-world estimate than either alone.

Ferry/island destinations (ANALATIVU DH, KAYTS BH) are skipped and their
existing manual ETAs are preserved.

Usage:
    python3 update_etas.py
    python3 update_etas.py --dry-run

Options:
    --dry-run   Print results but do not modify generate_files.py
"""

import re
import sys
import os
import json
import time
import argparse
import urllib.request

# ── Origin: Homagama Hospital ───────────────────────────────────────────────
ORIGIN_LAT = 6.8614
ORIGIN_LON  = 80.0022

# Ferry/island destinations — cannot be road-routed; keep manual ETAs
SKIP_API = {"ANALATIVU DH", "KAYTS BH"}

OSRM_BASE      = "http://router.project-osrm.org/table/v1/driving"
VALHALLA_BASE  = "https://valhalla1.openstreetmap.de/route"
BATCH_SIZE     = 50   # for OSRM batch table; Valhalla is called one-by-one
RATE_PAUSE     = 0.3  # seconds between requests


def parse_section(code: str, start_marker: str, end_char: str) -> str:
    """Return the text of a bracketed section starting at start_marker."""
    idx = code.index(start_marker)
    depth = 0
    for i, ch in enumerate(code[idx:], idx):
        if ch in "([{":
            depth += 1
        elif ch in ")]}":
            depth -= 1
            if depth == 0:
                return code[idx: i + 1]
    raise ValueError(f"Unmatched bracket in section starting with '{start_marker}'")


def parse_eta_data(code: str) -> list[tuple[str, str, float]]:
    """Extract [(name, district, hours), ...] from eta_data block."""
    block = parse_section(code, "eta_data = [", "]")
    pattern = re.compile(r'\("([^"]+)",\s*"([^"]+)",\s*([\d.]+)\)')
    return [(name, district, float(h)) for name, district, h in pattern.findall(block)]


def parse_coords(code: str) -> dict[str, tuple[float, float]]:
    """Extract {name: (lat, lon)} from coords block."""
    block = parse_section(code, "coords = {", "}")
    pattern = re.compile(r'"([^"]+)":\s*\(([\d.]+),\s*([\d.]+)\)')
    return {name: (float(lat), float(lon)) for name, lat, lon in pattern.findall(block)}


def query_osrm_batch(destinations: list[tuple[float, float]]) -> list[float | None]:
    """
    Query OSRM table API for drive times (seconds) from origin to each destination.
    Coordinates are lon,lat for OSRM. Returns durations in seconds (None on failure).
    """
    all_coords = [(ORIGIN_LON, ORIGIN_LAT)] + [(lon, lat) for lat, lon in destinations]
    coord_str  = ";".join(f"{lon},{lat}" for lon, lat in all_coords)
    url = f"{OSRM_BASE}/{coord_str}?sources=0&annotations=duration"

    with urllib.request.urlopen(url, timeout=30) as resp:
        data = json.loads(resp.read().decode())

    if data.get("code") != "Ok":
        raise RuntimeError(f"OSRM error: {data.get('code')} — {data.get('message', '')}")

    row = data["durations"][0]
    return [row[i + 1] for i in range(len(destinations))]


def query_valhalla(dest_lat: float, dest_lon: float) -> float | None:
    """
    Query Valhalla for drive time (seconds) from origin to one destination.
    Returns seconds, or None on failure.
    """
    payload = json.dumps({
        "locations": [
            {"lon": ORIGIN_LON, "lat": ORIGIN_LAT},
            {"lon": dest_lon,   "lat": dest_lat},
        ],
        "costing": "auto",
    }).encode()
    req = urllib.request.Request(
        VALHALLA_BASE,
        data=payload,
        headers={"Content-Type": "application/json", "Accept": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode())
    return data["trip"]["summary"]["time"]  # seconds


def main():
    parser = argparse.ArgumentParser(
        description="Update ETAs in generate_files.py via OSRM + Valhalla (free, no API key)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print results without modifying generate_files.py",
    )
    args = parser.parse_args()

    script_dir  = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(script_dir, "generate_files.py")

    with open(script_path, "r") as f:
        code = f.read()

    eta_entries = parse_eta_data(code)
    coords_map  = parse_coords(code)

    print(f"Origin: Homagama Hospital ({ORIGIN_LAT}, {ORIGIN_LON})")
    print(f"Routers: OSRM (batch) + Valhalla (per-institute) — averaged\n")

    # Deduplicate: one API call per unique name
    seen: set[str] = set()
    to_query: list[tuple[str, tuple[float, float]]] = []
    skipped_no_coords: list[str] = []
    skipped_ferry: list[str] = []

    for name, _, _ in eta_entries:
        if name in seen:
            continue
        seen.add(name)
        if name in SKIP_API:
            skipped_ferry.append(name)
            continue
        if name in coords_map:
            to_query.append((name, coords_map[name]))
        else:
            skipped_no_coords.append(name)

    print(f"Institutes to query:  {len(to_query)}")
    if skipped_ferry:
        print(f"Skipped (ferry/island — manual ETA kept): {', '.join(skipped_ferry)}")
    if skipped_no_coords:
        print(f"Skipped (no coords):  {', '.join(skipped_no_coords)}")
    print()

    # ── Phase 1: OSRM batch calls ────────────────────────────────────────────
    osrm_results: dict[str, float] = {}   # name → seconds
    print("=== Phase 1: OSRM ===")
    total_batches = (len(to_query) + BATCH_SIZE - 1) // BATCH_SIZE
    for batch_idx in range(0, len(to_query), BATCH_SIZE):
        batch       = to_query[batch_idx: batch_idx + BATCH_SIZE]
        names       = [n for n, _ in batch]
        dest_coords = [c for _, c in batch]
        batch_num   = batch_idx // BATCH_SIZE + 1

        print(f"  Batch {batch_num}/{total_batches}  ({len(batch)} destinations)...", end=" ", flush=True)
        try:
            durations = query_osrm_batch(dest_coords)
            ok = 0
            for name, secs in zip(names, durations):
                if secs is not None:
                    osrm_results[name] = secs
                    ok += 1
            print(f"{ok} ok")
        except Exception as exc:
            print(f"ERROR: {exc}")

        if batch_idx + BATCH_SIZE < len(to_query):
            time.sleep(RATE_PAUSE)

    print(f"  OSRM: {len(osrm_results)}/{len(to_query)} succeeded\n")

    # ── Phase 2: Valhalla one-by-one ─────────────────────────────────────────
    valhalla_results: dict[str, float] = {}   # name → seconds
    print("=== Phase 2: Valhalla ===")
    for i, (name, (lat, lon)) in enumerate(to_query, 1):
        print(f"  [{i}/{len(to_query)}] {name}...", end=" ", flush=True)
        try:
            secs = query_valhalla(lat, lon)
            valhalla_results[name] = secs
            print(f"{secs/3600:.2f} h")
        except Exception as exc:
            print(f"FAILED ({exc})")
        time.sleep(RATE_PAUSE)

    print(f"  Valhalla: {len(valhalla_results)}/{len(to_query)} succeeded\n")

    # ── Phase 3: Average OSRM + Valhalla ────────────────────────────────────
    print("=== Results (averaged) ===")
    new_etas: dict[str, float] = {}
    failed:   list[str]        = []

    for name, _ in to_query:
        osrm_s  = osrm_results.get(name)
        val_s   = valhalla_results.get(name)

        if osrm_s is not None and val_s is not None:
            avg_hours = round((osrm_s + val_s) / 2 / 3600, 1)
            new_etas[name] = avg_hours
            print(f"  {name}: OSRM={osrm_s/3600:.2f}h  Valhalla={val_s/3600:.2f}h  → avg={avg_hours}h")
        elif osrm_s is not None:
            hours = round(osrm_s / 3600, 1)
            new_etas[name] = hours
            print(f"  {name}: OSRM only → {hours}h  (Valhalla failed)")
        elif val_s is not None:
            hours = round(val_s / 3600, 1)
            new_etas[name] = hours
            print(f"  {name}: Valhalla only → {hours}h  (OSRM failed)")
        else:
            print(f"  {name}: BOTH FAILED — keeping existing ETA")
            failed.append(name)

    print(f"\nSummary: {len(new_etas)} updated, {len(failed)} kept (both routers failed).")

    if args.dry_run:
        print("[dry-run] generate_files.py NOT modified.")
        return

    if not new_etas:
        print("No new ETAs to write. generate_files.py unchanged.")
        return

    # ── Update eta_data in generate_files.py ────────────────────────────────
    updated_code = code
    replaced = 0
    for name, new_hours in new_etas.items():
        pat = re.compile(
            r'(\("' + re.escape(name) + r'",\s*"[^"]+",\s*)[\d.]+(\))'
        )
        new_code, n = pat.subn(
            lambda m, h=new_hours: f"{m.group(1)}{h}{m.group(2)}",
            updated_code,
        )
        if n:
            updated_code = new_code
            replaced += n

    with open(script_path, "w") as f:
        f.write(updated_code)

    print(f"\nUpdated {replaced} entries in generate_files.py")
    print("Run:  python3 generate_files.py   to regenerate CSV/markers.js/index.html")



if __name__ == "__main__":
    main()
