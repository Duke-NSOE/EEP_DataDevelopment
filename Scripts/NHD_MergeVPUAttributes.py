# NHD_MergeVPUAttributes.py
#
# Merges and appends NHD tables for indivdidual zones into a single table for all zones
#  CumTotPrecip: Mean Annual and monthly tables --> CumTotPrecipXX.csv
#  CumTotTemp:  Mean Annual and monthly tables --> CumTotTempXX.csv
#  ROMA:  Mean Annual and monthly tables --> RunoffXX.csv
#
# This script is designed to work with the native NHD+ directory structure and
#  should be run setting the rootFldr variable to a folder containing the
#  NHD region root folders.
#
# When complete, this script generages 3 csv files containing the mean annual
#  and mean monthly values for the three parameters: precip, temp, and runoff
#
# Spring 2015
# John.Fay@Duke.edu

import sys, os, arcpy

#Root folder - Set this to where the NHD+ data live
rootFldr = r'K:\Research\NHDv2'
outFldr = os.path.abspath("..\\Data\\VPUMerge.gdb")

#Allow overwrites
arcpy.env.overwriteOutput = True

#Create a list of links to each NHD+ region data folder relative to the root folder
#The data we need live in the VPUAttributeExtension folders within each workspace
dataFldrs = []
dataFldrs.append(os.path.join(rootFldr,"NHDPlusSA\\NHDPlus03N\\VPUAttributeExtension"))
dataFldrs.append(os.path.join(rootFldr,"NHDPlusSA\\NHDPlus03S\\VPUAttributeExtension"))
dataFldrs.append(os.path.join(rootFldr,"NHDPlusSA\\NHDPlus03W\\VPUAttributeExtension"))
dataFldrs.append(os.path.join(rootFldr,"NHDPlusMS\\NHDPlus05\\VPUAttributeExtension"))
dataFldrs.append(os.path.join(rootFldr,"NHDPlusMS\\NHDPlus06\\VPUAttributeExtension"))

#Make a list of files to merge
arcpy.env.workspace = dataFldrs[0]
parameters = arcpy.ListFiles("*.txt")

#Drop some items...
parameters.remove("IncrLat.txt")
parameters.remove("CumDivNLCD2011.txt")
parameters.remove("CumDivPrecipMA.txt")
parameters.remove("CumDivTempMA.txt")
parameters.remove("CumTotNLCD2011.txt")

#Status counter
x = 1

for param in parameters:
    print "Working on {} ({} of {})".format(param,x,len(parameters))
    x += 1 #Increase the counter

    #Create the output file in the geodatabase
    outFile = os.path.join(outFldr,param[:-4])

    #loop thru each workspace and create an merge list
    fileNames = []
    for df in dataFldrs:
        fileNames.append(os.path.join(df,param))
        
    #Merge the files
    print "...merging files" 
    arcpy.Merge_management(fileNames,outFile)
