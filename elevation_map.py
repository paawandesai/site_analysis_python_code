import osmnx as ox
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colormaps

list(colormaps)

# Define the center point and distance for the area of interest
lat = 30.28846032303379
long = -97.73536240661028
point = (30.28846032303379, -97.73536240661028)
dist = 1000  # Distance in meters from the point

# Get the bounding box
north, south, east, west = ox.utils_geo.bbox_from_point(point, dist=dist)

# Create a network graph from the area
G = ox.graph_from_bbox(north, south, east, west, network_type='all')

# Add elevation data to nodes using Google Maps Elevation API
G = ox.elevation.add_node_elevations_google(G, api_key='AIzaSyAStyQvkqqCHiYoaasYJ101qV1ZfgpKofM')

# Get the elevation values from the graph nodes
elevation_values = [data['elevation'] for node, data in G.nodes(data=True)]
elevation_1d = np.array(elevation_values)

# Determine the appropriate shape for the elevation array
num_nodes = len(elevation_values)
pairs = []
for num_rows in range(1, int(num_nodes**0.5) + 1):
    if num_nodes % num_rows == 0:
        num_cols = num_nodes // num_rows
        pairs.append((num_rows, num_cols))

# Sort the pairs by the difference between the factors
pairs.sort(key=lambda x: abs(x[0] - x[1]))

# The pair with the smallest difference is the first one
closest_pair = pairs[0]
num_rows = closest_pair[0]
num_cols = closest_pair[1]
print("Number of Nodes:", num_nodes)
print('Number of rows:', num_rows)
print('Number of columns:', num_cols)   

# Convert the elevation values to a 2D grid
elevation_array = elevation_1d.reshape(num_rows, num_cols)

# Plotting the contour map
plt.figure(figsize=(10, 10))

# Create contour lines for elevation
contour_levels = np.linspace(np.min(elevation_array), np.max(elevation_array), 10)
plt.contourf(elevation_array, levels=contour_levels, cmap='terrain')

plt.plot(long, lat, 'r*', markersize=15)

# Set title and axis labels
plt.title('Elevation Map')
plt.xlabel('Longitude')
plt.ylabel('Latitude')

# Add colorbar for contour
cbar = plt.colorbar()
cbar.set_label('Elevation (m)')

# Show the map
plt.show()


#G = ox.elevation.add_node_elevations(G, api_key='AIzaSyAStyQvkqqCHiYoaasYJ101qV1ZfgpKofM')