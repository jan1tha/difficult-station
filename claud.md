# Project: Redda — Difficult Station Vacancy Selector

## Purpose
Personal tool to identify and prioritise **difficult/remote medical officer posting vacancies** in Sri Lanka that are currently available, sorted by estimated travel time from Homagama Hospital.

## Source Data (`Source/`)
| File | Rows | Columns | Description |
|---|---|---|---|
| `Difficult Station List.csv` | 320 | SN, PROVINCE, RDHS, STATION | Master list of all officially designated difficult stations |
| `Vacancy List.csv` | 427 | INDEX, DISTRICT, INSTITUTE, DESIGNATION, VACANCIES | Current transfer circular vacancies |

`PDF537_vac.csv` — working copy of vacancy list used by `reverify_matches.py`  
`Available list.csv` — working copy of difficult station list used by `reverify_matches.py`

## Output Files
| File | Rows | Description |
|---|---|---|
| `AVAILABLE_DIFFICULT_STATIONS.csv` | 82 | Intersection: vacancies that are at difficult stations |
| `DIFFICULT_STATIONS_BY_ETA.csv` | 82 | Same, sorted by ETA from Homagama Hospital |
| `markers.js` | — | JS array `markersData` with lat/lon/eta for Leaflet map |
| `index.html` | — | Password-protected Leaflet map of stations |

## Scripts
### `reverify_matches.py`
- Reads `Available list.csv` (difficult stations) + `PDF537_vac.csv` (vacancies)
- Matches by exact name, substring, then fuzzy (ratio > 0.75)
- Outputs `AVAILABLE_DIFFICULT_STATIONS.csv`
- Also prints potential fuzzy matches for manual review

### `generate_files.py`
- Reads `AVAILABLE_DIFFICULT_STATIONS.csv`
- Annotates each row with ETA (hours by road from Homagama/Kottawa) and lat/lon coordinates
- Sorts by ETA ascending
- Outputs:
  - `DIFFICULT_STATIONS_BY_ETA.csv`
  - `markers.js`
  - `index.html` (password: `redda2026`, SHA-256 protected)

## Map (`index.html`)
- Leaflet map, centered on Sri Lanka
- Password: `redda2026`
- Colour coding by ETA from Homagama Hospital:
  - 🟢 Green: < 3 hrs
  - 🟠 Orange: 3–5 hrs
  - 🔴 Red: > 5 hrs
- Popup shows: station name, district, designation, vacancies, ETA

## Key Domain Notes
- **RDHS** = Regional Director of Health Services (used as district in difficult station list)
- **KALMUNAI** appears as separate district from AMPARA in vacancy list
- ETA is by road from **Homagama Hospital, Sri Lanka** — routes:
  - E01 Southern Expressway (from Kottawa): Kalutara, Galle, Matara, Hambantota
  - A4 road (via Avissawella): Ratnapura hills
  - E03 Central Expressway (from Kadawatha): Kandy, Matale, Kurunegala, Anuradhapura
  - A9 north (via Anuradhapura/Vavuniya): Mannar, Mullaitivu, Kilinochchi, Jaffna
  - Via Kandy + Mahiyanganaya: Ampara, Batticaloa, east coast
- Station names have OCR noise (`|`, `_`, `[`, `]`) — normalised in scripts
- `ISENARATHPURA DH` is an OCR variant of `SENARATHPURA DH` (same coords)
- `IRAKKAMAM ERAGAMA DH` and `IRAKKAMAM DH` are same location
- `NADDANKANDAL DH` and `NANDANKANNDAL DH` are same station (OCR variant)
- `KILIVETTY OH` is OCR misread of `KILIVETTY DH`
- `POONAKERY POONARYN DH` = full name; eta_data must include exact string (substring match fails)
- `ANALATIVU DH` (Jaffna islands) requires ferry from Jaffna — +1.0h overhead applied
- `KAYTS BH` is on Kayts island near Jaffna (causeway/short boat) — ETA 7.0h

## Workflow to Regenerate
```bash
python reverify_matches.py   # regenerate AVAILABLE_DIFFICULT_STATIONS.csv
python generate_files.py     # regenerate ETA CSV + map files
```
