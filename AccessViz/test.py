
# -*- coding: utf-8 -*-

#import problem1
from problem1 import lowo, zip2shp
from visualise_tt import visual

import geopandas as gpd
import zipfile
#fp= "http://blogs.helsinki.fi/accessibility/helsinki-region-travel-time-matrix-2015/"
fp=r"C:\Users\oyeda\Desktop\AUTOGIS\FINAL_ASSIGNMENT"
data_zip = zipfile.ZipFile((fp+"\HelsinkiRegion_TravelTimeMatrix2015.zip"), "r")
metropo=r"C:\Users\oyeda\Desktop\AUTOGIS\FINAL_ASSIGNMENT\MetropAccess_YKR_grid\MetropAccess_YKR_grid_EurefFIN.shp"

mtp= gpd.read_file(metropo)
#namelist=data_zip.namelist()
#lowo.extractfilesPrompt1(data_zip=data_zip, filepath = fp+"/matrices", sep=",", file_format=".csv")


#For testing
#[int(x) for x in aa]
    #6016696, 6015141, 5991603, 5991515, 5789455,9485399, 5789456, 4,2545,54646, 5802791, 8897
    
    #xx="HelsinkiRegion_TravelTimeMatrix2015/6016xxx/travel_times_to_ 6016696.txt"
    #xx[44:]
    
#bytes
#data_zip.read()
#data_zip.open(filename)
zip2shp.readzip1(data_zip=data_zip, separate_folder=False, userinput=[5991,342,6016696, 6015141, 5991603, 5991515, 5789455,9485399, 5789456, 4,2545,54646, 5802791, 8897,2524,245], grid_shp=mtp, filepath= r"C:\Users\oyeda\Desktop\AUTOGIS\FINAL_ASSIGNMENT\merged")
zip2shp.readzipPrompt1(data_zip=data_zip, separate_folder=True, grid_shp=mtp, filepath= r"C:\Users\oyeda\Desktop\AUTOGIS\FINAL_ASSIGNMENT\merged")

zip2shp.readzip2(data_zip=data_zip, separate_folder=True, userinput=[5991,342,6016696, 6015141, 5991603, 5991515, 5789455,9485399, 5789456, 4,2545,54646, 5802791, 8897,2524,245], grid_shp=mtp,filepath=r"C:\Users\oyeda\Desktop\AUTOGIS\FINAL_ASSIGNMENT\merged")
zip2shp.readzipPrompt2(data_zip=data_zip, grid_shp=mtp,filepath=r"C:\Users\oyeda\Desktop\AUTOGIS\FINAL_ASSIGNMENT\merged" )



hh=gpd.read_file(r"C:\Users\oyeda\Desktop\AUTOGIS\FINAL_ASSIGNMENT\merged\merged.shp5789455\merged.shp")


list(mtp.iloc[:,2])

lowo.extractfilesPrompt1(data_zip= data_zip, filepath= fp +"/matrices", sep="\t")
lowo.extractfilesPrompt2(data_zip= data_zip, filepath= fp +"/matrices", sep="\t")


zip2shp.readzipAll(data_zip=data_zip, userinput=[5991,342,6016696, 6015141, 5991603, 5991515, 5789455,9485399, 5789456, 4,2545,54646, 5802791, 8897,2524,245], grid_shp=mtp, filepath= r"C:\Users\oyeda\Desktop\AUTOGIS\FINAL_ASSIGNMENT\merged")
zip2shp.readzipAllprompt(data_zip=data_zip, grid_shp=mtp, filepath= r"C:\Users\oyeda\Desktop\AUTOGIS\FINAL_ASSIGNMENT\merged")
aa=gpd.read_file(r"C:\Users\oyeda\Desktop\AUTOGIS\FINAL_ASSIGNMENT\merged\mergedAll.shp")


visual.vis(data_zip, userinput=[5991,342,6016696, 6015141, 5991603, 5991515, 5789455,9485399, 5789456, 4,2545,54646, 5802791, 8897,2524,245], 
           destination_style='grid',map_type='static',grid_shp=mtp, tt_col="pt_r_tt",n_classes=10, classification='pysal_class',  class_type='Quantiles' ,
           filepath=r"C:\Users\oyeda\Desktop\AUTOGIS\FINAL_ASSIGNMENT\visualise")   
#Ensure that the CRS is the same than in the all layers
mtp['geometry'] = mtp['geometry'].to_crs(epsg=3067)
mtp.crs
