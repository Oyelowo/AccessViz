# -*- coding: utf-8 -*-

import problem1
from problem1 import lowo, zip2shp, zip2shp2

import geopandas as gpd
import zipfile
#fp= "http://blogs.helsinki.fi/accessibility/helsinki-region-travel-time-matrix-2015/"
fp=r"C:\Users\oyeda\Desktop\AUTOGIS\FINAL_ASSIGNMENT"
data_zip = zipfile.ZipFile((fp+"\HelsinkiRegion_TravelTimeMatrix2015.zip"), "r")
metropo=r"C:\Users\oyeda\Desktop\AUTOGIS\FINAL_ASSIGNMENT\MetropAccess_YKR_grid\MetropAccess_YKR_grid_EurefFIN.shp"

mtp= gpd.read_file(metropo)

lowo.extractfiles(data_zip=data_zip)


#For testing
#[int(x) for x in aa]
    #6016696, 6015141, 5991603, 5991515, 5789455,9485399, 5789456, 4,2545,54646, 5802791, 8897
    
    #xx="HelsinkiRegion_TravelTimeMatrix2015/6016xxx/travel_times_to_ 6016696.txt"
    #xx[44:]
    
#bytes
#data_zip.read()
#data_zip.open(filename)

zip2shp.readzip(data_zip=data_zip, userinput=[5991,342,5991603,2524,245], grid_shp=mtp, filepath= r"C:\Users\oyeda\Desktop\AUTOGIS\FINAL_ASSIGNMENT\merged")
zip2shp2.readzipPrompt(data_zip=data_zip, grid_shp=mtp,filepath=r"C:\Users\oyeda\Desktop\AUTOGIS\FINAL_ASSIGNMENT\merged" )

problem1.zip2shp.readzipPrompt
problem1.zip2shp2.readzipPrompt