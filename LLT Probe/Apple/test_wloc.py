from wloc import QueryBSSID
import pprint

# List of BSSIDs 
bssids = [""]

# Query Apple's WiFi positioning service
location_data = QueryBSSID(bssids)

# Print the results
pprint.pprint(location_data)
#print(location_data)
