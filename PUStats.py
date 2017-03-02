##this is a prototype script for generating stats
import arcpy
from Tkinter import *

arcpy.env.workspace = "Database Connections/RPUD_TESTDB.sde"

##point feature
#total number
#total input by user x
#total input with time range y


##line feature
#total length
#total input by user x
#total input with time range y

arcpy.env.overwriteOutput = True

#input 1 - feature class
inData = "RPUD.WaterDistributionNetwork/RPUD.wPressureMain" 
#input 2 - output feature class
outTable = "C:/data/Junk.gdb/lenSumTest"
#input 3 - editor
editor = "LIZ"
#input 4 - time range
timeStart = ""
timeEnd = ""
whereClause = "EDITEDBY = '{0}'".format(editor)
# whereClause = "EDITEDBY = '{0}' AND EDITEDON >= timestamp \'{1}\' AND EDITEDON <= timestamp \'{2}\'".format(editor, timeStart, timeEnd)


arcpy.MakeFeatureLayer_management(inData, "WMN", whereClause)
arcpy.Statistics_analysis("WMN", outTable, [["SHAPE.LEN", "SUM"]])


class Application(Frame):
	def calStats(self):

	def createWidgets(self):
		self.QUIT = Button(self)
		self.QUIT["text"] = "Quit"
		self.QUIT["fg"] = "red"
		self.QUIT["command"] = self.quit

		self.QUIT.pack({"side": "left"})

		self.calStats = Button(self)
		self.calStats["text"] = "Go"
		self.calStats["command"] = self.calStats

		self.calStats.pack({"side": left})