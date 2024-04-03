import osmnx as ox
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point, box
from matplotlib.lines import Line2D

point = (30.28846032303379, -97.73536240661028)
dist = 1000  # Distance in meters from the point

# Get the bounding box
north, south, east, west = ox.utils_geo.bbox_from_point(point, dist=dist)

# Get street network, buildings, and nature areas
G = ox.graph.graph_from_bbox(north, south, east, west, network_type='all', simplify=False)
buildings_gdf = ox.geometries.geometries_from_bbox(north, south, east, west, tags={'building': True})

nature_tags = {'leisure': ['park', 'garden'], 'landuse': ['grass', 'forest', 'recreation_ground', 'meadow']}
nature_gdf = ox.geometries.geometries_from_bbox(north, south, east, west, tags=nature_tags)

infrastructure_tags = {'amenity': ['parking', 'parking_space', 'garage', 'parking_lot']}
infrastructure_gdf = ox.geometries.geometries_from_bbox(north, south, east, west, tags=infrastructure_tags)

# Function to standardize plots
def standardize_plot(ax, gdf, color, title, xlim, ylim):
    if not gdf.empty:
        gdf.plot(ax=ax, color=color, zorder=2)
    ax.set_title(title)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.axis('off')

# Standardized axis limits
xlim = (west, east)
ylim = (south, north)
figsize = (15, 15)

# Function to plot each layer separately
def plot_layer(gdf, color, title, point):
    fig, ax = plt.subplots(figsize=figsize)
    standardize_plot(ax, gdf, color, title, xlim, ylim)
    ax.scatter(point[1], point[0], marker='*', color='red', s=100, zorder=3)  # Add star marker for exact lat/long
    plt.show()

# # Display each layer
# plot_layer(buildings_gdf, 'black', 'Building Footprints', point)
# plot_layer(nature_gdf, 'green', 'Nature Areas', point)
# plot_layer(infrastructure_gdf, 'darkgrey', 'Additional Infrastructure', point)

# Combined Map
fig, ax = plt.subplots(figsize=figsize)

if not buildings_gdf.empty:
    buildings_gdf.plot(ax=ax, color='black', zorder=5)
if not nature_gdf.empty:
    nature_gdf.plot(ax=ax, color='green', alpha=0.7, zorder=4)
if not infrastructure_gdf.empty:
    infrastructure_gdf.plot(ax=ax, color='darkgrey', alpha=0.7, zorder=3)
ax.scatter(point[1], point[0], marker='*', color='red', s=100, zorder=6)  # Add star marker for exact lat/long
ax.set_xlim(*xlim)
ax.set_ylim(*ylim)
ax.set_title('Combined Map')
ax.axis('off')
plt.show()
