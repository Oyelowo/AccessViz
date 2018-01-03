# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 17:54:06 2017

@author: oyeda
"""

# =============================================================================
# 4. AccessViz can also compare travel times or travel distances between two 
# different travel modes (more than two travel modes are not allowed). Thus IF 
# the user has specified two travel modes (passed in as a list) for the AccessViz, 
# the tool will calculate the time/distance difference of those travel modes into 
# a new data column that should be created in the Shapefile. The logic of the 
# calculation is following the order of the items passed on the list where first 
# travel mode is always subtracted by the last one: travelmode1 - travelmode2. 
# The tool should ensure that distances are not compared to travel times and vice 
# versa. If the user chooses to compare travel modes to each other, you should 
# add the travel modes to the filename such as Accessibility_5797076_pt_vs_car.shp. 
# If the user has not specified any travel modes, the tool should only create the 
# Shapefile but not execute any calculations. It should be only possible to compare 
# two travel modes between each other at the time. Accepted travel modes are the 
# same ones that are found in the actual TravelTimeMatrix file (pt_r_tt, car_t, etc.). 
# If the user specifies something else, stop the program, and give advice what are 
# the acceptable values.
# =============================================================================


from bokeh.palettes import YlOrRd6 as palette

from bokeh.plotting import figure, save
#from bokeh.io import show
#from bokeh.layouts import column, row
#from bokeh.models import Div
from bokeh.io import output_file, show
from bokeh.models import Title
from bokeh.models import ColumnDataSource, HoverTool, LogColorMapper, GeoJSONDataSource

from bokeh.palettes import RdYlGn10 as palette5
from shapely.geometry import Point

import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib import legend
import pysal as ps

import numpy as np
import pandas as pd
import textwrap
from get_geom import get_geom


#from bokeh.core.properties import values

#from bokeh.plotting import figure, save
#
#from bokeh.models import ColumnDataSource, HoverTool, LogColorMapper
#import bokeh.models.mappers.ColorMapper
from bokeh.models.mappers import CategoricalColorMapper, ContinuousColorMapper,LinearColorMapper
#import bokeh.sampledata
#bokeh.sampledata.download()

#from bokeh.palettes import RdYlGn10 as palette
from bokeh.palettes import RdYlGn11 as palette2
from bokeh.palettes import BrBG10 as palette3
from bokeh.palettes import RdYlGn9 as palette4


class AccessVizError(Exception):
    """Base class for exceptions in this AccessViz module."""
    pass

class visual_comp:
    def vis_compare(data_zip,userinput, filepath, grid_shp, compare_mod=[], visualisation=True, map_type='interactive', destination_style='grid',        
            classification='pysal_class', class_type="Quantiles", n_classes=8,
            multiples=[-2, -1, 1, 2],  pct=0.1, hinge=1.5, truncate=True, pct_classes=[1,10,50,90,99,100],
            class_lower_limit="", class_upper_limit="", class_step="", label_lower_limit="", label_upper_limit="", label_step=""):

            
            namelist=data_zip.namelist()
            m_list=[]
            #iterate over the userinput, to get all its element/values
            for element in userinput:
                #concatenate the input with the standard names of the file
                element_file=("HelsinkiRegion_TravelTimeMatrix2015/"+str(element)[0:4]+"xxx/travel_times_to_ "+ str(element) + ".txt")
                #now, check if the file is in not namelist of all the files in the ziped folder.
                #if it is not, give the warning
                if element_file not in namelist:
                    print("WARNING: The specified matrix {0} is not available".format(element))
                    print("\n")
                else:
                    print("Matrix {0} is available".format(element))
                    m_list.append(element)
                                        #check for the progress
                    print("Processing file travel_times_to_{0}.txt.. Progress: {1}/{2}".format(element,len([i for i in range(len(m_list))]), len(userinput)))
                    
                    #The above can also simply be done as below
                    #slice the string. This is used for the following step, just
                    #to know which of the matrix is presently being extracted.
                    #f_slice=filename[44:]
                    #print("processing file {0}.. Progress: {1}/{2}".format(f_slice,len([i for i in range(len(m_list))]), len(m_list)))
                        
                    bytes = data_zip.read(element_file)
                        #print the file size
                    print('has',len(bytes),'bytes')
                    print("\n")
                        
                    tt_matrices= pd.read_csv(element_file, sep=";")
                    
                    column_list=[i for i in tt_matrices.columns]
                    
                    absent_col= [i for i in compare_mod if i not in column_list]
                    #find if any of the items of the listed transport modes is/are not column(s) in the matrix dataframe
                    if any(x not in column_list for x in compare_mod):
                        if len(absent_col)==1:
                            raise AccessVizError("The specified travel mode", str(absent_col).strip('[]'), "is not available. Accepted travel modes include:", str([i for i in tt_matrices.columns][2:]).strip('[]'))
#                            break
                        elif len(absent_col)>1:
                            raise AccessVizError("The specified travel modes:", str(absent_col).strip('[]'), ", are not available. Accepted travel modes include:", str([i for i in tt_matrices.columns][2:]).strip('[]'))
#                            break
                    else:
                        if len(compare_mod)> 2:
                    #userinput= [int(x) for x in input("list the ID-numbers you want to read and separate each by a comma(,): ").split(',')]
                            raise AccessVizError("WARNING: More than two travel modes are not allowed. Specify only two similar travel modes(i.e either distance or time but not both at thesame time)")
    #                            break
                        elif len(compare_mod)==2:
                            if compare_mod[0]==compare_mod[1]:
                                raise AccessVizError("WARNING: You are comparing the same travel modes\n")
    #                            break
                            elif compare_mod[0][-1] != compare_mod[1][-1]:
                                raise AccessVizError("WARNING!:You cannot compare Travel Distance with Travel Time!!!\n")
    #                            break
                        elif len(compare_mod)==1:
                                raise AccessVizError("WARNING: You have specified just one travel mode. \n One travel mode is not allowed. \n Specify two travel modes in the list")
    #                            break
                       
                          
                        
                    #This is done to handle matrices with nodata at all. e.g: matrix"6016696"
                    if tt_matrices['to_id'].max()==-1:
                        print('The MATRIX- {0} is empty and has nodata'.format(element))
                        print('\n')
                    else:
                        merged_metro = pd.merge(grid_shp,tt_matrices,  left_on="YKR_ID", right_on="from_id")
                        
                        #check if list is empty.
                        if not compare_mod:
                          merged_metro.to_file(driver = 'ESRI Shapefile', filename= filepath+"/travel_times_to_" + str(element) + ".shp")
                    
                        else:
                            mode1=compare_mod[0]; mode2=compare_mod[1]
                            tt_col=mode1+'_vs_' + mode2
                            
                            #Next I will calculate the difference but be mindful of the empty grids.
                            #when either or both of the modes is/are empty, the resultant difference
                            #should be nodata(i.e -1)
                            #create an empty column to imput the mode difference
                            merged_metro[tt_col]=""
                            mode1_vs_mode2=[]
                            for idx, rows in merged_metro.iterrows():
                                if rows[mode1]==-1 or rows[mode2]==-1:
                                    difference=-1
                                    mode1_vs_mode2.append(difference)
                                else:
                                    difference= rows[mode1]-rows[mode2]
                                    mode1_vs_mode2.append(difference)
                            merged_metro[tt_col]=mode1_vs_mode2
                            
# =============================================================================
#                            alternative
#                             mode1_vs_mode2=[]
#                             for i in range(len(data)):
#                                 print(i)
#                                 if data.loc[i, "pt_r_tt"]!=-1 or data.loc[i,"car_r_t"]!=-1:
#                                     dat= data["pt_r_tt"] - data["car_r_t"]
#                                     mode1_vs_mode2.append(dat)
#                                 elif data.loc[i, "pt_r_tt"]==-1 or data.loc[i,"car_r_t"]==-1:
#                                     dat=-1
#                                     mode1_vs_mode2.append(dat)
#                             data["pt_diff_car_tt"] = mode1_vs_mode2
# =============================================================================
             
                            
                            #now, export the result
                            merged_metro.to_file(driver = 'ESRI Shapefile', filename= filepath+"/travel_times_to_" + tt_col + "_" +str(element) + ".shp")
                            
                            
                            if visualisation==True:
                                #However, for the visualisation, there is need to exclude the nodata grids with -1
                                merged_metro= merged_metro.loc[merged_metro[ tt_col]!=-1]

                            
                                 #Calculate the x and y coordinates of the grid.
                                merged_metro['x'] = merged_metro.apply(get_geom.getCoords, geom_col="geometry", coord_type="x", axis=1)
                    
                                merged_metro['y'] = merged_metro.apply(get_geom.getCoords, geom_col="geometry", coord_type="y", axis=1)
                            
                           
                                if classification =='pysal_class':
                                    if class_type == "Natural_Breaks":
                                        classifier = ps.Natural_Breaks.make(k=n_classes)
                                    elif class_type == "Equal_Interval":
                                        classifier = ps.Equal_Interval.make(k=n_classes)
                                    elif class_type == "Box_Plot":
                                        classifier = ps.Box_Plot.make(hinge)
                                    elif class_type == "Fisher_Jenks":
                                        classifier = ps.Fisher_Jenks.make(k=n_classes)
                    #                elif class_type == "Fisher_Jenks_Sampled":
                    #                    classifier = ps.Fisher_Jenks_Sampled.make(k=n_classes, pct=0.1)
                                    elif class_type == "HeadTail_Breaks":
                                        classifier = ps.HeadTail_Breaks.make(k=n_classes)
                                    elif class_type == "Jenks_Caspall":
                                        classifier = ps.Jenks_Caspall.make(k=n_classes)
                                    elif class_type == "Jenks_Caspall_Forced":
                                        classifier = ps.Jenks_Caspall_Forced.make(k=n_classes)
                                    elif class_type == "Quantiles":
                                        classifier = ps.Quantiles.make(k=n_classes)
                                    elif class_type == "Percentiles":
                                        classifier = ps.Percentiles.make(pct_classes)
                                    elif class_type == "Std_Mean":
                                        classifier = ps.Std_Mean.make(multiples)
                                    mode_classif = merged_metro[[tt_col]].apply(classifier)
                                   
                                    
                                    #Rename the columns of our classified columns.
                                    mode_classif.columns = [tt_col+"_ud"]
                                    
                                    
                                    #Join the classes back to the main data.
                                    merged_metro = merged_metro.join(mode_classif)
                                    
                                        
                                    merged_metro['label_' + tt_col ] = mode_classif
                                        
                                    
                                
                                elif classification == "User_Defined":
                                     #Next, we want to classify the travel times with 5 minute intervals until 200 minutes.
                    
                                    #Let’s create a list of values where minumum value is 5, maximum value is 200 and step is 5.
                                    breaks = [x for x in range(class_lower_limit, class_upper_limit, class_step)]
                                    #Now we can create a pysal User_Defined classifier and classify our travel time values.
                                
                                    classifier = ps.User_Defined.make(bins=breaks)
                                
                                    #walk_classif = data[['walk_t']].apply(classifier)
                                    
                                    mode_classif = merged_metro[[tt_col]].apply(classifier)
                                    
                                    
                                    #Rename the columns of our classified columns.
                                    mode_classif.columns = [tt_col+"_ud"]
                                    #walk_classif.columns = ['walk_t_ud']
                                    
                                    #Join the classes back to the main data.
                                    merged_metro = merged_metro.join(mode_classif)
                                    #data = data.join(walk_classif)
                                    #Create names for the legend (until 60 minutes). The following will produce: ["0-5", "5-10", "10-15", ... , "60 <"].
            #                        
                                    names = ["%s-%s" % (x-label_step, x) for x in range(label_lower_limit, label_upper_limit, label_step)]
                                    #         ["{0}kk{1}".format(x-5,x) for x in range(5, 200, 5)]   #alternative
                                    
                                    #Add legend label for over 60.
                                    names.append("%s<" % label_upper_limit)
                                    #Assign legend names for the classes.
                                    #data['label_wt'] = None
                                    
                                    merged_metro['label_' + tt_col ] = None
                                    
                                    #Update rows with the class-names.
                                    
                                    for i in range(len(names)):
                                        merged_metro.loc[merged_metro[tt_col+"_ud"] == i, 'label_' + tt_col] = names[i]
                                       
                                    #Update all cells that didn’t get any value with "60 <"
                                    #data['label_wt'] = data['label_wt'].fillna("%s <" % upper_limit)
                                    
                                    merged_metro['label_' + tt_col] = merged_metro['label_' + tt_col].fillna("%s<" % label_upper_limit)
                                    
                                #Finally, we can visualize our layers with Bokeh, add a legend for travel times 
                                #and add HoverTools for Destination Point and the grid values (travel times).
                                # Select only necessary columns for our plotting to keep the amount of data minumum
                                #df = data[['x', 'y', 'walk_t','walk_t_ud', 'car_r_t','car_r_t_ud', 'from_id', 'label_wt', "label_car"]]
                                df = merged_metro[['x', 'y',"YKR_ID",mode1,mode2, tt_col,tt_col+"_ud","from_id" ,'label_' + tt_col]]
                                dfsource = ColumnDataSource(data=df)
                                
                                df_dest_id= df.loc[df['YKR_ID']==element]
                                dfsource_dest_id = ColumnDataSource(data=df_dest_id)
                                # Specify the tools that we want to use
                                TOOLS = "pan,wheel_zoom,box_zoom,reset,save"
                                
                                # Flip the colors in color palette
                                palette2.reverse()
                                color_mapper = LogColorMapper(palette=palette2)
                                #color_mapper = ContinuousColorMapper(palette=palette4)
                                
                                
                                
                             #This part is for automating the title
                                
                                list_of_titles = ["walk_t: Travel time in minutes from origin to destination by walking",
                                                  "walk_d: Distance in meters of the walking route",
                                                "pt_r_tt: Travel time in minutes from origin to destination by public transportation in rush hour traffic(including waiting time at home)", 
                                                "pt_r_t: Travel time in minutes from origin to destination by public transportation in rush hour traffic(excluding waiting time at home)",
                                                "pt_r_d: Distance in meters of the public transportation route in rush hour traffic",
                                                "pt_m_tt: Travel time in minutes to destination by public transportation in midday traffic(including waiting time at home)",
                                                "pt_m_t: Travel time in minutes from origin to destination by public transportation in midday traffic(excluding waiting time at home)",
                                                "pt_m_d: Distance in meters of the public transportation route in midday traffic",
                                                "car_r_t: Travel time in minutes from origin to destination by private car in rush hour traffic",
                                                "car_r_d: Distance in meters of the private car route in rush hour traffic",
                                                "car_m_t: Travel time in minutes from origin to destination by private car in midday traffic",
                                                "car_m_d: Distance in meters of the private car route in midday traffic"]
                                                                    
                                title_mod1=list_of_titles[tt_matrices.columns.get_loc(mode1) - 2]
                                title_mod2=list_of_titles[tt_matrices.columns.get_loc(mode2) - 2]
                                index=title_mod1.find('destination')
                                title_mat=title_mod1[:index+len('destination')] + ' ' + str(element) +  title_mod1[index+len('destination'):]
                                index_mode1 = title_mat.find(mode1 + str(':'))
                                   
                                if 'destination' in title_mod1:
                                     if mode2[:2]=='pt':
                                        title_matrix=  title_mat[:index_mode1 + len(mode1)] + ' vs ' + mode2 + (': Difference between'+  title_mat[index_mode1 + len(mode1)+1:] + ' vs ' + title_mod2[title_mod2.find('public'):]).title() 
                                     elif mode2[:4]=='walk':
                                        title_matrix=  title_mat[:index_mode1 + len(mode1)] + ' vs ' + mode2 + (': Difference between'+  title_mat[index_mode1 + len(mode1)+1:] + ' vs ' + title_mod2[title_mod2.find('walking'):]).title()
                                     elif mode2[:3]=="car":
                                        title_matrix=  title_mat[:index_mode1 + len(mode1)] + ' vs ' + mode2 + (': Difference between'+  title_mat[index_mode1 + len(mode1)+1:] + ' vs ' + title_mod2[title_mod2.find('private'):]).title() 
                                        
                                            
                                
                                #here, for the title. i got the location of the specified travel mode(tt_col), then, with its
                    #                    with its index, i got the corresponsding location in the list which was arranged according to the
                    #                    to the columns of the dataframe(tt_matrices) too. 2 is subracted(i.e -2) because, the list_of_titles
                    #                    is shorter by 2, as it does not include from_id or to_id which are not variables of interest here but the travel modes only.
                    
                                elif 'Distance' in title_mod1: 
                                    title_mat=title_mod1 + ' to ' + str(element) 
                                    if mode2[:2]=='pt':
                                        title_matrix=  title_mat[:index_mode1 + len(mode1)] + ' vs ' + mode2 + (': Difference between'+  title_mat[index_mode1 + len(mode1)+1:] + ' vs ' + title_mod2[title_mod2.find('public'):]).title() 
                                    elif mode2[:4]=='walk':
                                        title_matrix=  title_mat[:index_mode1 + len(mode1)] + ' vs ' + mode2 + (': Difference between'+   title_mat[index_mode1 + len(mode1)+1:] + ' vs ' + title_mod2[title_mod2.find('walking'):]).title() 
                                    elif mode2[:3]=="car":
                                        title_matrix=  title_mat[:index_mode1 + len(mode1)] + ' vs ' + mode2 + (': Difference between'+  title_mat[index_mode1 + len(mode1)+1:] + ' vs ' + title_mod2[title_mod2.find('private'):]).title() 
                                        
                                    
                                   
                                
                                if map_type=='interactive':
                                
                                    
                                    p = figure(title=tt_col, tools=TOOLS,
                                                 plot_width=850, plot_height=650, active_scroll = "wheel_zoom" )
                                 
                                    
                                    #p.title.text=title_matrix
                                    p.title.text_color = "blue"
                                    p.title.text_font = "times"
                                    p.title.text_font_style = "italic"
                                    p.title.text_font_size='20px'
                                    p.title.offset=-5.0
                                    
                                    p.add_layout(Title(text=title_matrix[len(tt_col)+1:][211:], text_font_size="11pt", text_font_style="bold"), 'above')   #sub
                                    p.add_layout(Title(text=title_matrix[len(tt_col)+1:][102:211], text_font_size="11pt", text_font_style="bold"), 'above')    #sub
                                    p.add_layout(Title(text=title_matrix[len(tt_col)+1:][:102], text_font_size="11pt",text_font_style="bold"),'above')       #main
                                   
                         #                    This can be used if you want a more generalised title
                        #                    differentiating just travel times and distances and not the meanas.
                        #                    if tt_col[-1]== 't':
                        #                        p = figure(title="Travel times to The Grid", tools=TOOLS,
                        #                               plot_width=800, plot_height=650, active_scroll = "wheel_zoom" )
                        #                    elif tt_col[-1]== 'd':
                        #                        p = figure(title="Travel distances to The Grid", tools=TOOLS,
                        #                               plot_width=800, plot_height=650, active_scroll = "wheel_zoom" )
                        #                   
                                    
                                    # Do not add grid line
                                    p.grid.grid_line_color = None
                                    
                                    # Add polygon grid and a legend for it
                                    grid = p.patches('x', 'y', source=dfsource, name="grid",
                                             fill_color={'field': tt_col+"_ud", 'transform': color_mapper},
                                             fill_alpha=1.0, line_color="black", line_width=0.03, legend='label_' + tt_col)
                                    
                                    
                                    # Modify legend location
                                    p.legend.location = "top_right"
                                    p.legend.orientation = "vertical"
                                    
                                    ghover = HoverTool(renderers=[grid])
                                    ghover.tooltips=[("YKR-ID", "@from_id"),
                                                     (mode1, "@"+ mode1),
                                                     (mode2, "@"+ mode2),
                                                    (mode1 +" minus "+ mode2, "@" + tt_col)]  
                                    p.add_tools(ghover)
                                    
                                      # Insert a circle on top of the location(coords in EurefFIN-TM35FIN)
                                    #print(element)
                                    #because, it  is a grid, the location of each cell has about s x and 
                                    #y coordinates, hence, after finding the x for each grid, select 
                                    #one of the x and y coordinates(the third, which is the centre of each grid) from the list.
                                    #dest_grid_x = (df.loc[df["YKR_ID"]==element, 'x'].values[0])[2]
                                    #dest_grid_y =  (df.loc[df["YKR_ID"]==element, 'y'].values[0])[2]
                                    
                                    #Alternative to getting the centre of a grid:
                                    grid_centroid=merged_metro.loc[merged_metro['YKR_ID']==element, 'geometry'].values[0].centroid
                                    dest_grid_x=grid_centroid.x 
                                    dest_grid_y= grid_centroid.y
                                    
                                    if destination_style=='circle':
                                    # Add two separate hover tools for the data
                                        circle = p.circle(x=[dest_grid_x], y=[dest_grid_y], name="point", size=6, color="blue")
                                    
                                        phover = HoverTool(renderers=[circle])
                                        phover.tooltips=[("Destination Grid:", str(element))]
                                        p.add_tools(phover)
                                       
                                    elif destination_style=='grid':
                                        grid_dest_id= p.patches('x', 'y', source=dfsource_dest_id, name='grid', color='blue')
                                    
                                        ghover_dest_id = HoverTool(renderers=[grid_dest_id])
                                        ghover_dest_id.tooltips=[("DESTINATION GRID", str(element))] 
                                        p.add_tools(ghover_dest_id)
                                   
                                    
                            
                                  # Output filepath to HTML
                                   
                                    # Save the map
                                    save(p, filepath + "/" +mode1 + "_vs_" + mode2 +"_" + str(element) + ".html")
                                    
                                elif map_type=='static':
                                    
                                    
                                    my_map = merged_metro.plot(column=tt_col, linewidth=0.02, legend=True, cmap="RdYlGn", scheme=class_type, k=n_classes, alpha=0.9)
                                     # Add roads on top of the grid
                                    # (use ax parameter to define the map on top of which the second items are plotted)
                    #                roads.plot(ax=my_map, color="grey", legend=True, linewidth=1.2)
                                    
                                    # Add metro on top of the previous map
                    #                metro.plot(ax=my_map, color="yellow", legend=True, linewidth=2.0)
                                    
                                    ## Insert a circle on top of the Central Railway Station (coords in EurefFIN-TM35FIN)
                                    dest_grid_x = (df.loc[df["YKR_ID"]==element, 'x'].values[0])[2]
                                    dest_grid_y =  (df.loc[df["YKR_ID"]==element, 'y'].values[0])[2]
                      
                                    dest_grid= gpd.GeoDataFrame()
                                    
                                    dest_grid_loc = Point(dest_grid_x, dest_grid_y)
                                    dest_grid["geometry"]=""
                                    dest_grid.loc[1,"geometry"]=dest_grid_loc
                                    #r_s["geometry"]=r_s["geometry"].to_crs(crs=gridCRS)
                                    
                                    dest_grid.plot(ax=my_map, color= "blue", legend=True, linewidth=2)
                                    
                   
                                    #plt.legend(["roads", "metro line","Rautatientori"])
                                    #title_map=list_of_titles[tt_matrices.columns.get_loc(tt_col) - 2]
                                    plt.title(textwrap.fill(title_matrix, 65), fontsize=8)
                                    

                                    #north arrow in the southeastern corner
                                    my_map.text(x=df['x'].max()[2],y=df['y'].min()[2], s='N\n^', ha='center', fontsize=23, family='Courier new', rotation = 0)
                                    
                                    
                                    #move legend to avoid overlapping the map
                                    lege = my_map.get_legend()
                                    lege.set_bbox_to_anchor((1.60, 0.9))
                                    
                                    #resize the map to fit in thr legend.
                                    mapBox = my_map.get_position()
                                    my_map.set_position([mapBox.x0, mapBox.y0, mapBox.width*0.6, mapBox.height*0.9])
                                    my_map.legend(loc=2, prop={'size': 3})                
                                    
#                                    plt.show()
                                    
                                    # Save the figure as png file with resolution of 300 dpi
                                    outfp = filepath + "/" + "static_map_"+ mode1 + "_vs_" + mode2 +"_" + str(element) + ".png"
                                    plt.savefig(outfp, dpi=300)
                    
                                        
            #put into an object the inputs are not in the matrix list(i.e which of the specified is not in the zipped matrices)
            absentinput= [i for i in userinput if i not in m_list]
            
            #check if all of the imputed values does not exist
            if len(absentinput)==len(userinput):
                print("all the inputs do not exist")
                
                #check for those that are not included in the matrices
            elif any(absentinput) not in m_list:
                #warn that they do not exist
                print("WARNING: ", (str(absentinput)).strip('[]'), "are not available in the matrices")
                #check how many of them are not in the matrices
                print(len(absentinput), "of the inputs are not included in the matrices")    
                print("\n")
                                            
            merged_files=[i for i in userinput if i in m_list]
            if not compare_mod:
                if len(userinput)==1:
                    
                    print("NOTE: You have not specified the travel modes to compare, hence, the merged shapefile",str(merged_files).strip("[]"), "alone was produced")
                elif len(userinput)>1:
                    print("NOTE: You have not specified the travel modes to compare, hence, the merged shapefiles- {0} -alone were produced".format(str(merged_files).strip("[]")))
      