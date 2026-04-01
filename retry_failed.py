#!/usr/bin/env python3
"""Retry Valhalla for the 8 stations that got HTTP 429 in the previous run."""

import re, json, time, urllib.request

ORIGIN_LAT, ORIGIN_LON = 6.8614, 80.0022
VALHALLA_BASE = "https://valhalla1.openstreetmap.de/route"
OSRM_BASE     = "http://router.project-osrm.org/table/v1/driving"
RATE_PAUSE    = 2.0   # longer delay to avoid 429 again

script_path = "generate_files.py"
with open(script_path) as f:
    code = f.read()

# Parse eta_data
eta_block = re.search(r'eta_data = \[.*?\n\]', code, re.DOTALL).group()
eta_entries = {n: float(h) for n, d, h in re.findall(r'\("([^"]+)",\s*"([^"]+)",\s*([\d.]+)\)', eta_block)}

# Parse coords
coords = {n: (float(lat), float(lon))
          for n, lat, lon in re.findall(r'"([^"]+)":\s*\(([\d.]+),\s*([\d.]+)\)', code)}

# ── Get pure OSRM values for all stations ──────────────────────────────────
SKIP = {'ANALATIVU DH', 'KAYTS BH'}
seen: set = set()
unique = []
for name in eta_entries:
    if name in seen or name in SKIP or name not in coords:
        continue
    seen.add(name)
    unique.append((name, coords[name]))

osrm_results: dict = {}
BATCH = 50
print(f"Fetching OSRM values for {len(unique)} stations...")
for i in range(0, len(unique), BATCH):
    batch = unique[i:i+BATCH]
    all_c = [(ORIGIN_LON, ORIGIN_LAT)] + [(lon, lat) for _, (lat, lon) in batch]
    coord_str = ";".join(f"{lo},{la}" for lo, la in all_c)
    url = f"{OSRM_BASE}/{coord_str}?sources=0&annotations=duration"
    with urllib.request.urlopen(url, timeout=30) as r:
        data = json.loads(r.read())
    row = data["durations"][0]
    for j, (name, _) in enumerate(batch):
        if row[j+1] is not None:
            osrm_results[name] = row[j+1] / 3600
    time.sleep(0.3)

print(f"OSRM done: {len(osrm_results)} stations\n")

# ── Identify OSRM-only stations (where current eta == round(osrm,1)) ───────
osrm_only = []
for name, (lat, lon) in unique:
    if name not in osrm_results:
        continue
    osrm_val = round(osrm_results[name], 1)
    if eta_entries[name] == osrm_val:
        osrm_only.append((name, lat, lon))

print(f"Found {len(osrm_only)} OSRM-only stations (Valhalla previously failed):")
for name, lat, lon in osrm_only:
    print(f"  {name}  ({lat}, {lon})  current={eta_entries[name]}h  osrm={osrm_results[name]:.2f}h")
print()

# ── Retry Valhalla with longer delay ───────────────────────────────────────
new_etas: dict = {}
for i, (name, lat, lon) in enumerate(osrm_only, 1):
    print(f"[{i}/{len(osrm_only)}] {name}...", end=" ", flush=True)
    try:
        payload = json.dumps({
            "locations": [{"lon": ORIGIN_LON, "lat": ORIGIN_LAT},
                          {"lon": lon,        "lat": lat}],
            "costing": "auto",
        }).encode()
        req = urllib.request.Request(
            VALHALLA_BASE, data=payload,
            headers={"Content-Type": "application/json", "Accept": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.loads(r.read())
        val_secs = data["trip"]["summary"]["time"]
        osrm_secs = osrm_results[name] * 3600
        avg = round((osrm_secs + val_secs) / 2 / 3600, 1)
        new_etas[name] = avg
        print(f"OSRM={osrm_results[name]:.2f}h  Valhalla={val_secs/3600:.2f}h  → avg={avg}h")
    except Exception as exc:
        print(f"FAILED again: {exc}")
    time.sleep(RATE_PAUSE)

print(f"\n{len(new_etas)}/{len(osrm_only)} succeeded.")

if not new_etas:
    print("Nothing to update.")
    exit(0)

# ── Update generate_files.py ───────────────────────────────────────────────
updated = code
replaced = 0
for name, hours in new_etas.items():
    pat = re.compile(r'(\("' + re.escape(name) + r'",\s*"[^"]+",\s*)[\d.]+(\))')
    new_code, n = pat.subn(lambda m, h=hours: f"{m.group(1)}{h}{m.group(2)}", updated)
    if n:
        updated = new_code
        replaced += n

with open(script_path, "w") as f:
    f.write(updated)

print(f"Updated {replaced} entries in generate_files.py")
print("Run: python3 generate_files.py")
