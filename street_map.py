import osmnx as ox
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D

# Step 1: Downloading Street Networks
location = (30.28846032303379, -97.73536240661028)
distance = 1000 # Distance in meters from the point

# Download street network data from OSM and construct a MultiDiGraph model
G = ox.graph.graph_from_point(location, dist=distance, network_type='all')

# Impute edge (driving) speeds and calculate edge travel times
G = ox.speed.add_edge_speeds(G)
G = ox.speed.add_edge_travel_times(G)

# Get edge speeds and travel times as arrays
speeds = np.array([data['speed_kph'] for u, v, key, data in G.edges(keys=True, data=True)])
travel_times = np.array([data['travel_time'] for u, v, key, data in G.edges(keys=True, data=True)])

# Define colormap for speeds and travel times
speed_cmap = plt.cm.get_cmap('YlOrRd')
time_cmap = plt.cm.get_cmap('Blues')

# Normalize speeds and travel times
min_speed, max_speed = speeds.min(), speeds.max()
min_time, max_time = travel_times.min(), travel_times.max()

# Assign colors to edges based on speeds and travel times
speed_colors = [speed_cmap((speed - min_speed) / (max_speed - min_speed)) for speed in speeds]
time_colors = [time_cmap((time - min_time) / (max_time - min_time)) for time in travel_times]

# Plot the graph with the edge colors
fig, ax = ox.plot_graph(G, bgcolor='w', node_size=0, edge_color=speed_colors, edge_linewidth=0.5, show=False)

# Plot additional features
# Traffic volume
ox.plot.plot_graph(G, ax=ax, bgcolor='w', node_size=0, edge_color='orange', edge_linewidth=0.5, edge_alpha=0.5, show=False)

# Transit stops
transit_stops = ox.geometries.geometries_from_point(location, tags={'highway': 'bus_stop'}, dist=distance)
transit_stops.plot(ax=ax, color='blue', markersize=5)

# Pedestrian walkways
pedestrian_walkways = ox.geometries.geometries_from_point(location, tags={'highway': 'footway'}, dist=distance)
pedestrian_walkways.plot(ax=ax, color='green', linewidth=1)

# Bike lanes
bike_lanes = ox.geometries.geometries_from_point(location, tags={'highway': 'cycleway'}, dist=distance)
bike_lanes.plot(ax=ax, color='red', linewidth=1)

# Other modes of transportation infrastructure (e.g., railway)
other_infrastructure = ox.geometries.geometries_from_point(location, tags={'railway': True}, dist=distance)
other_infrastructure.plot(ax=ax, color='purple', linewidth=1)

# Plot for exact latitude and longitude
ax.plot(location[1], location[0], marker='*', color='red', markersize=15, label='Exact Location')

# Create legend
legend_elements = [
    Line2D([0], [0], color='blue', lw=2, label='Transit Stops'),
    Line2D([0], [0], color='green', lw=2, label='Pedestrian Walkways'),
    Line2D([0], [0], color='red', lw=2, label='Bike Lanes'),
    Line2D([0], [0], color='purple', lw=2, label='Railway')
]
ax.legend(handles=legend_elements)


# Show the plot
plt.show()