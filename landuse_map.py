import osmnx as ox
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point
from matplotlib.lines import Line2D
from matplotlib.colors import ListedColormap

# Define the center point and distance for the area of interest
point = (30.28846032303379, -97.73536240661028)
dist = 1000  # Distance in meters from the point

# Get the bounding box
north, south, east, west = ox.utils_geo.bbox_from_point(point, dist=dist)

# Get land use data and urban amenities
landuse_gdf = ox.geometries.geometries_from_bbox(north, south, east, west, tags={'landuse': True})
amenities_gdf = ox.geometries.geometries_from_bbox(north, south, east, west, tags={'amenity': True})

# Create a GeoDataFrame for the center point
point_gdf = gpd.GeoDataFrame(geometry=[Point(point[1], point[0])], crs='EPSG:4326')

# Define labels for urban amenities
amenity_labels = {
    'hospital': 'Hospital',
    'school': 'School',
    'restaurant': 'Restaurant',
    'parking': 'Parking',
    'bank': 'Bank',
    'pharmacy': 'Pharmacy',
    'place_of_worship': 'Place of Worship',
    'supermarket': 'Supermarket',
    'fire_station': 'Fire Station',
    'police': 'Police Station'
}

# Define colors for each amenity type
amenity_colors = {
    'hospital': 'red',
    'school': 'blue',
    'restaurant': 'green',
    'parking': 'orange',
    'bank': 'purple',
    'pharmacy': 'pink',
    'place_of_worship': 'brown',
    'supermarket': 'cyan',
    'fire_station': 'yellow',
    'police': 'grey'
}

# Create a colormap based on the colors
cmap = ListedColormap(list(amenity_colors.values()))

# Plotting the map
fig, ax = plt.subplots(figsize=(15, 15))

# Plot land use areas
if not landuse_gdf.empty:
    landuse_gdf.plot(ax=ax, column='landuse', legend=True, zorder=2)

# Plot urban amenities
amenity_legend_handles = []
for amenity_type, label in amenity_labels.items():
    if amenity_type in amenities_gdf['amenity'].unique():
        amenity_gdf = amenities_gdf[amenities_gdf['amenity'] == amenity_type]
        amenity_gdf.plot(ax=ax, color=amenity_colors[amenity_type], markersize=10, marker='o', label=label, zorder=3)
        amenity_legend_handles.append(Line2D([0], [0], marker='o', color='w', markerfacecolor=amenity_colors[amenity_type], markersize=10, label=label))

# Plot the center point as a distinct star marker
point_gdf.plot(ax=ax, color='red', marker='*', markersize=100, zorder=4)

# Customize the legend
landuse_legend = ax.get_legend()
landuse_legend.set_title('Land Use Types')

# Add legend for urban amenities
ax.legend(handles=amenity_legend_handles, loc='upper right')

# Set title and axis labels
ax.set_title('Land Use Map')
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')

# Set axis limits
ax.set_xlim(west, east)
ax.set_ylim(south, north)

# Hide axis
ax.axis('off')

# Show the map
plt.show()
