import csv
import difflib

def normalize(text):
    if not text: return ""
    # Remove common noise and normalize case/spacing
    text = text.upper().replace('|', '').replace('_', '').replace('[', '').replace(']', '')
    return " ".join(text.split())

def find_matches():
    difficult_stations = []
    with open('Available list.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            difficult_stations.append({
                'SN': row['SN'],
                'STATION': normalize(row['STATION']),
                'ORIGINAL_STATION': row['STATION'],
                'DISTRICT': row['RDHS'].upper()
            })

    vacancy_list = []
    with open('PDF537_vac.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            vacancy_list.append({
                'INDEX': row['INDEX'],
                'INSTITUTE': normalize(row['INSTITUTE']),
                'ORIGINAL_INSTITUTE': row['INSTITUTE'],
                'DISTRICT': row['DISTRICT'].upper(),
                'DESIGNATION': row['DESIGNATION'],
                'VACANCIES': row['VACANCIES']
            })

    matched_indices = set()
    final_matches = []
    potential_mismatches = []

    # 1. Exact or Substring Matching
    for vac in vacancy_list:
        v_name = vac['INSTITUTE']
        matched = False
        for diff in difficult_stations:
            d_name = diff['STATION']
            
            # Match if one is inside other (significant words only)
            if v_name == d_name or (len(d_name) > 5 and (d_name in v_name or v_name in d_name)):
                # Optional: check district too to be sure
                # Some names might repeat across districts
                final_matches.append(vac)
                matched_indices.add(vac['INDEX'])
                matched = True
                break
        
        if not matched:
            # 2. Fuzzy Matching for leftovers
            for diff in difficult_stations:
                d_name = diff['STATION']
                ratio = difflib.SequenceMatcher(None, v_name, d_name).ratio()
                if ratio > 0.75: # High similarity
                    potential_mismatches.append({
                        'VAC_INDEX': vac['INDEX'],
                        'VAC_NAME': vac['ORIGINAL_INSTITUTE'],
                        'DIFF_NAME': diff['ORIGINAL_STATION'],
                        'VAC_DISTRICT': vac['DISTRICT'],
                        'DIFF_DISTRICT': diff['DISTRICT'],
                        'RATIO': round(ratio, 2)
                    })
                    break

    # Save exact matches to CSV
    with open('AVAILABLE_DIFFICULT_STATIONS.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['INDEX', 'DISTRICT', 'INSTITUTE', 'DESIGNATION', 'VACANCIES'])
        writer.writeheader()
        # Sort by index
        sorted_matches = sorted(final_matches, key=lambda x: int(x['INDEX']))
        for m in sorted_matches:
            writer.writerow({
                'INDEX': m['INDEX'],
                'DISTRICT': m['DISTRICT'],
                'INSTITUTE': m['ORIGINAL_INSTITUTE'],
                'DESIGNATION': m['DESIGNATION'],
                'VACANCIES': m['VACANCIES']
            })

    print(f"Exact/Substring Matches Found: {len(final_matches)}")
    print("\nPotential Matches (Please review):")
    print(f"{'VAC_IDX':<8} | {'VAC_INSTITUTE':<35} | {'DIFF_STATION':<35} | {'SCORE'}")
    print("-" * 100)
    for pm in potential_mismatches:
        print(f"{pm['VAC_INDEX']:<8} | {pm['VAC_NAME']:<35} | {pm['DIFF_NAME']:<35} | {pm['RATIO']}")

if __name__ == "__main__":
    find_matches()
