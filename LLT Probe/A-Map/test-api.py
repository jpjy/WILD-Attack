import requests
import time

# Tencent Map API Config
#API_URL = "https://apilocate.amap.com/position"
API_URL = "http://8.138.206.8:5050/gd_position"
#API_KEY = "23ff36b2fe109a9162e7e34f88341aeb"  # Replace with your A-Map API Key
API_KEY = "8a3ddd69a104ae67a34b"
IMEI = "15030518977"

# Function to read MAC addresses from file and test
def test_amap_with_mac_list(file_path):
    with open(file_path, 'r') as file:
        mac_list = []
        for line in file:
            line = line.strip()
            if line and ':' in line:
                # Extracting MAC address (ignoring line numbers)
                mac = line.split()[-1]  # Last part should be the MAC
                mac_list.append(mac)

    if len(mac_list) < 2:
        print("At least two MAC addresses are required.")
        return

    base_mac = mac_list[0]

    for mac in mac_list[0:]:
        test_macs = f"{mac},-35"
        #response = requests.get(f"{API_URL}?key={API_KEY}&accesstype=1&imei={IMEI}&macs={test_macs}&output=json")
        response = requests.get(f"{API_URL}?token={API_KEY}&accesstype=1&imei={IMEI}&macs={test_macs}&output=json")
        print(f"Testing with MACs: {test_macs}")
        if response.status_code == 200:
            data = response.json()
            print(data)
        else:
            print(f"HTTP Error: {response.status_code}")

# Run the test with mac.txt file
test_amap_with_mac_list("mac-spoof.txt")