# Redda — Difficult Station Vacancy Selector

A personal tool to find available **difficult/remote medical officer vacancies** in Sri Lanka from the current transfer circular, ranked by travel time from Homagama Hospital.

## How It Works

1. **Source PDFs** (converted to CSV in `Source/`) are cross-referenced:
   - `Difficult Station List.csv` — all officially designated difficult stations
   - `Vacancy List.csv` — current transfer circular vacancies

2. **`reverify_matches.py`** finds the intersection (vacancies that are at difficult stations) → `AVAILABLE_DIFFICULT_STATIONS.csv`

3. **`generate_files.py`** adds ETA from Homagama Hospital and GPS coordinates, then outputs:
   - `DIFFICULT_STATIONS_BY_ETA.csv` — stations sorted nearest to farthest
   - `index.html` — interactive map

## Viewing the Map

Open `index.html` in a browser.  
Password: `redda2026`

### Map Legend
| Colour | ETA from Homagama |
|--------|------------------|
| 🟢 Green | < 3 hours |
| 🟠 Orange | 3–5 hours |
| 🔴 Red | > 5 hours |

## Regenerating Files

If source CSVs are updated, run scripts in order:

```bash
python reverify_matches.py   # step 1: find matches → AVAILABLE_DIFFICULT_STATIONS.csv
python generate_files.py     # step 2: add ETA + coords → CSV + map files
```

## File Structure

```
Redda/
├── Source/
│   ├── Difficult Station List.csv   # master difficult stations (320 stations)
│   └── Vacancy List.csv             # current circular vacancies (427 rows)
├── PDF537_vac.csv                   # working copy of vacancy list
├── Available list.csv               # working copy of difficult station list
├── AVAILABLE_DIFFICULT_STATIONS.csv # intersection result (79 stations)
├── DIFFICULT_STATIONS_BY_ETA.csv    # sorted by ETA from Homagama
├── markers.js                       # map marker data (auto-generated)
├── index.html                       # interactive map (auto-generated)
├── reverify_matches.py              # step 1 script
├── generate_files.py                # step 2 script
└── images/
```
