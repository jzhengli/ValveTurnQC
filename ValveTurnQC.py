## script for QC water valve turns-to-close, output featureclass include all valves need to be check, results store in a file geodatabase
## 
import arcpy

RPUDWorkspace = "Database Connections/RPUD_TESTDB.sde"

#############################################################
fileDBWorkspace = 'C:/data/Junk.gdb' ### change this output path before running the script                                
valveToQC = 'RPUD.Water_Distribution_Features/fs_MissingValve' ### comment out this line and use System Valve below if needed  
# valveToQC = 'RPUD.WaterDistributionNetwork/wSystemValve'
#############################################################

try:
	arcpy.env.workspace = RPUDWorkspace
	inFCName = valveToQC
	inFC = RPUDWorkspace + "/" + inFCName
	dsc = arcpy.Describe(inFCName)
	fields = dsc.fields
	fieldNames = [field.name for field in fields if field.name != dsc.OIDFieldName]
	diameterIdx = fieldNames.index("DIAMETER")
	turnsIdx = fieldNames.index("TURNSTOCLOSE")

	arcpy.env.workspace = fileDBWorkspace
	outFCName = "ValveTurnsQC"
	outFC = fileDBWorkspace + "/" + outFCName
	try:
		if arcpy.Exists(outFCName):
			arcpy.Delete_management(outFCName)
	except Exception:
		print ("Cannot get a lock, try close all ArcGIS windows")
		exit()
	arcpy.CreateFeatureclass_management(fileDBWorkspace, outFCName, "POINT", inFC, "DISABLED", "DISABLED", arcpy.Describe(inFC).spatialReference)
	# print arcpy.Describe(fileDBWorkspace + "/" + outFCName)

	arcpy.env.workspace = RPUDWorkspace

	whereClause = "DIAMETER IS NOT NULL AND TURNSTOCLOSE IS NOT NULL ORDER BY DIAMETER" # find all features with valid diameter and turns-to-close value
	with arcpy.da.SearchCursor(inFC, fieldNames, whereClause) as sCursor:
		with arcpy.da.InsertCursor(outFC, fieldNames) as iCursor:
			for row in sCursor:
				sigma = int((round(row[diameterIdx] * 0.25))) # custom range for verify turns to close based on diameter
				if row[diameterIdx] == 0:
					iCursor.insertRow(row)
					print (u'Diameter {0}, Turns {1}'.format(row[diameterIdx], row[turnsIdx])) # 29 is the index for DIAMETER, 11 is the index for TURNSTOCLOSE
				elif not ((row[turnsIdx] - sigma) <= (row[diameterIdx] * 3) <= (row[turnsIdx] + sigma)): # Turns-to-close normally equals diameter * 3
					print (u'Diameter {0}, Turns {1}'.format(row[diameterIdx], row[turnsIdx]))
					iCursor.insertRow(row)
	print ("Result has been saved to: " + outFC)
except Exception:
	print ("Please check your input/output path!")

