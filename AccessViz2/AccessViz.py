# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 16:40:18 2017

@author: oyeda
"""

# =============================================================================
# AccessViz
# What the tool should do?
# AccessViz is a set of tools that can be used for managing and helping to analyze 
# Helsinki Region Travel Time Matrix data (2013 / 2015) that can be downloaded from here.
#  Read also the description of the dataset from the web-pages so that you get 
#  familiar with the data.
# 
# AccessViz tool package has following main functionalities (i.e. functions) that 
# should work independently:
# 
# 1. AccessViz finds from the data folder all the matrices that user has specified 
# by assigning a list of integer values that should correspond to YKR-IDs found from 
# the attribute table of a Shapefile called MetropAccess_YKR_grid.shp. If the ID-number 
# that the user has specified does not exist in the data folders, the tools should 
# warn about this to the user but still continue running. The tool should also 
# inform the user about the execution process: tell the user what file is currently 
# under process and how many files there are left (e.g. “Processing file travel_times_to_5797076.txt.. Progress: 3/25”).
# =============================================================================


def demoprint():
    print("oyelowo is a genius")