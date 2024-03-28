import osmnx as ox
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import box


point = (30.28846032303379, -97.73536240661028)

dist = 1000 # Distance in meters from the point

# Get the bounding box
north, south, east, west = ox.utils_geo.bbox_from_point(point, dist=dist)

# Get street network, buildings, and nature areas
G = ox.graph_from_bbox(north, south, east, west, network_type='all', simplify=False)
buildings_gdf = ox.features_from_bbox(north, south, east, west, tags={'building': True})


# Nature and infrastructure areas
nature_tags = {'leisure': ['park', 'garden'], 'landuse': ['grass', 'forest', 'recreation_ground', 'meadow']}
infrastructure_tags = {'amenity': ['parking', 'parking_space', 'garage', 'parking_lot']}


try:
    nature_gdf = ox.features_from_bbox(north, south, east, west, tags=nature_tags)
except Exception:
    nature_gdf = gpd.GeoDataFrame()

try:
    infrastructure_gdf = ox.features_from_bbox(north, south, east, west, tags=infrastructure_tags)
except Exception:
    infrastructure_gdf = gpd.GeoDataFrame()

# Streets as areas with varying width and straight cap
streets_gdf = ox.graph_to_gdfs(G, nodes=False, edges=True)
streets_gdf = streets_gdf.to_crs(epsg=3857)  # Project to Web Mercator
width_map = {'primary': 10, 'secondary': 8, 'tertiary': 6, 'residential': 4, 'unclassified': 2}
streets_gdf['width'] = streets_gdf['highway'].map(width_map).fillna(2) * 2  # Width in meters
streets_gdf['geometry'] = streets_gdf.geometry.buffer(streets_gdf['width'], cap_style=2)  # Straight cap
streets_gdf = streets_gdf.to_crs(epsg=4326)  # Reproject back to WGS84

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

# Plotting each map in separate figures
def plot_layer(gdf, color, title):
    fig, ax = plt.subplots(figsize=figsize)
    standardize_plot(ax, gdf, color, title, xlim, ylim)
    plt.show()

# Display each layer
plot_layer(buildings_gdf, 'black', 'Building Footprints')
plot_layer(streets_gdf, 'grey', 'Streets')
plot_layer(nature_gdf, 'green', 'Nature Areas')
plot_layer(infrastructure_gdf, 'darkgrey', 'Additional Infrastructure')

# Combined Map
fig, ax = plt.subplots(figsize=figsize)
if not streets_gdf.empty:
    streets_gdf.plot(ax=ax, color='grey', alpha=1, zorder=2)
if not infrastructure_gdf.empty:
    infrastructure_gdf.plot(ax=ax, color='darkgrey', alpha=1, zorder=3)
if not nature_gdf.empty:
    nature_gdf.plot(ax=ax, color='green', alpha=1, zorder=4)
if not buildings_gdf.empty:
    buildings_gdf.plot(ax=ax, color='black', zorder=5)
ax.set_xlim(*xlim)
ax.set_ylim(*ylim)
ax.set_title('Combined Map')
ax.axis('off')
plt.show()

# Calculate total area of the bounding box in square meters
bbox = box(west, south, east, north)
bbox_gdf = gpd.GeoDataFrame(geometry=[bbox], crs='EPSG:4326')
bbox_gdf = bbox_gdf.to_crs(epsg=3857)
bbox_area = bbox_gdf.geometry.area.iloc[0]

# Function to calculate SCR
def calculate_scr(gdf, bbox_area):
    gdf_projected = gdf.to_crs(epsg=3857)
    total_feature_area = gdf_projected.geometry.area.sum()
    scr = total_feature_area / bbox_area
    return scr

# Get data for buildings, streets, nature areas, and infrastructure
G = ox.graph_from_bbox(north, south, east, west, network_type='all', simplify=False)
buildings_gdf = ox.features_from_bbox(north, south, east, west, tags={'building': True})
nature_tags = {'leisure': ['park', 'garden'], 'landuse': ['grass', 'forest', 'recreation_ground', 'meadow']}
nature_gdf = ox.features_from_bbox(north, south, east, west, tags=nature_tags)

# Process streets as areas
streets_gdf = ox.graph_to_gdfs(G, nodes=False, edges=True)
street_widths = {'primary': 8, 'secondary': 6, 'tertiary': 4, 'residential': 2, 'unclassified': 2}
streets_gdf['width'] = streets_gdf['highway'].map(street_widths).fillna(3)
streets_gdf = streets_gdf.to_crs(epsg=3857)
streets_gdf['geometry'] = streets_gdf.geometry.buffer(streets_gdf['width'] / 2)  # Buffer in meters

# Calculate SCR for each category
scr_buildings = calculate_scr(buildings_gdf, bbox_area)
scr_streets = calculate_scr(streets_gdf, bbox_area)
scr_nature = calculate_scr(nature_gdf, bbox_area)

# Print SCR values
print(f"Site Coverage Ratio for Building Footprints: {scr_buildings:.2%}")
print(f"Site Coverage Ratio for Streets: {scr_streets:.2%}")
print(f"Site Coverage Ratio for Nature Areas: {scr_nature:.2%}")
