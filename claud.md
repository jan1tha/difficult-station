# Project: Redda — Medical Vacancy Map

## Purpose
Personal tool to browse all current Sri Lanka medical officer transfer circular vacancies on an interactive map, with filters and ETA from Homagama Hospital. Difficult stations are highlighted.

## Current State (commit 4ab4e90, 20 March 2026)
- **428 total vacancies** from `Source/Vacancy List.csv`
- **82 are difficult stations** (in `AVAILABLE_DIFFICULT_STATIONS.csv`)
- All 428 plotted on map with coords + ETAs
- Password: `redda2026` (SHA-256 protected)

## Source Data (`Source/`)
| File | Rows | Description |
|---|---|---|
| `Vacancy List.csv` | 428 | Transfer circular — INDEX, DISTRICT, INSTITUTE, DESIGNATION, VACANCIES |
| `Difficult Station List.csv` | 320 | Master list of officially designated difficult stations |

`PDF537_vac.csv` / `Available list.csv` — working copies used by `reverify_matches.py`

## Output Files
| File | Rows | Description |
|---|---|---|
| `ALL_STATIONS_BY_ETA.csv` | 428 | All vacancies sorted by ETA — includes IS_DIFFICULT, IS_DH, DESIG_GROUP |
| `AVAILABLE_DIFFICULT_STATIONS.csv` | 82 | Vacancies at difficult stations |
| `DIFFICULT_STATIONS_BY_ETA.csv` | 82 | Difficult stations sorted by ETA |
| `NON_DIFFICULT_STATIONS.csv` | 346 | Non-difficult vacancies |
| `markers.js` | — | JS array `markersData` — all 428 markers with lat/lon/eta/is_difficult/is_dh/desig_group |
| `index.html` | — | Password-protected Leaflet map |

## Scripts

### `reverify_matches.py`
- Exact → substring → fuzzy (ratio > 0.75) matching of vacancy list vs difficult station list
- Outputs `AVAILABLE_DIFFICULT_STATIONS.csv`

### `generate_files.py` (master generator, ~872 lines)
Key internals:
- `eta_data` — list of `(NAME, DISTRICT, hours)` for ~250 institutes
- `coords` — dict `NAME: (lat, lon)` for all 428 institutes
- `lookup_eta(name, district)` — exact match → substring → district fallback dict
- `lookup_coords(name)` — exact match → substring fallback
- `normalize_designation(raw)` — raw string → grouped label (e.g. "MO Surgery", "SHO Paediatrics")
- `is_dh(institute)` — True if name ends with " DH"
- `create_files()` — reads all 428 vacancies, computes ETA + coords, writes all outputs

**Regenerate:**
```bash
cd /Users/janitha/Documents/Personal/Redda
python3 reverify_matches.py   # only if vacancy list changed
python3 generate_files.py     # always run after any change
git add -A && git commit -m "..." && git push
```

## Map (`index.html`)
- Leaflet 1.7.1, OpenStreetMap, centred on Sri Lanka (7.87, 80.77), zoom 7
- Password: `redda2026`
- **4 Filters** (top-right collapsible panel): Station Type / Facility Type / Designation / District
- **Visual encoding:**
  - Fill: Difficult = fillOpacity 0.75 (solid filled), Standard = fillOpacity 0.2 (hollow)
  - Size: DH = radius 9, Non-DH = radius 7
  - Border: DH = solid, Non-DH = dashed (`dashArray: "4 3"`)
  - Colour by ETA: Green < 3h, Orange 3–5h, Red > 5h
- Popup: name + DIFFICULT/STANDARD badge + DH badge, district, designation, desig_group, vacancies, ETA

## ETA Routes (from Homagama Hospital, 6.8614N 80.0022E)
| Corridor | Covers |
|---|---|
| E01 Southern Expressway (Kottawa) | Kalutara, Galle, Matara, Hambantota |
| A4 via Avissawella | Ratnapura, Kegalle |
| E03 Central Expressway (Kadawatha) | Kandy, Matale, Nuwara Eliya, Kurunegala |
| A9 North via Anuradhapura/Vavuniya | Anuradhapura, Mannar, Mullaitivu, Kilinochchi, Jaffna |
| Via Kandy + Mahiyanganaya | Badulla, Moneragala, Polonnaruwa, Ampara, Batticaloa |

## Known OCR Variants (both keys exist in eta_data + coords)
- `TPUTTALAM BH` = PUTTALAM BH
- `KANTALE 8H` = KANTALE BH
- `UDUGAMA 8H` = UDUGAMA BH
- `BALAPITIVA BH` = BALAPITIYA BH
- `KINNIYABH` = KINNIYA BH
- `VALAICHCHENA! BH` = VALAICHCHENAI BH
- `SAMMANTHURA! MOH` = SAMMANTHURAI MOH
- `IVAVUNIYA DGH/RDHS` = VAVUNIYA DGH
- `ISENARATHPURA DH` = SENARATHPURA DH
- `NANDANKANNDAL DH` = NADDANKANDAL DH
- `KILIVETTY OH` = KILIVETTY DH
- `BELIIATTE DH` = BELIATTE DH
- `POONAKERY POONARYN DH` — requires explicit entry in eta_data/coords (substring match fails)

## Key Domain Notes
- **KALMUNAI** is a separate district from AMPARA in the vacancy list
- `ANALATIVU DH` (Jaffna islands) — ETA 10.5h (ferry)
- `KAYTS BH` — Kayts island near Jaffna, ETA 7.0h
- `FOR WOMEN` in Galle = maternity hospital
- `HOSPITAL` in KALMUNAI = Kalmunai Base Hospital (bare name in source CSV)
- Station names stripped of OCR noise (`|`, `_`, `[`, `]`) before lookup

## Git
- Repo: https://github.com/jan1tha/difficult-station.git, branch `main`
- Last commit: `4ab4e90` — Fix password hash substitution in index.html
