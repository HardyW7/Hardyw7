##### The link to my geoprocessing service is: http://qilin.geog.uw.edu:6080/arcgis/rest/services/hardyw7/ReclassVectorWooldridge7/GPServer ########
##### the name of the geoprocessing service is: ReclassVectorWooldridge7
##### I was unable to update my original service and so I ended up with more than one version


import arcpy

#set environment workspace and overwrite functions
arcpy.env.workspace = "U:/"

#set local variables
inputFC = arcpy.GetParameterAsText(0)            #Input feature class
inField = arcpy.GetParameterAsText(1)            #Input field from 'inputFC' to be reclassed
rcTable = arcpy.GetParameterAsText(2)            #Table that has reclass ranges
remapLower = arcpy.GetParameterAsText(3)         #Field in 'rcTable' that has lower bounds
remapUpper = arcpy.GetParameterAsText(4)         #Field in 'rcTable' that has upper bounds
remapValue = arcpy.GetParameterAsText(5)         #Field in 'rcTable' that has new values
outField = arcpy.GetParameterAsText(6)           #User inputted name for reclass field to be created
outFieldType = arcpy.GetParameterAsText(7)       #Type for 'outField'
remapVals = []                                   #Variable for reclass decision numbers
notfoundvalue = "9999"
outputFC = arcpy.GetParameterAsText(8) #Output file parameter

#copy feature layer
arcpy.CopyFeatures_management(inputFC,outputFC)

#Create a new field in 'outputFC' called 'outField' of type 'outFieldType'
arcpy.AddField_management(outputFC,outField,outFieldType)

#Create a list of lists containing a lower bound, upper bound and new value in each list
with arcpy.da.SearchCursor(rcTable,[remapLower,remapUpper,remapValue]) as cursor:
    for row in cursor:
        remapVals.append([row[0], row[1], row[2]])

#Change the values of the 'outField' based on 'inField' value being within a reclass range
with arcpy.da.UpdateCursor(outputFC,[inField,outField]) as cursor:
    for row in cursor:
        for i in range(0,len(remapVals),1):                                #entendable number of reclass classes
            if row[0] >= remapVals[i][0] and row[0] < remapVals[i][1]:     #iterates over the 'i'th list
                row[1] = remapVals[i][2]
                cursor.updateRow(row)
                i += 1

#Records not caught by the above for loop remain with a value of 0'
#For each record that has remained '0' update it to '9999'
with arcpy.da.UpdateCursor(outputFC,[inField,outField]) as cursor:
    for row in cursor:
        if row[1] == 0:
            row[1] = notfoundvalue
            cursor.updateRow(row)


			
			
######### I talked with Amanda at the very end of my assignment because my tool would run locally but not as a geoprocessing service
######### she suggested changing the parameter type for the lookup table from 'Table' to 'Dataset'