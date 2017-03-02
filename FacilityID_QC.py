## Script for QCing FacilityID of all major features, result being logged in a log file in same directory
import arcpy, logging, os, sys, time

arcpy.env.overwriteOutput = True 
arcpy.env.workspace = "Database Connections/RPUD_TRANSDB.sde"

logging.basicConfig(filename=os.path.join(os.path.dirname(sys.argv[0]), 'facilityID_qc.log'), level=logging.INFO, format='%(asctime)s %(message)s')
def logMessage(msg):
	logging.info(msg)
	print(time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime()) + msg)


def countFeature(fc, lyr, whereClause=""):
	arcpy.MakeFeatureLayer_management(fc, lyr, whereClause)
	result = arcpy.GetCount_management(lyr).getOutput(0)
	return result


def diagnoseField(fd, fc, prefix="", field="FACILITYID"):
	featureDataset = fd
	featureClass = fc
	layerName = fc + "_lyr"
	fieldName = field
	idPrefix = prefix
	
	whereClause = fieldName + " IS NOT NULL"
	notNull = countFeature(featureDataset + featureClass, layerName, whereClause)
	total = countFeature(featureDataset + featureClass, layerName)

	whereClause = "{0} NOT LIKE '{1}%' AND {0} IS NOT NULL".format(fieldName, idPrefix)
	wrongPrefix = countFeature(featureDataset + featureClass, layerName, whereClause)
	
	logMessage("Scanning {}...".format(featureClass))
	logMessage("Total count in {0} is: {1}".format(featureClass, total))
	logMessage("{0} null value found in field {1}".format(int(total) - int(notNull), fieldName))
	logMessage("{0} out of {1} not null value do not have correct prefix '{2}' in FacilityID".format(wrongPrefix, notNull, idPrefix))
	logMessage("...")


## Water
def checkWater():
	dataset = "RPUD.WaterDistributionNetwork/"
	diagnoseField(dataset, "RPUD.wCasing", "WCAS")
	diagnoseField(dataset, "RPUD.wControlValve", "WCV")
	diagnoseField(dataset, "RPUD.wFitting", "WFIT")
	diagnoseField(dataset, "RPUD.wGravityMain", "WGM")
	diagnoseField(dataset, "RPUD.wHydrant", "WHYD")
	diagnoseField(dataset, "RPUD.wLateralLine", "WLAT")
	diagnoseField(dataset, "RPUD.wNetworkStructure", "WNS")
	diagnoseField(dataset, "RPUD.wPressureMain", "WMN")
	diagnoseField(dataset, "RPUD.wSamplingStation", "WSS")
	diagnoseField(dataset, "RPUD.wServiceConnection", "WSC")
	diagnoseField(dataset, "RPUD.wSystemValve", "WSV")

## Sewer
def checkSewer():
	dataset = "RPUD.SewerCollectionNetwork/"
	diagnoseField(dataset, "RPUD.ssAerial", "SAM")
	diagnoseField(dataset, "RPUD.ssCasing", "SCA")
	diagnoseField(dataset, "RPUD.ssCleanout", "SCO")
	diagnoseField(dataset, "RPUD.ssControlValve", "SCV")
	diagnoseField(dataset, "RPUD.ssFitting", "SF")
	diagnoseField(dataset, "RPUD.ssForceMain", "SFMN")
	diagnoseField(dataset, "RPUD.ssGravityMain", "SGMN")
	diagnoseField(dataset, "RPUD.ssGreaseTrap", "SGT")
	diagnoseField(dataset, "RPUD.ssLateralLine", "SLAT")
	diagnoseField(dataset, "RPUD.ssManhole", "SMH")
	diagnoseField(dataset, "RPUD.ssMeterStation", "SMS")
	diagnoseField(dataset, "RPUD.ssNetworkStructure", "SNS")
	diagnoseField(dataset, "RPUD.ssSystemValve", "SSV")

## Reuse
def checkReuse():
	dataset = "RPUD.ReclaimedWaterDistributionNetwork/"
	diagnoseField(dataset, "RPUD.rCasing", "RCAS")
	diagnoseField(dataset, "RPUD.rControlValve", "RCV")
	diagnoseField(dataset, "RPUD.rFitting", "RFIT")
	diagnoseField(dataset, "RPUD.rHydrant", "RHYD")
	diagnoseField(dataset, "RPUD.rLateralLine", "RLAT")
	diagnoseField(dataset, "RPUD.rNetworkStructure", "RNS")
	diagnoseField(dataset, "RPUD.rPressureMain", "RMN")
	diagnoseField(dataset, "RPUD.rSamplingStation", "RSS")
	diagnoseField(dataset, "RPUD.rServiceConnection", "RSC")
	diagnoseField(dataset, "RPUD.rSystemValve", "RSV")

def main():
	logMessage("Start")
	checkWater()
	checkSewer()
	checkReuse()
	logMessage("End")

if __name__ == "__main__":
    main()
