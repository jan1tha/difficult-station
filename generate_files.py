import csv
import json
import hashlib

# ETAs recalculated using haversine distance + corridor-based road factors
# calibrated against known reference distances from Homagama Hospital.
# Route key: E01=Southern Expressway(Kottawa), E03=Central Expressway(Kadawatha),
#             A4=Ratnapura road, A9=North road via Anuradhapura/Vavuniya
eta_data = [
    # --- KALUTARA / NEAR SOUTHWEST ---
    ("MOLKAWA PMCU", "KALUTARA", 1.6),              # via E01 Dodangoda exit + last mile
    ("YATTAPATHA PMCU", "KALUTARA", 1.8),           # hill roads, not near expressway exit
    # --- RATNAPURA CORRIDOR (A4 via Avissawella) ---
    ("NARISSA PMCU", "RATNAPURA", 1.5),             # A4, ~65km road
    ("POTHUPITIYA DH", "RATNAPURA", 2.2),           # A4 via Ratnapura + local
    ("ALUPOLA DH", "RATNAPURA", 2.5),               # A4 beyond Ratnapura into hills
    ("PALAMKOTTE DH", "RATNAPURA", 2.8),            # deep Ratnapura hills
    # --- SOUTHERN EXPRESSWAY (E01 from Kottawa) ---
    ("HALVITIGALA PMCU", "GALLE", 1.4),             # E01 Kurundugahahetekma exit + 15 km
    ("BERALIHERA PMCU", "HAMBANTOTA", 2.5),         # E01 to Hambantota + inland road
    ("DERANGALA PMCU", "MATARA", 2.3),              # E01 Godagama exit + 30 km
    ("ROTAMBA PMCU", "MATARA", 2.4),                # E01 Godagama exit + last mile
    ("LANKAGAMA PMCU", "GALLE", 2.8),               # E01 to Pinnaduwa, then very winding inland via Neluwa
    # --- KANDY CORRIDOR (E03) ---
    ("WESTHALL DH", "KANDY", 3.0),                  # E03 + last mile uphill
    ("MORAHENA DH", "KANDY", 3.2),                  # E03 + winding Knuckles approach
    ("MEEMURE PMCU", "KANDY", 4.6),                 # E03 then deep Knuckles, very remote
    ("AAMBAGAHAPELESSA DH", "KANDY", 5.0),          # far remote Kandy hills
    ("BATUMULLA DH", "KANDY", 4.9),                 # remote Kandy/Matale border hills
    # --- NUWARA ELIYA / CENTRAL HILLS (E03 via Kandy) ---
    ("NORTH MEDAKUMBURA DH", "NUWARA ELIYA", 3.5),  # via Kandy, plantation area
    ("GONAPITIYA DH", "NUWARA ELIYA", 3.6),         # via Kandy + NE road
    ("HAMBEGAMUWA DH", "MONERAGALA", 3.8),          # via Kandy, Moneragala border
    ("MULOYA DH", "NUWARA ELIYA", 3.8),             # deep hill country
    ("AGARAPATHANA DH", "NUWARA ELIYA", 3.6),       # via Kandy + Nuwara Eliya road
    ("UPCOT PMCU", "NUWARA ELIYA", 3.8),            # high plantation, winding access
    ("DAYAGAMA WEST DH", "NUWARA ELIYA", 4.0),      # deep Nuwara Eliya interior
    ("KALAGANWATTA PMCU", "NUWARA ELIYA", 4.5),     # remote hill plantation
    ("RUPAHA PMCU", "NUWARA ELIYA", 4.2),           # remote interior
    # --- MATALE (E03 + local) ---
    ("ALUTHWEWA PMCU", "MATALE", 3.5),              # E03 to Dambulla area + last mile
    ("OPALGALA PMCU", "MATALE", 3.5),               # E03 + Matale hills
    ("HATTOTA AMUNA DH", "MATALE", 4.5),            # deep Matale, beyond Sigiriya
    ("MARAKA DH", "MATALE", 4.5),                   # deep Matale interior
    # --- KURUNEGALA / N. WESTERN (E03) ---
    ("PAHALAGIRIBAWA DH", "KURUNEGALA", 3.1),       # E03 + A33 last mile
    ("USGALA SIYABALANGAMUWA PMCU", "KURUNEGALA", 3.2), # E03 + rural last mile
    ("RAJANGANAYA DH", "KURUNEGALA", 3.5),          # NW via irrigation area
    # --- NORTH CENTRAL / ANURADHAPURA (E03 + A9) ---
    ("ANDIYAGALA DH", "ANURADHAPURA", 3.1),         # A9 from Anuradhapura, ~190 km road
    ("THANTIRIMALE DH", "ANURADHAPURA", 4.3),       # deep jungle north of Anuradhapura
    ("WAHALKADA DH", "ANURADHAPURA", 4.5),          # far NE Anuradhapura via A9
    ("KUNCHUKULAM PMCU", "ANURADHAPURA", 5.4),      # Mannar direction from Vavuniya
    # --- MONERAGALA / UVA EAST ---
    ("KOTIYAGALA PMCU", "MONERAGALA", 5.5),         # far east Moneragala towards Batticaloa
    ("INGINIYAGALA DH", "MONERAGALA", 5.5),         # east Moneragala, remote
    # --- MANNAR (A9 via Vavuniya, then west) ---
    ("VANKALAI DH", "MANNAR", 5.5),                 # Mannar coast
    ("MURUNKAN BH", "MANNAR", 5.4),                 # near Mannar, A14 road
    ("VIDATHALTIVU DH", "MANNAR", 5.9),             # west coast remote
    ("THARAPURAM PMCU", "MANNAR", 6.0),             # west coast remote
    ("PERIYAMADHU PMCU", "MANNAR", 5.9),            # north Mannar area
    ("ERUKALAMPIDDY DH", "MANNAR", 6.2),            # far NW near Mannar coast
    ("THALAIMANNAR DH", "MANNAR", 6.1),             # Thalaimannar tip, ferry point
    # --- VAVUNIYA ---
    ("NEDUNKERNY DH", "VAVUNIYA", 5.7),             # north Vavuniya on A9
    # --- TRINCOMALEE ---
    ("SERUWILA DH", "TRINCOMALEE", 5.2),            # via Habarana + A11, accessible
    ("GOMARANKADAWELA DH", "TRINCOMALEE", 5.5),     # north Trincomalee, remote
    ("MANALCHENAI PMCU", "TRINCOMALEE", 6.0),       # east coast Trincomalee
    ("PADAVISIRIPURA DH", "TRINCOMALEE", 6.0),      # towards Mullaitivu direction
    ("SAMPOOR DH", "TRINCOMALEE", 6.2),             # east coast Trincomalee
    ("KILIVETTY DH", "TRINCOMALEE", 6.0),           # east coast
    ("KILIVETTY OH", "TRINCOMALEE", 6.0),           # same location (OCR variant)
    # --- MULLAITIVU ---
    ("WELIOYA MOH", "MULLAITIVU", 5.5),             # A9 + east via Welioya
    ("MALLAVI BH", "MULLAITIVU", 6.2),              # north Mullaitivu
    ("THUNUKKAI PMCU", "MULLAITIVU", 6.3),          # north Mullaitivu
    ("NANDANKANNDAL DH", "MULLAITIVU", 6.0),        # difficult station list spelling
    ("NADDANKANDAL DH", "MULLAITIVU", 6.0),         # vacancy list OCR spelling
    ("ODDUSUDDAN DH", "MULLAITIVU", 6.5),           # deep Mullaitivu
    ("ALAMPIL DH", "MULLAITIVU", 7.0),              # far north coast
    ("PUTHUKKUDYIRUPPU BH", "MULLAITIVU", 7.0),     # far north Mullaitivu
    # --- KILINOCHCHI ---
    ("POONAKERY DH", "KILINOCHCHI", 6.2),           # A9 via Kilinochchi area
    ("POONAKERY POONARYN DH", "KILINOCHCHI", 6.2), # vacancy list full name
    # --- JAFFNA ---
    ("MULLIYAN PMCU", "JAFFNA", 6.7),               # Jaffna peninsula tip
    ("KAYTS BH", "JAFFNA", 7.0),                    # Kayts island (short boat/causeway from Jaffna)
    ("ANALATIVU DH", "JAFFNA", 10.5),               # island, requires ferry from Jaffna
    # --- BATTICALOA ---
    ("KATHIRAVELY DH", "BATTICALOA", 6.3),          # north Batticaloa coast
    ("NAWALKADU DH", "BATTICALOA", 6.8),            # north Batticaloa
    ("MANDUR DH", "BATTICALOA", 6.7),               # Batticaloa interior
    ("PALUGAMAM DH", "BATTICALOA", 6.5),            # Batticaloa area
    # --- AMPARA / EASTERN ---
    ("TAMPITIYA PMCU", "AMPARA", 5.8),              # via Kandy-Mahiyanganaya-Ampara, ~290 km
    ("SENARATHPURA DH", "AMPARA", 6.5),             # east Ampara
    ("LAHUGALA MOH", "AMPARA", 6.5),                # deep Ampara, Lahugala area
    ("WEERAGODA PMCU", "AMPARA", 6.5),              # east Ampara
    ("ISENARATHPURA DH", "AMPARA", 6.5),            # same as SENARATHPURA (OCR variant)
    ("DEEGAWAPIYA DH", "KALMUNAI", 7.0),            # east Kalmunai coast area
    ("ANNAMALAI DH", "KALMUNAI", 7.0),              # Kalmunai interior
    ("IRAKKAMAM DH", "KALMUNAI", 6.5),              # Kalmunai area
    ("IRAKKAMAM ERAGAMA DH", "KALMUNAI", 6.5),      # same location
    ("ULLAI PMCU", "KALMUNAI", 7.0),                # south Kalmunai / Pottuvil area
    ("THIRUKKOVIL BH", "KALMUNAI", 7.0),            # south Kalmunai coast
    ("PANAMA DH", "AMPARA", 7.5),                   # extreme SE, very remote coastal
    ("HOSPITAL", "KALMUNAI", 7.0),                  # Kalmunai area (blood bank)
]

