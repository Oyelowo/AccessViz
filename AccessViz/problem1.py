# -*- coding: utf-8 -*-
"""
Created on Fri Dec 22 10:15:11 2017

@author: oyeda
"""
#import geopandas as gpd
#import zipfile
##fp= "http://blogs.helsinki.fi/accessibility/helsinki-region-travel-time-matrix-2015/"
#fp=r"C:\Users\oyeda\Desktop\AUTOGIS\FINAL_ASSIGNMENT"
#data_zip = zipfile.ZipFile((fp+"\HelsinkiRegion_TravelTimeMatrix2015.zip"), "r")
#metropo=r"C:\Users\oyeda\Desktop\AUTOGIS\FINAL_ASSIGNMENT\MetropAccess_YKR_grid\MetropAccess_YKR_grid_EurefFIN.shp"
#
#mtp= gpd.read_file(metropo)
#for i,rows in z.
# =============================================================================
# 1. AccessViz finds from the data folder all the matrices that user has 
# specified by assigning a list of integer values that should correspond to 
# YKR-IDs found from the attribute table of a Shapefile called
# MetropAccess_YKR_grid.shp. If the ID-number that the user has specified does
# not exist in the data folders, the tools should warn about this to the user 
# but still continue running. The tool should also inform the user about the 
# execution process: tell the user what file is currently under process and how 
# many files there are left 
# (e.g. “Processing file travel_times_to_5797076.txt.. Progress: 3/25”).
# =============================================================================

#aa= raw_input()
#x= input("list the ID-numbers you want to read: ")  
#aa= [int(x) for x in input().split()] #with this, you only need to separate by space

#alternative
#s = input()
#numbers = list(map(int, s.split()))


#aa= [int(x) for x in input("list the ID-numbers you want to read and separate each by a comma(,): ").split(',')]
#print("these are the numbers{0}".format(aa))
#type(aa)

class lowo:
#    def __init__(self):
#        ''' Constructor for this class. '''
    def extractfiles(data_zip):
        '''
        data: this is the zipped data which should be specified.
        This function extracts matrices(files) from the zipped Helsinki Region Travel
        Time Matrix, according to the userinputs(matrix ID). It also states if
        the specified input is not included in the matrices
        specified by user'''
    #ui is userinput
        userinput= [int(x) for x in input("list the ID-numbers you want to read and separate each by a comma(,): ").split(',')]
    
        #Extract the names of all the lists from the zipped file
        namelist= data_zip.namelist()
        
        #create an empty list
        m_list=[]
        #iterate over all the names in the namelist of the zipped folders
        for filename in namelist:
            #iterate over the userinput, to get all its element/values
            for element in userinput:
                #when each element is converted to string, check if the length
                #of the string is equal to normal length of every matrix ID(i.e, 7)
                # and also if the element is in the filename in the namelist
                if len(str(element))==7 and str(element) in filename:
                    #the below can also be used to know which of the filenames exactly
                    #print(filename)
                    
                    #this can be used to know its index in the list
                    #print(namelist.index(filename))
                    
                    #now, append the element to the matrix list which now includes
                    #the imputed values by user which are equal to the normal length of the 
                    #IDs(i.7) and are also in the zip folders(i.e filename)
                    m_list.append(element)
                    
                    #check for the progress
                    print("Processing file travel_times_to_{0}.txt.. Progress: {1}/{2}".format(element,len([i for i in range(len(m_list))]), len(m_list)))
                    
                    #The above can also simply be done as below
                    #slice the string. This is used for the following step, just
                    #to know which of the matrix is presently being extracted.
                    #f_slice=filename[44:]
                    #print("processing file {0}.. Progress: {1}/{2}".format(f_slice,len([i for i in range(len(m_list))]), len(m_list)))
                    
                    #read the file
                    bytes = data_zip.read(filename)
                    
                    #print the file size
                    print('has',len(bytes),'bytes')
                    
                    #extract the files
                    data_zip.extract(filename)
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
    
     #           if any(x in lk for x in ui)== False:
    #                print('d')
#extractfiles(data=data_zip)

 

#For testing
#[int(x) for x in aa]
    #6016696, 6015141, 5991603, 5991515, 5789455,9485399, 5789456, 4,2545,54646, 5802791, 8897
    
    #xx="HelsinkiRegion_TravelTimeMatrix2015/6016xxx/travel_times_to_ 6016696.txt"
    #xx[44:]