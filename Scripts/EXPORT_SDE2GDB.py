#EXPORT_SDE2GDB.py
#
# Source: http://gis.stackexchange.com/questions/67529/how-to-copy-an-sde-geodatabase-to-a-file-geodatabase-using-python
#
# July 2015
# John.Fay@duke.edu

import arcpy, os, shutil, time
import logging as log
from datetime import datetime

databaseConnection = os.path.abspath("C:\WorkSpace\EEP_Spring2015\EEP_Tool\Data\NC.sde")
targetGDB = 'C:/temp/XMLS/NC_copy.gdb'

def formatTime(x):
    minutes, seconds_rem = divmod(x, 60)
    if minutes >= 60:
        hours, minutes_rem = divmod(minutes, 60)
        return "%02d:%02d:%02d" % (hours, minutes_rem, seconds_rem)
    else:
        minutes, seconds_rem = divmod(x, 60)
        return "00:%02d:%02d" % (minutes, seconds_rem)

def getDatabaseItemCount(workspace):
    arcpy.env.workspace = workspace
    feature_classes = []
    for dirpath, dirnames, filenames in arcpy.da.Walk(workspace,datatype="Any",type="Any"):
        for filename in filenames:
            feature_classes.append(os.path.join(dirpath, filename))
    return feature_classes, len(feature_classes)

def replicateDatabase(dbConnection, targetGDB):
    startTime = time.time()

    featSDE,cntSDE = getDatabaseItemCount(dbConnection)
    featGDB,cntGDB = getDatabaseItemCount(targetGDB)

    now = datetime.now()
    logName = now.strftime("SDE_REPLICATE_SCRIPT_%Y-%m-%d_%H-%M-%S.log")
    log.basicConfig(datefmt='%m/%d/%Y %I:%M:%S %p', format='%(asctime)s %(message)s',\
    filename=logName,level=log.INFO)

    print "Old Target Geodatabase: %s -- Feature Count: %s" %(targetGDB, cntGDB)
    log.info("Old Target Geodatabase: %s -- Feature Count: %s" %(targetGDB, cntGDB))
    print "Geodatabase being copied: %s -- Feature Count: %s" %(dbConnection, cntSDE)
    log.info("Geodatabase being copied: %s -- Feature Count: %s" %(dbConnection, cntSDE))

    arcpy.env.workspace = dbConnection

    #deletes old targetGDB
    try:
        shutil.rmtree(targetGDB)
        print "Deleted Old %s" %(os.path.split(targetGDB)[-1])
        log.info("Deleted Old %s" %(os.path.split(targetGDB)[-1]))
    except Exception as e:
        print e
        log.info(e)

    #creates a new targetGDB
    GDB_Path, GDB_Name = os.path.split(targetGDB)
    print "Now Creating New %s" %(GDB_Name)
    log.info("Now Creating New %s" %(GDB_Name))
    arcpy.CreateFileGDB_management(GDB_Path, GDB_Name)

    datasetList = [arcpy.Describe(a).name for a in arcpy.ListDatasets()]
    featureClasses = [arcpy.Describe(a).name for a in arcpy.ListFeatureClasses()]
    tables = [arcpy.Describe(a).name for a in arcpy.ListTables()]

    #Compiles a list of the previous three lists to iterate over
    allDbData = datasetList + featureClasses + tables

    for sourcePath in allDbData:
        targetName = sourcePath.split('.')[-1]
        targetPath = os.path.join(targetGDB, targetName)
        if arcpy.Exists(targetPath)==False:
            try:
                print "Atempting to Copy %s to %s" %(targetName, targetPath)
                log.info("Atempting to Copy %s to %s" %(targetName, targetPath))
                arcpy.Copy_management(sourcePath, targetPath)
                print "Finished copying %s to %s" %(targetName, targetPath)
                log.info("Finished copying %s to %s" %(targetName, targetPath))
            except Exception as e:
                print "Unable to copy %s to %s" %(targetName, targetPath)
                print e
                log.info("Unable to copy %s to %s" %(targetName, targetPath))
                log.info(e)
        else:
            print "%s already exists....skipping....." %(targetName)
            log.info("%s already exists....skipping....." %(targetName))
    featGDB,cntGDB = getDatabaseItemCount(targetGDB)
    print "Completed replication of %s -- Feature Count: %s" %(dbConnection, cntGDB)
    log.info("Completed replication of %s -- Feature Count: %s" %(dbConnection, cntGDB))
    totalTime = (time.time() - startTime)
    totalTime = formatTime(totalTime)
    log.info("Script Run Time: %s" %(totalTime))

if __name__== "__main__":
    #databaseConnection = r"YOUR_SDE_CONNECTION"
    #targetGDB = "DESTINATION_PATH\\SDE_Replicated.gdb"
    replicateDatabase(databaseConnection, targetGDB) 