coords = {
    "NARISSA PMCU": (6.6167, 80.2167), "MOLKAWA PMCU": (6.6051, 80.2377), "YATTAPATHA PMCU": (6.4667, 80.2167),
    "POTHUPITIYA DH": (6.4634, 80.4307), "DERANGALA PMCU": (6.2167, 80.5667), "ALUPOLA DH": (6.7167, 80.6167),
    "HALVITIGALA PMCU": (6.2833, 80.3167), "ROTAMBA PMCU": (6.1833, 80.5833), "PALAMKOTTE DH": (6.3333, 80.6167),
    "BERALIHERA PMCU": (6.1667, 81.0167), "AGARAPATHANA DH": (6.8641, 80.7056), "UPCOT PMCU": (6.7790, 80.6243),
    "WESTHALL DH": (7.0667, 80.5667), "RAJANGANAYA DH": (8.1657, 80.1964), "ALUTHWEWA PMCU": (8.0833, 80.9667),
    "OPALGALA PMCU": (7.5833, 80.7167), "USGALA SIYABALANGAMUWA PMCU": (8.0167, 80.3167), "DAYAGAMA WEST DH": (6.8548, 80.7586),
    "MORAHENA DH": (7.2167, 80.6833), "ANDIYAGALA DH": (7.9005, 80.5272), "PAHALAGIRIBAWA DH": (7.9833, 80.3500),
    "LANKAGAMA PMCU": (6.3333, 80.4667), "HAMBEGAMUWA DH": (6.5406, 80.9419), "GONAPITIYA DH": (7.0333, 80.7333),
    "NORTH MEDAKUMBURA DH": (6.9967, 80.6359), "MULOYA DH": (7.0667, 80.7667), "MEEMURE PMCU": (7.4333, 80.8333),
    "HATTOTA AMUNA DH": (7.6833, 80.8500), "KALAGANWATTA PMCU": (7.1000, 80.9000), "RUPAHA PMCU": (7.0500, 80.8500),
    "AAMBAGAHAPELESSA DH": (7.2722, 80.9833), "BATUMULLA DH": (7.4170, 80.9330), "THANTIRIMALE DH": (8.3500, 80.3833),
    "KOTIYAGALA PMCU": (6.7726, 81.5297), "KUNCHUKULAM PMCU": (8.8333, 80.0500), "MURUNKAN BH": (8.8326, 80.0324),
    "MARAKA DH": (7.5833, 80.9667), "WAHALKADA DH": (8.5667, 80.6222), "SERUWILA DH": (8.3708, 81.3193),
    "PERIYAMADHU PMCU": (9.0182, 80.1706), "VANKALAI DH": (8.8922, 79.9352), "WELIOYA MOH": (9.0125, 80.7850),
    "GOMARANKADAWELA DH": (8.7333, 80.9833), "MANALCHENAI PMCU": (8.5167, 81.1833), "PADAVISIRIPURA DH": (8.9367, 80.8133),
    "NEDUNKERNY DH": (9.1167, 80.5333), "ERUKALAMPIDDY DH": (9.1167, 79.8333), "THARAPURAM PMCU": (9.05, 79.85),
    "VIDATHALTIVU DH": (9.0333, 79.9833), "MALLAVI BH": (9.1333, 80.2833), "THUNUKKAI PMCU": (9.1500, 80.2167),
    "INGINIYAGALA DH": (7.2138, 81.5432), "ODDUSUDDAN DH": (9.1519, 80.6493), "POONAKERY DH": (9.5000, 80.2000),
    "NAWALKADU DH": (7.7167, 81.6833), "MANDUR DH": (7.5167, 81.7333), "PALUGAMAM DH": (7.5333, 81.7167),
    "ALAMPIL DH": (9.1500, 80.8500), "PUTHUKKUDYIRUPPU BH": (9.3167, 80.7167), "SAMPOOR DH": (8.4833, 81.2833),
    "THALAIMANNAR DH": (9.0834, 79.7344), "KATHIRAVELY DH": (8.1167, 81.3833), "MULLIYAN PMCU": (9.5414, 80.4722),
    "KAYTS BH": (9.6667, 79.9833), "KILIVETTY DH": (8.5833, 81.2167), "KILIVETTY OH": (8.5833, 81.2167),
    "NADDANKANDAL DH": (9.2167, 80.5167), "NANDANKANNDAL DH": (9.2167, 80.5167),
    "SENARATHPURA DH": (7.2912, 81.6724), "ISENARATHPURA DH": (7.2912, 81.6724), "LAHUGALA MOH": (6.8781, 81.7200),
    "WEERAGODA PMCU": (7.3830, 81.6968), "DEEGAWAPIYA DH": (7.2842, 81.7867), "TAMPITIYA PMCU": (7.4167, 81.4833),
    "ANNAMALAI DH": (7.4500, 81.7833), "IRAKKAMAM DH": (7.2500, 81.7167), "IRAKKAMAM ERAGAMA DH": (7.2500, 81.7167),
    "ULLAI PMCU": (6.8417, 81.8333), "THIRUKKOVIL BH": (7.1150, 81.8519), "PANAMA DH": (6.7500, 81.8000),
    "HOSPITAL": (7.4199, 81.8228), "ANALATIVU DH": (9.6667, 79.7667)
}

