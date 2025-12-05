from wloc import QueryBSSID
import pprint

# List of BSSIDs 
bssids = ["00:e6:3a:87:22:36"]

# Query Apple's WiFi positioning service
location_data = QueryBSSID(bssids)

# Print the results
pprint.pprint(location_data)
#print(location_data)
