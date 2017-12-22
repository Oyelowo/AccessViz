# -*- coding: utf-8 -*-

import problem1

import geopandas as gpd
import zipfile
#fp= "http://blogs.helsinki.fi/accessibility/helsinki-region-travel-time-matrix-2015/"
fp=r"C:\Users\oyeda\Desktop\AUTOGIS\FINAL_ASSIGNMENT"
data_zip = zipfile.ZipFile((fp+"\HelsinkiRegion_TravelTimeMatrix2015.zip"), "r")
metropo=r"C:\Users\oyeda\Desktop\AUTOGIS\FINAL_ASSIGNMENT\MetropAccess_YKR_grid\MetropAccess_YKR_grid_EurefFIN.shp"

mtp= gpd.read_file(metropo)

problem1.lowo.extractfiles(data_zip)


#For testing
#[int(x) for x in aa]
    #6016696, 6015141, 5991603, 5991515, 5789455,9485399, 5789456, 4,2545,54646, 5802791, 8897
    
    #xx="HelsinkiRegion_TravelTimeMatrix2015/6016xxx/travel_times_to_ 6016696.txt"
    #xx[44:]