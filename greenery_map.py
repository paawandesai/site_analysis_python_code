import osmnx as ox
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point, box
from matplotlib.lines import Line2D

# Define the center point and distance for the area of interest
point = (30.28846032303379, -97.73536240661028)
dist = 1000  # Distance in meters from the point

# Get the bounding box
north, south, east, west = ox.utils_geo.bbox_from_point(point, dist=dist)

# Get green spaces, parks, water bodies, and building footprints
nature_tags = {'natural': ['water', 'wood', 'tree', 'scrub', 'wetland', 'grassland', 'fell']}
buildings_gdf = ox.geometries.geometries_from_bbox(north, south, east, west, tags={'building': True})
nature_gdf = ox.geometries.geometries_from_bbox(north, south, east, west, tags=nature_tags)

# Create a GeoDataFrame for the center point
point_gdf = gpd.GeoDataFrame(geometry=[Point(point[1], point[0])], crs='EPSG:4326')

# Plotting the map
fig, ax = plt.subplots(figsize=(15, 15))

if not buildings_gdf.empty:
    buildings_gdf.plot(ax=ax, color='grey', alpha=0.7, zorder=2)
if not nature_gdf.empty:
    nature_gdf.plot(ax=ax, color='green', alpha=0.7, zorder=3)

# Plot the center point as a distinct star marker
point_gdf.plot(ax=ax, color='red', marker='*', markersize=100, zorder=4)

# Customize the legend
building_legend = Line2D([0], [0], marker='o', color='w', markerfacecolor='grey', markersize=10, label='Building Footprints')
green_legend = Line2D([0], [0], marker='o', color='w', markerfacecolor='green', markersize=10, label='Green Spaces')
star_legend = Line2D([0], [0], marker='*', color='w', markerfacecolor='red', markersize=15, label='Exact Location')

# Add legend
ax.legend(handles=[building_legend, green_legend, star_legend], loc='upper right')

# Set title and axis labels
ax.set_title('Greenery/Building Footprint Map')
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')

# Set axis limits
ax.set_xlim(west, east)
ax.set_ylim(south, north)

# Hide axis
ax.axis('off')

# Show the map
plt.show()
