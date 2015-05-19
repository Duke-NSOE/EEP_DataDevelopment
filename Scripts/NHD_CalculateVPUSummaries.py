# NHD_CalculateVPUSummaries.py
#
# Description: Calculates min and max of the of monthly means
#
#
# Spring 2015
# John.Fay@Duke.edu

import sys, os, arcpy

#The VPU attribute geodatabase; this is the product of the NHD_MergeVPUAttributes.py script
vpuGDB = os.path.abspath("..\\Data\\VPUMerge.gdb")

#Allow overwrites
arcpy.env.overwriteOutput = True
arcpy.env.workspace = vpuGDB

#Create a list of the parameter tables/field name tuples to process
parameters = [('IncrPrecip','Precip'),('IncrTempMA','Temp'),('ROMA','RunOff')]

#Loop through the tables
for tbl,fld in parameters:
    #Repeat for max and min values
    for stat in ("min","max"):
        print "Calculating {} of {}.".format(stat,fld)
        
        #Add field to hold the outputs
        fldName = "{}_{}".format(fld,stat)
        print "...adding {} field".format(fldName)
        arcpy.AddField_management(tbl,fldName,"DOUBLE",8,4)
        
        #Create the field expression
        print "...building calculation expression"
        exp = stat + "("
        for x in range(1,13):
            #Convert number to two digit month
            mm = "%02d" %x
            #Add the field to the expression
            exp += "!{}V{}!,".format(fld,mm)
        #Replace the last comma with a close parens
        exp = exp[:-1] + ")"
        
        #Apply the field expression
        arcpy.CalculateField_management(tbl,fldName,exp,"PYTHON")