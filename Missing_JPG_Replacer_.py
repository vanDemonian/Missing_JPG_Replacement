#!/usr/local/Cellar/python

"""
	This program iterates through multiple directories and finds gaps in the image sequence
	which it then fills with blank frames numbered according to the datetime of the image 
	that was missing.

	input files must be named according to the format below

		MONA2**_2015_07_26-15_55_13.jpg




"""
from PIL import Image
import calendar
import os, shutil
import dirwalk
from datetime import datetime, date, time, timedelta
import time


#_______________________________________________________________________________________________________
ScreenWidth = 1920
ScreenHeight = 1278

quality = 100
fileExt = '.jpg'

#inputDir = '/Volumes/Ent_One_1TB/DTLA_DATA/8_MONA/2015/'
inputDir = '/Volumes/DTLA_1_NavarreRiver_2_LakeStClair_3_LakeKingWilliam/STCLAIR_1920_copy'

black = (0,0,0)
fillColour = black

namePaths = []
namePaths2 = []

slotList = []
shotList = []
# this is the # of seconds between each DTLA DSLR capture. 
interval = 300.00

#_______________________________________________________________________________________________________

for root, dirs, files in os.walk(inputDir):
	for name in files:
		if name.endswith(fileExt):
			namePaths.append(os.path.join(root,name))

totalJPEGS = tJ = len(namePaths)

print "		"


#_______________________________________________________________________________________________________


def Filename_epochsecs(filename):
	#determines epoch seconds for entire datetime of filename
	Year = int(filename[-23:-19])
	Month= int(filename[-18:-16])
	Day = int(filename[-15:-13])
	#-------------------------------
	hour = int(filename[-12:-10])
	minute = int(filename[-9:-7])
	sec = int(filename[-6:-4])
	#-------------------------------
	datetime_in_Secs = (Year, Month, Day, hour, minute, sec, 0,0,0)
	dt_secs = calendar.timegm(datetime_in_Secs)

	return dt_secs


def Epochsecs_filename(epochsecs):
	#returns datetime based on epoch seconds
	newYMDhms 	= time.gmtime(epochsecs)

	newyear		= str(newYMDhms[0])
	newmonth	= str(newYMDhms[1])
	newday		= str(newYMDhms[2])
	newhour		= str(newYMDhms[3])
	newminute	= str(newYMDhms[4])
	newsecond	= str(newYMDhms[5])

	newfilename = str(newyear + '_' + str(newmonth).rjust(2).replace(' ','0') + '_' + str(newday).rjust(2).replace(' ','0') + '-' + str(newhour).rjust(2).replace(' ','0') + '_' + str(newminute).rjust(2).replace(' ','0') + '_' + str(newsecond).rjust(2).replace(' ','0') + '.jpg')

	return newfilename


class SHOT:

	def __init__(self, namePath):

		self.namePath = namePath
		self.sampleTime = Filename_epochsecs(namePath)

		return
	
class SLOT:

	def __init__(self, epochsecs, interval):

		self.midSlot   = epochsecs
		self.startSlot = self.midSlot - (interval/2)
		self.endSlot   = self.midSlot + (interval/2)
		self.hasShot   = 0
		self.SHOT      = SHOT

		return





location  = namePaths[0][-31:-23]

startSecs = Filename_epochsecs(namePaths[0])
startTime = Epochsecs_filename(startSecs)

endSecs   = Filename_epochsecs(namePaths[-1])
endTime	  = Epochsecs_filename(endSecs)

duration  = (endSecs - startSecs)


totalSlots = tS  = (duration / interval)
emptySlots = eS  =  (tS - tJ)




print "*_________________________________________________________________________________*"
print "		", location
print "start time  = " , startTime , " which is  ", startSecs, " since the epoch began"
print "end time    = " , endTime , " which is  ", endSecs, " since the epoch began "
print "		"
print "duration    = " , duration , " epoch seconds" , "        = " , (float(duration)/86400.00) , " days. "
print "total number of slots between start and end    = ", tS
print "total number of jpegs found                    = ", tJ
print "total number of empty slots to be filled       = ", eS
print "		"
print "		"



#________________________________________________________________________________________________________


t1  = float(Filename_epochsecs(namePaths[0]))

i = 0
while i <= tS:
	slot = SLOT(t1, interval) 
	slotList.append(slot)
	t1+=interval

	i+=1


for name in namePaths:
	shot = SHOT(name) 
	shotList.append(shot)


for SHOT in shotList:
	xx = SHOT.sampleTime
	print xx

	for SLOT in slotList:
		if SLOT.startSlot < xx and xx < SLOT.endSlot:
			SLOT.hasShot = 1
			SLOT.SHOT = SHOT.namePath


for SLOT in slotList:

	print SLOT.hasShot, "  ", SLOT.SHOT, "  ", SLOT.startSlot, "  ", SLOT.midSlot, "  ", SLOT.endSlot


a = 0
for SLOT in slotList:

	if SLOT.hasShot == 0:

		img = Image.new('RGB', (ScreenWidth, ScreenHeight), fillColour)
		newName = Epochsecs_filename(SLOT.midSlot)
		print a,"  newName   ", newName

		outpathName = inputDir  + '/' + location + newName
		img.save(outpathName, 'jpeg', quality=quality)
		a+=1













