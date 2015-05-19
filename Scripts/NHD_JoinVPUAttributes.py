# NHD_JoinVPUAttributes.py
#
# Description: Joins the annual mean and mean monthly tables for a given
#  NHD+ VPU Attribute (precipitation, temperature, runoff) into a single
#  table.
#
# Requires a geodatabase that includes tables for the annual and monthly
#  records for each parameter, e.g., the results of the NHD_MergeVPUAttributes.py
#  script.
#
# Spring 2015
# John.Fay@Duke.edu

import sys, os, arcpy

#The VPU attribute geodatabase; this is the product of the NHD_MergeVPUAttributes.py script
vpuGDB = os.path.abspath("..\\Data\\VPUMerge.gdb")

#Allow overwrites
arcpy.env.overwriteOutput = True
arcpy.env.workspace = vpuGDB

#Create a list of the parameter tables to create
parameters = ['IncrPrecipMA', 'IncrTempMA','ROMA0001']

##---PRECIPITATION---
print "Processing precipitation files"
# Set inputs and output
inTable = 'IncrPrecipMA'
outTable = 'IncrPrecip'

#Copy the mean annual table to a new table
arcpy.CopyRows_management(inTable,outTable)

#Remove the extranneous fields
arcpy.DeleteField_management(outTable,["MissDataA","PrecipVT","Hydroseq"])

#Rename the Mean Annual field
arcpy.AlterField_management(outTable,"PrecipV","PrecipVMA","PrecipMA")

#Add an attribute index to speed processing
arcpy.AddIndex_management(outTable,"FeatureID","FeatureID","UNIQUE","ASCENDING")

#Loop through the monthly tables and join each
for mm in range(1,13):
    mmFile = "IncrPrecipMM%02d" %mm     #Table name
    mmFld = "PrecipV%02d" %mm           #Merged field name
    #Join the monthy mean field
    print "...joining field from  {}".format(mmFile)
    arcpy.JoinField_management(outTable,"FeatureID",mmFile,"FeatureID",["PrecipV"])
    #Rename the field just added
    arcpy.AlterField_management(outTable,"PrecipV",mmFld,mmFld)

##---TEMPERATURE---
print "Processing temperature files"
# Set inputs and output
inTable = 'IncrTempMA'
outTable = 'IncrTemp'

#Copy the mean annual table to a new table
arcpy.CopyRows_management(inTable,outTable)

#Remove the extranneous fields
arcpy.DeleteField_management(outTable,["MissDataA","TempVT","Hydroseq"])

#Rename the Mean Annual field
arcpy.AlterField_management(outTable,"TempV","TempVMA","TempMA")

#Loop through the monthly tables and join each
for mm in range(1,13):
    mmFile = "IncrTempMM%02d" %mm     #Table name
    mmFld = "TempV%02d" %mm           #Merged field name
    #Join the monthy mean field
    print "...joining field from  {}".format(mmFile)
    arcpy.JoinField_management(outTable,"FeatureID",mmFile,"FeatureID",["TempV"])
    #Rename the field just added
    arcpy.AlterField_management(outTable,"TempV",mmFld,mmFld)
    
##---RUNOFF---
print "Processing runoff files"
# Set inputs and output
inTable = 'ROMA0001'
outTable = 'ROMA'

#Copy the mean annual table to a new table
arcpy.CopyRows_management(inTable,outTable)

#Remove the extranneous fields
arcpy.DeleteField_management(outTable,["MissDataA","RunOffVT","Hydroseq"])

#Rename the Mean Annual field
arcpy.AlterField_management(outTable,"RunOffV","RunOffVMA","RunOffMA")

#Loop through the monthly tables and join each
for mm in range(1,13):
    mmFile = "ROMM%02d0001" %mm     #Table name
    mmFld = "RunOffV%02d" %mm           #Merged field name
    #Join the monthy mean field
    print "...joining field from  {}".format(mmFile)
    arcpy.JoinField_management(outTable,"FeatureID",mmFile,"FeatureID",["RunOffV"])
    #Rename the field just added
    arcpy.AlterField_management(outTable,"RunOffV",mmFld,mmFld)