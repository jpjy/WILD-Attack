import math
from wloc import QueryBSSID
import time

# === Location Utilities ===

def haversine(coord1, coord2):
    R = 6371000
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))

def bearing(from_coord, to_coord):
    lat1 = math.radians(from_coord[0])
    lat2 = math.radians(to_coord[0])
    diff_long = math.radians(to_coord[1] - from_coord[1])
    x = math.sin(diff_long) * math.cos(lat2)
    y = (math.cos(lat1)*math.sin(lat2)
         - math.sin(lat1)*math.cos(lat2)*math.cos(diff_long))
    initial = math.atan2(x, y)
    return (math.degrees(initial) + 360) % 360

def direction_name(bearing_degrees):
    dirs = ['N','NE','E','SE','S','SW','W','NW']
    return dirs[int((bearing_degrees+22.5)//45) % 8]


def dfs_navigate(mac, target_location, visited, path, reach_threshold, query_counter):
    """
    Recursive DFS to find a path from `mac` to within `reach_threshold` of `target_location`.
    Also tracks how many total unique BSSID queries were made (via `query_counter` set).
    """
    if mac in query_counter:
        return None  # Already queried and failed earlier

    time.sleep(0.5)

    result = QueryBSSID([mac])
    query_counter.add(mac)

    if not result or mac not in result:
        return None

    current_loc = result[mac]
    distance = haversine(current_loc, target_location)
    current_step = len(path)

    print(f"\n📍 Step {current_step}: At {current_loc} via {mac} — {distance:.1f} m to target")

    if distance <= reach_threshold:
        print(f"🎉 Reached target in {current_step} steps!")
        return path + [(mac, current_loc)]

    visited.add(mac)
    neighbors = [
        (nbr_mac, nbr_loc)
        for nbr_mac, nbr_loc in result.items()
        if nbr_mac not in visited
    ]
    neighbors.sort(key=lambda item: haversine(item[1], target_location))

    for nbr_mac, nbr_loc in neighbors:
        brng = bearing(current_loc, nbr_loc)
        dir_name = direction_name(brng)
        step_dist = haversine(current_loc, nbr_loc)
        print(f"  → Trying {nbr_mac} at {nbr_loc} ({step_dist:.1f} m {dir_name})")
        result_path = dfs_navigate(
            nbr_mac,
            target_location,
            visited,
            path + [(mac, current_loc)],
            reach_threshold,
            query_counter
        )
        if result_path:
            return result_path
        else:
            print(f"  ↩️  Backtracking from {nbr_mac}")

    return None


def navigate_to_target(start_mac, target_location, reach_threshold=25):
    visited = set()
    query_counter = set()  # Tracks how many unique BSSIDs we've queried
    full_path = dfs_navigate(start_mac, target_location, visited, [], reach_threshold, query_counter)

    print(f"\n📊 Total BSSIDs queried: {len(query_counter)}")

    if not full_path:
        print("❌ Could not find a path within threshold.")
    else:
        print(f"\n📌 Final Path (Total Hops: {len(full_path)}):")
        for i, (m, loc) in enumerate(full_path):
            print(f"  Hop {i}: {m} → {loc}")
    return full_path


# === Run Script ===

if __name__ == "__main__":
    
    start_mac = "00:e6:3a:87:22:36" # in Paris


    # # 19. Louvre Museum
    target_location = (48.86079458999164, 2.3376708197464815)


    path = navigate_to_target(start_mac, target_location, reach_threshold=25)
