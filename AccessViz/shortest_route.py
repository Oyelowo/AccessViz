# -*- coding: utf-8 -*-
"""
Created on Fri Dec 29 23:41:01 2017

@author: oyeda
"""

#(option 3). AccessViz can also visualize shortest path routes (walking, cycling, 
#and/or driving) using OpenStreetMap data from Helsinki Region. The impedance value 
#for the routes can be distance (as was shown in Lesson 7) or time (optional for 
#the most advanced students). This functionality can also be a separate program 
#(it is not required to bundle include this with the rest of the AccessViz tool)

from problem1 import lowo, zip2shp
from visualise_tt import visual
from problem4 import visual_comp

import geopandas as gpd
import pandas as pd
import zipfile


import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, LineString, Polygon
import osmnx as ox
import networkx as nx
from shapely.geometry import box
import folium
#fp= "http://blogs.helsinki.fi/accessibility/helsinki-region-travel-time-matrix-2015/"
fp=r"C:\Users\oyeda\Desktop\AUTOGIS\FINAL_ASSIGNMENT"
data_zip = zipfile.ZipFile((fp+"\HelsinkiRegion_TravelTimeMatrix2015.zip"), "r")
access_grid_fp=r"C:\Users\oyeda\Desktop\AUTOGIS\FINAL_ASSIGNMENT\MetropAccess_YKR_grid\MetropAccess_YKR_grid_EurefFIN.shp"
access_gridUTM= gpd.read_file(access_grid_fp)

#original projection of the grid was UTM i.e 
#{'ellps': 'GRS80', 'no_defs': True, 'proj': 'utm', 'units': 'm', 'zone': 35}
#and I decided to change to {'init': 'epsg:4326'} which is the original projection of 
#osmnx
#Although, I could import the polygon directly from placename "Helsinki", I decided to 
#first convert to lat_lon(which osmnx graph uses to import polygon), so, i can expand the network a bit by creating a buffer around the bounding box 
#and then using that to import the edges/roads and I can also use folium map to
#get the location of the grids.
#access_gridUTM=access_gridUTM[access_gridUTM.YKR_ID.isin([5785642,6015143])]
access_gridUTM.crs
access_grid= access_gridUTM.copy()

#convert crs
access_grid=access_grid.to_crs({'init': 'epsg:4326'})



#find the bounding box
access_grid.bounds
access_grid.crs

#this creates like a somewhat polygon which is the bounding box geometry
bbox_access = box(*access_grid.unary_union.bounds)

#because some shortest routes might exist a bit outside the bounding box of Helsinki,
#it is a good idea to create a little buffer around the bounding box
bbox_buf=bbox_access.buffer(0.05)

#check for the area
bbox_access.area
bbox_access.representative_point

bbox_buf
# Create a Map instance from the bounding box's centroid
m = folium.Map(location=(bbox_access.centroid.y, bbox_access.centroid.x), tiles='Stamen Toner',
                   zoom_start=11, control_scale=True , prefer_canvas=True)
m.save(fp+ "/visualise" + "/area_of_interest.html")

#network_types, walking, cycling, and/or driving
#network_type="walk", "bike", "drive"
graph_access= ox.graph_from_polygon(bbox_buf, network_type="drive")
#graph_try= ox.graph_from_polygon('Helsinki', network_type="drive")
# =============================================================================
#alternative is to import from Helsinki right away
# graph= ox.graph_from_polygon("Helsinki", network_type="drive")
# type(graph)
# 
# ox.plot_graph(graph)
# nodes_not_repro = ox.graph_to_gdfs(graph, edges=False)
# 
# nodes_not_repro.crs
# =============================================================================

#ox.plot_graph(graph_access)

#reproject from lat_long to UTM
graph_proj =ox.project_graph(graph_access)


nodes_proj, edges_proj = ox.graph_to_gdfs(graph_proj, nodes=True, edges=True)
#nodes_proj, edges_proj = ox.graph_to_gdfs(graph_proj, edges=True)
nodes_proj[['x', 'y']]
nodes_proj.crs

#find the centroid of each grid. Now,I am using the original grid shapefle because
#it has already been projected to UTM format which can now be used for finding
#the shortest route alongside the reprojected graph_access.
access_gridUTM['centroid_grids']=access_gridUTM["geometry"].centroid
#These centroids will serve as representative point of each grid

#select only the area of interest with the origin and destination
access_gridUTM=access_gridUTM[access_gridUTM.YKR_ID.isin([5785642,6015143])]

#find the nearest node of each of the centroid and the distance of the centroid to the nearest node..
grid_nodes=[]
distance=[]
for i,rows in access_gridUTM.iterrows():
    print(i)
    #get the distance of the points to the nodes too. but without returning the distance
    #one object could be specified to avoid getting the nodes as list of nodes and distance of
    #points to nodes too. but here, i want to return the nearest nodes and the distance of points
    #to the nearest nodes
    yx, dist=ox.get_nearest_node(graph_proj, (rows.centroid_grids.y, rows.centroid_grids.x), method='euclidean', return_dist=True)
    grid_nodes.append(yx)
    distance.append(dist)
    
access_gridUTM['grid_nodes']=grid_nodes
access_gridUTM['dist_grid_node'] = distance
    
access_gridUTM.columns

#    5787546, 5785642

orig_node=access_gridUTM.loc[access_gridUTM['YKR_ID']== 5785642, 'grid_nodes'].values[0]
orig_loc=access_gridUTM.loc[access_gridUTM['YKR_ID']== 5785642, 'centroid_grids'].values[0]
origin=gpd.GeoDataFrame()
origin["geometry"]=''
origin.loc[1, "geometry"]=orig_loc
origin=gpd.GeoDataFrame(origin, geometry='geometry', crs=nodes_proj.crs)

origin.crs

dest_node=access_gridUTM.loc[access_gridUTM['YKR_ID']== 6015143, 'grid_nodes'].values[0]
dest_loc=access_gridUTM.loc[access_gridUTM['YKR_ID']== 6015143, 'centroid_grids'].values[0]
destination=gpd.GeoDataFrame()
destination["geometry"]=''
destination.loc[1, "geometry"]=dest_loc
destination=gpd.GeoDataFrame(destination, geometry='geometry', crs=nodes_proj.crs)

destination.crs

#find the shortest route of the node to the node of the destination grid.
route = nx.shortest_path(G=graph_proj, source=orig_node, target=dest_node, weight='distance')
  

#I could leverage on the fact that the indexes of the nodes dataframe are the osm id
#if not, i could also set the nodes id as the index. This selects the nodes in the route
#and  selects their geometries.
line=LineString(list(nodes_proj.loc[route].geometry.values))
distance_line=line.length      

line_geom=gpd.GeoDataFrame()
line_geom['route']= ''
line_geom.loc[1, 'route']=line

line_geom=gpd.GeoDataFrame(line_geom, geometry='route', crs=nodes_proj.crs)
line_geom.crs

fig, ax = ox.plot_graph(graph_proj, node_alpha=0)
line_geom.plot(ax=ax, color='red')
#line_geom.plot(ax=ax, color='green')

origin.plot(ax=ax, color="green", linewidth=0.3, zorder=10)

#add the destination nodes
destination.plot(ax=ax, color="blue", linewidth=0.3, zorder=10)
#dest_proj.plot(ax=ax, markersize=24, color='blue')'

plt.title("Shortest Route analysis")

plt.tight_layout()
plt.savefig(fp + '\shortest_paths.png')

