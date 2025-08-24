import requests
import json
import time
from itertools import combinations

# Replace with your actual API key
API_KEY = ""
GEOLOCATION_URL = f"https://www.googleapis.com/geolocation/v1/geolocate?key={API_KEY}"

# Read MAC addresses from a file
def read_macs(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    macs = [line.strip().split()[-1] for line in lines if ':' in line]
    return macs

# Format request payload with signal strength
def build_payload(mac1, mac2):
    return {
        "wifiAccessPoints": [
            {"macAddress": mac1, "signalStrength": -35},
            {"macAddress": mac2, "signalStrength": -35}
        ]
    }

# Send geolocation request
def send_request(payload):
    response = requests.post(GEOLOCATION_URL, json=payload)
    return response.json()

# Main routine to test all pairs
def locate_all_pairs(filename):
    macs = read_macs(filename)
    mac_pairs = list(combinations(macs, 2))  # All unique pairs
    for idx, (mac1, mac2) in enumerate(mac_pairs):
        payload = build_payload(mac1, mac2)
        print(f"\n[{idx+1}/{len(mac_pairs)}] Sending request with: {mac1} & {mac2}")
        try:
            result = send_request(payload)
            print(json.dumps(result, indent=2))
        except Exception as e:
            print(f"Error during request: {e}")
        time.sleep(1)

# Example usage
locate_all_pairs("ap-list-2.txt")
