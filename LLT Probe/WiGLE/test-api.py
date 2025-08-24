import requests
from requests.auth import HTTPBasicAuth

# WiGLE API credentials
api_name = ""
api_token = ""



bssid_list = [

]

# WiGLE API endpoint
base_url = "https://api.wigle.net/api/v2/network/detail"

# Check each BSSID
for bssid in bssid_list:
    print(f"Checking BSSID: {bssid}")
    response = requests.get(
        f"{base_url}?netid={bssid}",
        auth=HTTPBasicAuth(api_name, api_token)
    )

    if response.status_code == 200:
        data = response.json()
        if data.get("success") and data.get("results"):
            result = data["results"][0]
            print(f"Found: SSID={result.get('ssid')}, Location=({result.get('trilat')}, {result.get('trilong')}), Last Seen={result.get('lastupdt')}\n")
        else:
            print("Not found in WiGLE\n")
    else:
        print(f"API Error {response.status_code}: {response.text}\n")
