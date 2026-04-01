#!/usr/bin/env python3
"""
update_etas.py  —  Recalculate ETAs in generate_files.py using OSRM (free, no API key).

Uses the public OSRM routing server (router.project-osrm.org) powered by OpenStreetMap.
No traffic data — pure road-speed estimates. No API key required.

Note: OSRM cannot route to ferry-only destinations (ANALATIVU DH, KAYTS BH);
those are skipped and their existing manual ETAs are preserved.

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

# Ferry/island destinations — OSRM cannot route these; keep manual ETAs
SKIP_API = {"ANALATIVU DH", "KAYTS BH"}

OSRM_BASE   = "http://router.project-osrm.org/table/v1/driving"
BATCH_SIZE  = 50   # keep requests small to respect the public server
RATE_PAUSE  = 0.5  # seconds between batches


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
    Query OSRM table API for drive times (seconds) from the origin to each destination.
    Coordinates are lon,lat for OSRM. Returns list of durations in seconds (None on failure).
    """
    # Build coordinate string: origin first, then destinations (lon,lat order)
    all_coords = [(ORIGIN_LON, ORIGIN_LAT)] + [(lon, lat) for lat, lon in destinations]
    coord_str  = ";".join(f"{lon},{lat}" for lon, lat in all_coords)
    url = f"{OSRM_BASE}/{coord_str}?sources=0&annotations=duration"

    with urllib.request.urlopen(url, timeout=30) as resp:
        data = json.loads(resp.read().decode())

    if data.get("code") != "Ok":
        raise RuntimeError(f"OSRM error: {data.get('code')} — {data.get('message', '')}")

    # durations[0] = row for source 0; index 0 is origin→origin (0), rest are origin→dest
    row = data["durations"][0]
    return [row[i + 1] for i in range(len(destinations))]  # skip index 0 (self)


def main():
    parser = argparse.ArgumentParser(
        description="Update ETAs in generate_files.py via OSRM (free, no API key)"
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
    print(f"Router: OSRM public server (OpenStreetMap, no traffic data)\n")

    # Deduplicate: one API call per unique name (aliases share coords)
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

    # ── Batch OSRM calls ─────────────────────────────────────────────────────
    new_etas: dict[str, float] = {}
    failed:   list[str]        = []

    total_batches = (len(to_query) + BATCH_SIZE - 1) // BATCH_SIZE
    for batch_idx in range(0, len(to_query), BATCH_SIZE):
        batch     = to_query[batch_idx: batch_idx + BATCH_SIZE]
        names     = [n for n, _ in batch]
        dest_coords = [c for _, c in batch]
        batch_num = batch_idx // BATCH_SIZE + 1

        print(f"Batch {batch_num}/{total_batches}  ({len(batch)} destinations)...")
        try:
            durations = query_osrm_batch(dest_coords)
            for name, secs in zip(names, durations):
                if secs is None:
                    print(f"  ✗  {name}: no route found (keeping existing)")
                    failed.append(name)
                else:
                    hours = round(secs / 3600, 1)
                    new_etas[name] = hours
                    print(f"  ✓  {name}: {hours} h")
        except Exception as exc:
            print(f"  ERROR: {exc}")
            failed.extend(names)

        if batch_idx + BATCH_SIZE < len(to_query):
            time.sleep(RATE_PAUSE)

    print(f"\nOSRM results: {len(new_etas)} updated, {len(failed)} failed/kept.")

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
        # Match: ("NAME", "DISTRICT", old_hours)  — district may vary for aliases
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

    print(f"Updated {replaced} entries in generate_files.py")
    print("Run:  python3 generate_files.py   to regenerate CSV/markers.js/index.html")


if __name__ == "__main__":
    main()