def normalize_designation(raw):
    """Normalize messy OCR designation strings into clean groups."""
    d = raw.strip().upper().replace('.', '').replace('[', '').replace('!', '').strip()
    if d in ('AMOH', 'AMOH'): return 'AMOH'
    if d == 'MOIC': return 'MOIC'
    if 'RELIEF' in d: return 'MO Relief'
    if 'MENTAL HEALTH' in d: return 'MO Mental Health'
    if 'ANAESTHESIA' in d or 'ANESTHESIA' in d: return 'MO Anaesthesia / ICU'
    if 'BLOOD BANK' in d: return 'MO Blood Bank'
    if 'CARDIOLOGY' in d: return 'MO Cardiology'
    if 'DIALYSIS' in d: return 'MO Dialysis'
    if d == 'MO ENT' or d == 'ENT' in d and 'MO' in d: return 'MO ENT'
    if 'ENT' in d: return 'MO ENT'
    if 'EYE' in d or 'VITREO' in d or 'OPHTHAL' in d: return 'MO Eye'
    if 'GYN' in d or 'OBS' in d: return 'SHO GYN & OBS' if d.startswith('SHO') else 'MO GYN & OBS'
    if 'PICU' in d or 'NICU' in d or 'MICU' in d or 'SICU' in d: return 'MO ICU'
    if 'ICU' in d and 'NEURO' not in d: return 'MO Anaesthesia / ICU'
    if 'NEURO SURGERY' in d or 'NEUROLOGY' in d: return 'MO Neurology / Neurosurgery'
    if 'PBU' in d or 'SCBU' in d: return 'MO PBU / SCBU'
    if 'PAEDIATRIC SURGERY' in d: return 'MO Surgery'
    if 'PAEDIATRIC' in d or 'PAEDIATRICS' in d: return 'SHO Paediatrics' if d.startswith('SHO') else 'MO Paediatrics'
    if 'PATHOLOGY' in d or 'CHEMICAL PATH' in d or 'MICROBIOLOGY' in d or 'HAEMATOLOGY' in d: return 'MO Pathology / Lab'
    if 'PSYCHIATRY' in d: return 'MO Psychiatry'
    if 'RADIOLOGY' in d: return 'MO Radiology'
    if 'REHABILITATION' in d: return 'MO Rehabilitation'
    if 'ONCOL' in d or 'ONCO' in d: return 'MO Oncology'
    if 'ORTHO' in d: return 'MO Orthopaedic'
    if 'VASCULAR' in d or 'TRANSPLANT' in d: return 'MO Vascular Surgery'
    if 'PLASTIC' in d: return 'MO Surgery'
    if 'UROLOGY' in d or 'GU SURGERY' in d or 'GENITO' in d: return 'MO Urology / GU'
    if 'NEPHROLOGY' in d: return 'MO Nephrology'
    if 'ENDOCRINOLOGY' in d: return 'MO Endocrinology'
    if 'RHEUMATOLOGY' in d: return 'MO Rheumatology'
    if 'GASTRO' in d: return 'MO Gastroenterology'
    if 'RESPIRATORY' in d or 'PULMONOL' in d: return 'MO Respiratory'
    if 'DERMATOLOGY' in d: return 'MO Dermatology'
    if 'MEDICO LEGAL' in d: return 'MO Medico Legal'
    if 'STD' in d: return 'MO STD'
    if 'A&E' in d: return 'MO A&E'
    if 'ETU' in d or 'OPD' in d: return 'MO OPD / ETU'
    if 'SURGERY' in d and d.startswith('SHO'): return 'SHO Surgery'
    if 'MEDICINE' in d and d.startswith('SHO'): return 'SHO Medicine'
    if 'SURGERY' in d: return 'MO Surgery'
    if 'MEDICINE' in d: return 'MO Medicine'
    if 'SOE' in d: return 'MO (SOE)'
    if d.startswith('SHO'): return 'SHO'
    # General MO catch-all
    return 'MO'

