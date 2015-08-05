# NHD_CalculateNLCDSummaries.py
#
# Description: Adds new fields to the catchment NLCD tables (cumulative and 
#  incremental) and computes the total area of Anderson Level I (not II)
#  land covers (.e.g classes 21,22,23, and 24 are combbined into "NLCD2".
#
# Spring 2015
# John.Fay@Duke.edu

import sys, os, arcpy

#The VPU attribute geodatabase; this is the product of the NHD_MergeVPUAttributes.py script
vpuGDB = os.path.abspath("..\\Data\\VPUMerge.gdb")
cumNLCD = "CumTotNLCD2011"
incrNLCD = "IncrNLCD2011"

#Allow overwrites
arcpy.env.overwriteOutput = True
arcpy.env.workspace = vpuGDB

#Make a list of fields to add
flds = ["NLCD1","NLCD2","NLCD3","NLCD4","NLCD5","NLCD7","NLCD8","NLCD9"]

#Add fields (Repeat for cumulative and incremental NLCD tables)
for tbl in [incrNLCD]:
    #Add the fields
    for fld in flds:
        print ("Adding {} field to {}".format(fld,tbl))
        arcpy.AddField_management(tbl,fld,"DOUBLE",8,2)

##Cumulative NLCD-------------
#Create the field calculation expressions (remove the "C" when doing incremental...)
exp1c='!NLCD11AC!'
exp2c='!NLCD21AC! + !NLCD22AC! + !NLCD23AC! + !NLCD24AC!'
exp3c='!NLCD31AC!'
exp4c='!NLCD41AC! + !NLCD22AC! + !NLCD43AC!'
exp5c='!NLCD51AC!'
exp7c='!NLCD71AC!'
exp8c='!NLCD81AC! + !NLCD82AC!'
exp9c='!NLCD90AC! + !NLCD95AC!'

# Execute the field calculations
print "Executing calculations"
x = 1 ##Counter
arcpy.CalculateField_management(cumNLCD,"NLCD1",exp1c,"PYTHON"); print "{} of 8".format(x); x +=1
arcpy.CalculateField_management(cumNLCD,"NLCD2",exp2c,"PYTHON"); print "{} of 8".format(x); x +=1
arcpy.CalculateField_management(cumNLCD,"NLCD3",exp2c,"PYTHON"); print "{} of 8".format(x); x +=1
arcpy.CalculateField_management(cumNLCD,"NLCD4",exp3c,"PYTHON"); print "{} of 8".format(x); x +=1
arcpy.CalculateField_management(cumNLCD,"NLCD5",exp4c,"PYTHON"); print "{} of 8".format(x); x +=1
arcpy.CalculateField_management(cumNLCD,"NLCD7",exp7c,"PYTHON"); print "{} of 8".format(x); x +=1
arcpy.CalculateField_management(cumNLCD,"NLCD8",exp8c,"PYTHON"); print "{} of 8".format(x); x +=1
arcpy.CalculateField_management(cumNLCD,"NLCD9",exp9c,"PYTHON"); print "{} of 8".format(x); x +=1

##Incremental NLCD----------------
#Create the field calculation expressions (remove the "C" when doing incremental...)
exp1i='!NLCD11A!'
exp2i='!NLCD21A! + !NLCD22A! + !NLCD23A! + !NLCD24A!'
exp3i='!NLCD31A!'
exp4i='!NLCD41A! + !NLCD22A! + !NLCD43A!'
exp5i='!NLCD51A!'
exp7i='!NLCD71A!'
exp8i='!NLCD81A! + !NLCD82A!'
exp9i='!NLCD90A! + !NLCD95A!'

# Execute the field calculations
x = 1 ##Counter
arcpy.CalculateField_management(incrNLCD,"NLCD1",exp1i,"PYTHON"); print "{} of 8".format(x); x +=1
arcpy.CalculateField_management(incrNLCD,"NLCD2",exp2i,"PYTHON"); print "{} of 8".format(x); x +=1
arcpy.CalculateField_management(incrNLCD,"NLCD3",exp2i,"PYTHON"); print "{} of 8".format(x); x +=1
arcpy.CalculateField_management(incrNLCD,"NLCD4",exp3i,"PYTHON"); print "{} of 8".format(x); x +=1
arcpy.CalculateField_management(incrNLCD,"NLCD5",exp4i,"PYTHON"); print "{} of 8".format(x); x +=1
arcpy.CalculateField_management(incrNLCD,"NLCD7",exp7i,"PYTHON"); print "{} of 8".format(x); x +=1
arcpy.CalculateField_management(incrNLCD,"NLCD8",exp8i,"PYTHON"); print "{} of 8".format(x); x +=1
arcpy.CalculateField_management(incrNLCD,"NLCD9",exp9i,"PYTHON"); print "{} of 8".format(x); x +=1
