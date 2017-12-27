# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 09:16:52 2017

@author: oyeda
"""

m_list=[]
destination_style='circle'
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
        
        #This is done to handle matrices with nodata at all. e.g: matrix"6016696"
        if tt_matrices['to_id'].max()==-1:
            print('the MATRIX- {0} is empty and has nodata'.format(element))
            print('\n')
        else:
            merged_metro = pd.merge(grid_shp,tt_matrices,  left_on="YKR_ID", right_on="from_id")
            #print(merged_metro)
            #Calculate the x and y coordinates of the grid.
            merged_metro['x'] = merged_metro.apply(getCoords, geom_col="geometry", coord_type="x", axis=1)

            merged_metro['y'] = merged_metro.apply(getCoords, geom_col="geometry", coord_type="y", axis=1)
            
            #NOTE: I CHOSE TO DEAL WITH NODATA BY EXCLUDING THEM.
            merged_metro= merged_metro.loc[merged_metro.loc[:, tt_col]!=-1]
            
            #Next, we want to classify the travel times with 5 minute intervals until 200 minutes.

            #Let’s create a list of values where minumum value is 5, maximum value is 200 and step is 5.
            breaks = [x for x in range(5, 200, 5)]
            #Now we can create a pysal User_Defined classifier and classify our travel time values.
            
            if classification =='pysal_class':
                if class_type == "Natural_Breaks":
                    classifier = ps.Natural_Breaks.make(k=n_classes)
                elif class_type == "Equal_Interval":
                    classifier = ps.Equal_Interval.make(k=n_classes)
                elif class_type == "Box_Plot":
                    classifier = ps.Box_Plot.make(hinge=1.5)
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
                upper_limit = 60
                
                step = 10
                
                names = ["%s-%s" % (x-5, x) for x in range(step, upper_limit, step)]
                #         ["{0}kk{1}".format(x-5,x) for x in range(5, 200, 5)]   #alternative
                
                #Add legend label for over 60.
                names.append("%s<" % upper_limit)
                #Assign legend names for the classes.
                #data['label_wt'] = None
                
                merged_metro['label_' + tt_col ] = None
                
                #Update rows with the class-names.
                
                for i in range(len(names)):
                    merged_metro.loc[merged_metro[tt_col+"_ud"] == i, 'label_' + tt_col] = names[i]
                   
                #Update all cells that didn’t get any value with "60 <"
                #data['label_wt'] = data['label_wt'].fillna("%s <" % upper_limit)
                
                merged_metro['label_' + tt_col] = merged_metro['label_' + tt_col].fillna("%s<" % upper_limit)
                
            #Finally, we can visualize our layers with Bokeh, add a legend for travel times 
            #and add HoverTools for Destination Point and the grid values (travel times).
            # Select only necessary columns for our plotting to keep the amount of data minumum
            #df = data[['x', 'y', 'walk_t','walk_t_ud', 'car_r_t','car_r_t_ud', 'from_id', 'label_wt', "label_car"]]
            df = merged_metro[['x', 'y',"YKR_ID", tt_col,tt_col+"_ud","from_id" ,'label_' + tt_col]]
            df_dest_id= df.loc[df['YKR_ID']==element]
            dfsource = ColumnDataSource(data=df)
            dfsource_dest_id = ColumnDataSource(data=df_dest_id)
            # Specify the tools that we want to use
            TOOLS = "pan,wheel_zoom,box_zoom,reset,save"
            
            # Flip the colors in color palette
            palette4.reverse()
            color_mapper = LogColorMapper(palette=palette4)
            #color_mapper = ContinuousColorMapper(palette=palette4)
         
            
            list_of_titles = ["walk_t: Travel time in minutes from origin to destination by walking",
                              "walk_d: Distance in meters of the walking route",
                            "pt_r_tt: Travel time in minutes from origin to destination by public transportation in rush hour traffic", 
                            "pt_r_t:	 Travel time in minutes from origin to destination by public transportation in rush hour traffic",
                            "pt_r_d:	 Distance in meters of the public transportation route in rush hour traffic",
                            "pt_m_tt: Travel time in minutes from origin to destination by public transportation in midday traffic",
                            "pt_m_t:	 Travel time in minutes from origin to destination by public transportation in midday traffic",
                            "pt_m_d:	 Distance in meters of the public transportation route in midday traffic",
                            "car_r_t: Travel time in minutes from origin to destination by private car in rush hour traffic",
                            "car_r_d: Distance in meters of the private car route in rush hour traffic",
                            "car_m_t: Travel time in minutes from origin to destination by private car in midday traffic",
                            "car_m_d: Distance in meters of the private car route in midday traffic"]
                                                
            
            #here, for the title. i got the location of the specified travel mode(tt_col), then, with its
#                    with its index, i got the corresponsding location in the list which was arranged according to the
#                    to the columns of the dataframe(tt_matrices) too. 2 is subracted(i.e -2) because, the list_of_titles
#                    is shorter by 2, as it does not include from_id or to_id which are not variables of interest here but the travel modes only.
            if map_type=='interactive':
                p = figure(title=list_of_titles[tt_matrices.columns.get_loc(tt_col) - 2], tools=TOOLS,
                             plot_width=800, plot_height=650, active_scroll = "wheel_zoom" )
             
                
                
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
                                (tt_col, "@" + tt_col)]  
                p.add_tools(ghover)
                
                  # Insert a circle on top of the location(coords in EurefFIN-TM35FIN)
                #print(element)
                #because, it  is a grid, the location of each cell has about s x and 
                #y coordinates, hence, after finding the x for each grid, select 
                #one of the x and y coordinates(the third, which is the centre of each grid) from the list.
                dest_grid_x = (df.loc[df["YKR_ID"]==element, 'x'].values[0])[2]
                dest_grid_y =  (df.loc[df["YKR_ID"]==element, 'y'].values[0])[2]
                
                #Alternative to getting the centre of a grid:
#                grid_centroid=merged_metro.loc[merged_metro['YKR_ID']==element, 'geometry'].values[0].centroid
#                dest_grid_x=grid_centroid.x 
#                dest_grid_y= grid_centroid.y
                
                if destination_style=='circle':
                # Add two separate hover tools for the data
                    circle = p.circle(x=[dest_grid_x], y=[dest_grid_y], name="point", size=6, color="blue")
                
                    phover = HoverTool(renderers=[circle])
                    phover.tooltips=[("Destination", str(element))]
                    p.add_tools(phover)
                   
                elif destination_style=='grid':
                    grid_dest_id= p.patches('x', 'y', source=dfsource_dest_id, name='grid', color='blue')
                
                    ghover_dest_id = HoverTool(renderers=[grid_dest_id])
                    ghover_dest_id.tooltips=[("DESTINATION ID", str(element))] 
                    p.add_tools(ghover_dest_id)
               
                
        
              # Output filepath to HTML
               
                # Save the map
                save(p, filepath + "/" +tt_col +"_" + str(element) + ".html")
                
            elif map_type=='static':
                mapTitle, my_map = plt.subplots(1)
                my_map = merged_metro.plot(column=tt_col, linewidth=0.02, legend=True, cmap="RdYlGn", scheme="Quantiles", k=5, alpha=0.9)
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
                
                dest_grid.plot(ax=my_map, color= "blue", legend=True, linewidth=3)
                

                #plt.legend(["roads", "metro line","Rautatientori"])
                title_map=list_of_titles[tt_matrices.columns.get_loc(tt_col) - 2]
                plt.title(title_map[:43] + '\n'+ title_map[44:])
                
                #North arrow to southeastern corner
                my_map.text(x=402400,y=6669000, s='N\n^', ha='center', fontsize=20, family='Courier new', rotation = 0)
                
                #move legend so it doesn't overlap the map
                leg = my_map.get_legend()
                leg.set_bbox_to_anchor((1.58, 0.9))
                
                #resize mapwindow, so that legend can also fit there.
                mapBox = my_map.get_position()
                my_map.set_position([mapBox.x0, mapBox.y0, mapBox.width*0.7, mapBox.height*0.7])
                my_map.legend()                
                
                #plt.show()
                
                # Save the figure as png file with resolution of 300 dpi
                outfp = filepath + "/" + "static_map_"+tt_col +"_" + str(element) + ".png"
                plt.savefig(outfp, dpi=300)

            
#put into an object the inputs are not in the matrix list(i.e which of the specified is not in the zipped matrices)
absentinput= [i for i in userinput if i not in m_list]

#check if all of the imputed values does not exist
if len(absentinput)==len(userinput):
    print("all the inputs do not exist")
    
    #check for those that are not included in the matrices
elif any(absentinput) not in m_list:
    #warn that they do not exist
    print("WARNING: ", absentinput, ".txt do not exist")
    #check how many of them are not in the matrices
    print(len(absentinput), "of the inputs are not included in the matrices")    
    print("\n")