def is_dh(institute):
    """True if the institute name ends with DH (District Hospital)."""
    name = institute.strip().upper().replace('|','').replace('[','').replace(']','').strip()
    return name.endswith(' DH') or name.endswith('DH')

def create_files():
    # Load difficult station indices
    difficult_indices = set()
    with open('AVAILABLE_DIFFICULT_STATIONS.csv', 'r') as f:
        for row in csv.DictReader(f):
            difficult_indices.add(row['INDEX'])

    # Build difficult stations list with ETA + coords
    stations = []
    with open('AVAILABLE_DIFFICULT_STATIONS.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            inst = row['INSTITUTE'].strip().upper()
            clean_name = inst.replace('|', '').replace('_', '').replace('[', '').replace(']', '').strip()

            # Find ETA
            eta = None
            for e_name, e_dist, e_time in eta_data:
                if e_name in clean_name or clean_name in e_name:
                    eta = e_time
                    break
            if eta is None:
                if row['DISTRICT'] in ['JAFFNA', 'MULLAITIVU', 'KILINOCHCHI']: eta = 7.0
                elif row['DISTRICT'] in ['AMPARA', 'KALMUNAI', 'BATTICALOA']: eta = 8.0
                else: eta = 5.0

            # Find Lat/Lon
            lat, lon = None, None
            if clean_name in coords: lat, lon = coords[clean_name]
            else:
                for k, v in coords.items():
                    if k in clean_name or clean_name in k:
                        lat, lon = v; break

            stations.append({
                "INDEX": row['INDEX'],
                "DISTRICT": row['DISTRICT'],
                "INSTITUTE": row['INSTITUTE'],
                "DESIGNATION": row['DESIGNATION'],
                "VACANCIES": row['VACANCIES'],
                "ESTIMATED_TRAVEL_TIME_HOURS": eta,
                "IS_DH": "YES" if is_dh(row['INSTITUTE']) else "NO",
                "DESIG_GROUP": normalize_designation(row['DESIGNATION']),
                "lat": lat,
                "lon": lon
            })

    stations.sort(key=lambda x: x['ESTIMATED_TRAVEL_TIME_HOURS'])

    # Write DIFFICULT_STATIONS_BY_ETA.csv
    with open('DIFFICULT_STATIONS_BY_ETA.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['INDEX', 'DISTRICT', 'INSTITUTE', 'DESIGNATION', 'VACANCIES', 'ESTIMATED_TRAVEL_TIME_HOURS', 'IS_DH', 'DESIG_GROUP'])
        writer.writeheader()
        for s in stations:
            writer.writerow({k: v for k, v in s.items() if k in ['INDEX', 'DISTRICT', 'INSTITUTE', 'DESIGNATION', 'VACANCIES', 'ESTIMATED_TRAVEL_TIME_HOURS', 'IS_DH', 'DESIG_GROUP']})

    # Write NON_DIFFICULT_STATIONS.csv
    with open('NON_DIFFICULT_STATIONS.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['INDEX', 'DISTRICT', 'INSTITUTE', 'DESIGNATION', 'VACANCIES', 'IS_DH', 'DESIG_GROUP'])
        writer.writeheader()
        with open('Source/Vacancy List.csv', 'r') as vf:
            for row in csv.DictReader(vf):
                if row['INDEX'] not in difficult_indices:
                    writer.writerow({
                        'INDEX': row['INDEX'],
                        'DISTRICT': row['DISTRICT'],
                        'INSTITUTE': row['INSTITUTE'],
                        'DESIGNATION': row['DESIGNATION'],
                        'VACANCIES': row['VACANCIES'],
                        'IS_DH': "YES" if is_dh(row['INSTITUTE']) else "NO",
                        'DESIG_GROUP': normalize_designation(row['DESIGNATION'])
                    })

    # Write markers.js — difficult stations only (have ETAs + coords)
    valid_markers = [{
        "name": s['INSTITUTE'],
        "district": s['DISTRICT'],
        "lat": s['lat'],
        "lon": s['lon'],
        "eta": s['ESTIMATED_TRAVEL_TIME_HOURS'],
        "vacancies": s['VACANCIES'],
        "designation": s['DESIGNATION'],
        "desig_group": s['DESIG_GROUP'],
        "is_difficult": True,
        "is_dh": is_dh(s['INSTITUTE'])
    } for s in stations if s['lat']]
    with open('markers.js', 'w') as f:
        f.write("var markersData = " + json.dumps(valid_markers) + ";")

    # Generate Hash for "redda2026"
    pwd_hash = hashlib.sha256("redda2026".encode()).hexdigest()

    html_template = """<!DOCTYPE html>
<html>
<head>
    <title>Difficult Stations Sri Lanka</title>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
    <script src="markers.js"></script>
    <style>
        * { box-sizing: border-box; }
        body { margin: 0; padding: 0; font-family: Arial, sans-serif; }
        #map { height: 100vh; width: 100%; display: none; }

        /* Login */
        #login-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: #f0f2f5; display: flex; justify-content: center; align-items: center; z-index: 10000; }
        .login-box { background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); text-align: center; width: 300px; }
        .login-box h2 { margin-bottom: 20px; color: #1c1e21; }
        .login-box input { width: 100%; padding: 12px; margin-bottom: 16px; border: 1px solid #dddfe2; border-radius: 6px; font-size: 16px; }
        .login-box button { width: 100%; padding: 12px; background: #1877f2; color: white; border: none; border-radius: 6px; font-size: 16px; font-weight: bold; cursor: pointer; }
        #error-msg { color: #d93025; font-size: 14px; margin-top: 10px; display: none; }

        /* Filter panel */
        #filter-panel {
            position: fixed; top: 10px; right: 10px; z-index: 1000;
            background: white; border-radius: 10px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.2);
            width: 240px; display: none;
        }
        #filter-header {
            padding: 10px 14px; font-weight: bold; font-size: 14px;
            background: #1877f2; color: white; border-radius: 10px 10px 0 0;
            cursor: pointer; display: flex; justify-content: space-between; align-items: center;
        }
        #filter-body { padding: 12px 14px; }
        #filter-body.collapsed { display: none; }
        .filter-section { margin-bottom: 12px; }
        .filter-section label.section-label {
            font-size: 11px; font-weight: bold; color: #666;
            text-transform: uppercase; letter-spacing: 0.5px;
            display: block; margin-bottom: 6px;
        }
        .radio-group label, .checkbox-row label {
            display: flex; align-items: center; gap: 6px;
            font-size: 13px; cursor: pointer; padding: 2px 0;
        }
        select#desig-filter {
            width: 100%; padding: 6px 8px; font-size: 13px;
            border: 1px solid #ddd; border-radius: 5px;
        }
        #filter-count {
            font-size: 12px; color: #555; text-align: center;
            padding: 6px 0 2px; border-top: 1px solid #eee; margin-top: 8px;
        }
        .reset-btn {
            width: 100%; margin-top: 8px; padding: 6px;
            font-size: 12px; background: #f0f2f5; border: 1px solid #ddd;
            border-radius: 5px; cursor: pointer;
        }
        .reset-btn:hover { background: #e0e2e5; }

        /* Legend */
        .legend { line-height: 20px; font-size: 13px; padding: 8px 10px; }
        .legend i { width: 12px; height: 12px; display: inline-block; margin-right: 5px; border-radius: 50%; vertical-align: middle; }
        .legend .dh-icon { border-radius: 2px; }
    </style>
</head>
<body>
    <div id="login-overlay">
        <div class="login-box">
            <h2>Difficult Stations Map</h2>
            <input type="password" id="password-input" placeholder="Enter password" onkeydown="if(event.key==='Enter') checkPassword()">
            <button onclick="checkPassword()">Unlock Map</button>
            <p id="error-msg">Incorrect password!</p>
        </div>
    </div>

    <div id="filter-panel">
        <div id="filter-header" onclick="toggleFilters()">
            <span>&#9660; Filters</span>
            <span id="filter-count-badge" style="font-size:11px; font-weight:normal;"></span>
        </div>
        <div id="filter-body">
            <div class="filter-section">
                <label class="section-label">Station Type</label>
                <div class="radio-group">
                    <label><input type="radio" name="stype" value="all" checked onchange="applyFilters()"> All Difficult Stations</label>
                    <label><input type="radio" name="stype" value="dh" onchange="applyFilters()"> DH only</label>
                    <label><input type="radio" name="stype" value="nondh" onchange="applyFilters()"> Non-DH only</label>
                </div>
            </div>
            <div class="filter-section">
                <label class="section-label">Designation</label>
                <select id="desig-filter" onchange="applyFilters()">
                    <option value="">All Designations</option>
                </select>
            </div>
            <div id="filter-count"></div>
            <button class="reset-btn" onclick="resetFilters()">Reset Filters</button>
        </div>
    </div>

    <div id="map"></div>

    <script>
    function toggleFilters() {
        var body = document.getElementById('filter-body');
        var hdr = document.getElementById('filter-header').querySelector('span');
        if (body.classList.contains('collapsed')) {
            body.classList.remove('collapsed');
            hdr.textContent = '\\u25BC Filters';
        } else {
            body.classList.add('collapsed');
            hdr.textContent = '\\u25B2 Filters';
        }
    }

    async function checkPassword() {
        const password = document.getElementById('password-input').value;
        const hashBuffer = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(password));
        const hashHex = Array.from(new Uint8Array(hashBuffer)).map(b => b.toString(16).padStart(2,'0')).join('');
        if (hashHex === '%PWD_HASH%') {
            document.getElementById('login-overlay').style.display = 'none';
            document.getElementById('map').style.display = 'block';
            document.getElementById('filter-panel').style.display = 'block';
            initMap();
        } else {
            document.getElementById('error-msg').style.display = 'block';
        }
    }

    var allMarkerLayers = [];
    var map;

    function etaColor(eta) {
        if (eta < 3) return '#27ae60';
        if (eta < 5) return '#e67e22';
        return '#e74c3c';
    }

    function initMap() {
        map = L.map('map').setView([7.8731, 80.7718], 7);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; OpenStreetMap contributors'
        }).addTo(map);

        // Populate designation filter
        var desigs = [...new Set(markersData.map(m => m.desig_group))].sort();
        var sel = document.getElementById('desig-filter');
        desigs.forEach(function(d) {
            var opt = document.createElement('option');
            opt.value = d; opt.textContent = d;
            sel.appendChild(opt);
        });

        // Build markers
        markersData.forEach(function(m) {
            var color = etaColor(parseFloat(m.eta));
            var radius = m.is_dh ? 9 : 7;
            var dashArray = m.is_dh ? null : '4 3';
            var shape = L.circleMarker([m.lat, m.lon], {
                color: color, fillColor: color, fillOpacity: 0.6,
                radius: radius, weight: 2, dashArray: dashArray
            });
            shape.bindPopup(
                '<b>' + m.name + '</b>' +
                (m.is_dh ? ' <span style="background:#2980b9;color:white;padding:1px 5px;border-radius:3px;font-size:11px;">DH</span>' : '') +
                '<br>District: ' + m.district +
                '<br>Designation: ' + m.designation +
                ' <small style="color:#888;">(' + m.desig_group + ')</small>' +
                '<br>Vacancies: ' + m.vacancies +
                '<br>ETA from Homagama: <b>' + m.eta + ' hrs</b>'
            );
            allMarkerLayers.push({ layer: shape, data: m });
            shape.addTo(map);
        });

        // Legend
        var legend = L.control({ position: 'bottomright' });
        legend.onAdd = function() {
            var div = L.DomUtil.create('div', 'info legend');
            div.innerHTML =
                '<b>ETA from Homagama</b><br>' +
                '<i style="background:#27ae60"></i> &lt; 3 hrs<br>' +
                '<i style="background:#e67e22"></i> 3 – 5 hrs<br>' +
                '<i style="background:#e74c3c"></i> &gt; 5 hrs<br>' +
                '<hr style="margin:6px 0">' +
                '<i style="background:#aaa;border-radius:2px!important"></i> DH (filled)<br>' +
                '<i style="background:transparent;border:2px dashed #aaa;border-radius:50%"></i> Non-DH';
            return div;
        };
        legend.addTo(map);
        updateCount();
    }

    function applyFilters() {
        var stype = document.querySelector('input[name=stype]:checked').value;
        var desig = document.getElementById('desig-filter').value;
        allMarkerLayers.forEach(function(ml) {
            var m = ml.data;
            var show = true;
            if (stype === 'dh' && !m.is_dh) show = false;
            if (stype === 'nondh' && m.is_dh) show = false;
            if (desig && m.desig_group !== desig) show = false;
            if (show) { if (!map.hasLayer(ml.layer)) ml.layer.addTo(map); }
            else { if (map.hasLayer(ml.layer)) map.removeLayer(ml.layer); }
        });
        updateCount();
    }

    function resetFilters() {
        document.querySelector('input[name=stype][value=all]').checked = true;
        document.getElementById('desig-filter').value = '';
        applyFilters();
    }

    function updateCount() {
        var visible = allMarkerLayers.filter(ml => map.hasLayer(ml.layer)).length;
        var total = allMarkerLayers.length;
        var txt = 'Showing ' + visible + ' of ' + total + ' stations';
        document.getElementById('filter-count').textContent = txt;
        document.getElementById('filter-count-badge').textContent = visible + '/' + total;
    }
    </script>
</body>
</html>
""".replace('%PWD_HASH%', pwd_hash)

    with open('index.html', 'w') as f:
        f.write(html_template)
    print(f"Files re-generated with updated ETAs. Total: {len(valid_markers)}")

if __name__ == "__main__":
    create_files()
