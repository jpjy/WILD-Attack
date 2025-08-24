import folium
import pandas as pd

# === Configuration ===
input_file = 'Tampa-1km/Obtain-Tampa-AP-1km-July-28.txt'  # change this to your actual filename
output_map = 'Tampa-1km/July-28-map.html'

# === Load and parse the file ===
# Assuming format: BSSID, latitude, longitude (comma-separated, with optional spaces)
df = pd.read_csv(input_file, header=None, names=['BSSID', 'Latitude', 'Longitude'])
df['Latitude'] = df['Latitude'].astype(float)
df['Longitude'] = df['Longitude'].astype(float)

# === Determine the map center (mean of coordinates) ===
center_lat = df['Latitude'].mean()
center_lon = df['Longitude'].mean()

# === Create map ===
m = folium.Map(location=[center_lat, center_lon], zoom_start=13)

# === Add all points as red CircleMarkers ===
for _, row in df.iterrows():
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=0.1,  # small dot
        color='red',
        fill=True,
        fill_opacity=0.7
    ).add_to(m)

# === Save to HTML ===
m.save(output_map)
print(f"Map saved to {output_map}")
