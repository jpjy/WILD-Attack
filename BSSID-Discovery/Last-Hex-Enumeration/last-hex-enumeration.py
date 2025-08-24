import ast
import math
from wloc import QueryBSSID
import pprint
import os

# === CONFIGURATION ===

DISTANCE_THRESHOLD_METERS = 100.0  # max valid radius

INPUT_DIR = ""
OUTPUT_DIR = ""
INPUT_PATTERN = ""
OUTPUT_PATTERN = ""

FILE_RANGE = range(11, 21)  


# === UTILS ===

def load_bssids(filename):
    """Load original BSSIDs and their (lat, lon) from input dictionary file."""
    with open(filename, "r") as f:
        content = f.read()
    return ast.literal_eval(content)  # dict: {bssid: (lat, lon)}

def enumerate_last_hex(bssid):
    """Enumerate all BSSIDs with the same prefix and last byte from x0 to xf (e.g., 90 to 9f)."""
    parts = bssid.split(":")
    if len(parts) != 6:
        return []

    prefix = ":".join(parts[:5])
    last_byte = int(parts[5], 16)
    base = last_byte & 0xF0  # upper nibble group

    return [f"{prefix}:{i:02x}" for i in range(base, base + 16)]

def is_valid_location(loc):
    """Return True if the Apple response is not (-180.0, -180.0)."""
    return loc is not None and loc != (-180.0, -180.0)

def haversine(coord1, coord2):
    """Calculate great-circle distance between two (lat, lon) points in meters."""
    R = 6371000  # Earth radius in meters
    lat1, lon1 = coord1
    lat2, lon2 = coord2

    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c

# === CORE ===

def query_bssid_variants(bssid_dict):
    """For each original BSSID, enumerate variations and keep those within 100m."""
    discovered = {}
    for original, origin_loc in bssid_dict.items():
        variants = enumerate_last_hex(original)
        print(f"[+] Querying {len(variants)} variants of {original} (ref @ {origin_loc})")
        found = []

        for bssid in variants:
            try:
                result = QueryBSSID([bssid])
                loc = result.get(bssid)
                if is_valid_location(loc):
                    distance = haversine(origin_loc, loc)
                    if distance <= DISTANCE_THRESHOLD_METERS:
                        found.append((bssid, loc))
            except Exception as e:
                print(f"[!] Error querying {bssid}: {e}")
        
        discovered[original] = found
    return discovered

def write_results(discovered, output_file):
    """Write original BSSID and valid varied BSSIDs with (lat, lon) to file."""
    with open(output_file, "w") as f:
        for original, variants in discovered.items():
            if variants:
                f.write(f"{original}:\n")
                for bssid, (lat, lon) in variants:
                    f.write(f"  - {bssid} -> ({lat:.6f}, {lon:.6f})\n")
                f.write("\n")

def count_total_bssids(discovered_dict):
    """Count total unique BSSIDs: original + valid variants, but avoid double-counting."""
    total = 0
    for original, variants in discovered_dict.items():
        variant_bssids = {bssid for bssid, _ in variants}
        if original not in variant_bssids:
            total += 1  # count original separately if not in variants
        total += len(variant_bssids)
    print(f"[✔] Total number of unique BSSIDs (original + valid variants): {total}")


# def main():
#     bssid_dict = load_bssids(INPUT_FILE)
#     all_discovered = query_bssid_variants(bssid_dict)

#     print("\n=== Enumeration Results ===")
#     pprint.pprint(all_discovered)

#     write_results(all_discovered, OUTPUT_FILE)
#     print(f"\n[✔] Results written to: {OUTPUT_FILE}")
#     count_total_bssids(all_discovered)

def main():
    for i in FILE_RANGE:
        input_path = os.path.join(INPUT_DIR, INPUT_PATTERN.format(i))
        output_path = os.path.join(OUTPUT_DIR, OUTPUT_PATTERN.format(i))

        print(f"\n=== Processing {input_path} ===")
        bssid_dict = load_bssids(input_path)
        all_discovered = query_bssid_variants(bssid_dict)

        write_results(all_discovered, output_path)
        print(f"[✔] Results written to: {output_path}")
        count_total_bssids(all_discovered)

if __name__ == "__main__":
    main()
