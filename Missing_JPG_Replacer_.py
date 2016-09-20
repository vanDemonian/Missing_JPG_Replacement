#!/usr/local/Cellar/python

"""
	This program iterates through multiple directories and finds gaps in the image sequence
	which it then fills with blank frames numbered according to the datetime of the image 
	that was missing.

	input files must be named according to the format below

		MONA2**_2015_07_26-15_55_13.jpg




"""


from __future__ import generators
import glob
from PIL import Image
from PIL import ImageStat
from PIL import ImageChops
from PIL.ExifTags import TAGS, GPSTAGS
import string, sys, traceback, datetime, time, calendar
import EXIF, os, shutil
import dirwalk
from PIL import *
from numpy import *
from datetime import datetime, date, time, timedelta
import time



#_______________________________________________________________________________________________________
ScreenWidth = 1920
ScreenHeight = 1278

quality = 100
fileExt = '.jpg'

#inputDir = '/Volumes/Ent_One_1TB/DTLA_DATA/8_MONA/2015/'
inputDir = '/Users/pyDev/Documents/JPG_REFINERY/Frame_Replacer_Test_Data'

black = (0,0,0)
fillColour = black

namePaths = []
namePaths2 = []

# this is the # of seconds between each DTLA DSLR capture. 
interval = 300.00





#_______________________________________________________________________________________________________

for root, dirs, files in os.walk(inputDir):
	for name in files:
		if name.endswith(fileExt):
			namePaths.append(os.path.join(root,name))

totalJPEGS = len(namePaths)
print "		"


#_______________________________________________________________________________________________________


def Filename_epochsecs(filename):

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

	newYMDhms 	= time.gmtime(epochsecs)

	newyear		= str(newYMDhms[0])
	newmonth	= str(newYMDhms[1])
	newday		= str(newYMDhms[2])
	newhour		= str(newYMDhms[3])
	newminute	= str(newYMDhms[4])
	newsecond	= str(newYMDhms[5])

	newfilename = str(newyear + '_' + str(newmonth).rjust(2).replace(' ','0') + '_' + str(newday).rjust(2).replace(' ','0') + '-' + str(newhour).rjust(2).replace(' ','0') + '_' + str(newminute).rjust(2).replace(' ','0') + '_' + str(newsecond).rjust(2).replace(' ','0') + '.jpg')

	return newfilename


def Gap_filler(interval, gapStart, gapEnd, location, ScreenWidth, ScreenHeight, fillColour, inputDir):

		print "gapStart   ", gapStart, "   ", Epochsecs_filename(gapStart)
		print "gapEnd     ", gapEnd, "   ", Epochsecs_filename(gapEnd)

		gapSize = gapEnd - gapStart
		print "gapSize   ", gapSize
		fillNumber = gapSize/interval
		print "fillNumber   ", fillNumber
		fNum = int(math.floor(fillNumber)) - 1
		print "fNum   ", fNum

		x = 1
		while x <= (fNum):

			img = Image.new('RGB', (ScreenWidth, ScreenHeight), fillColour)
			fillTime = gapStart +  (x * interval)
			print "fillTime   ", fillTime
			newName = Epochsecs_filename(fillTime)
			print "newName   ", newName

			outpathName = inputDir  + '/' + location + newName
			img.save(outpathName, 'jpeg', quality=quality)

			x+=1





location  = namePaths[0][-31:-23]

startSecs = Filename_epochsecs(namePaths[0])
endSecs   = Filename_epochsecs(namePaths[-1])
startTime = Epochsecs_filename(startSecs)
endTime	  = Epochsecs_filename(endSecs)

duration  = (endSecs - startSecs)

tJ  = totalJPEGS
mSP = maxSamplesPossible  = int(duration / interval) + 1
tSM = totalSamplesMissing = int(maxSamplesPossible - tJ)

print "*_________________________________________________________________________________*"
print "		"
print "start time  = " , startSecs, " which was  ", startTime
print "end time    = " , endSecs, " which was  ", endTime
print "duration    = " , duration , " epoch seconds" , " = " , float(duration/86400) , " days. "
print "total number of potential samples        = ", maxSamplesPossible
print "total number of jpegs found              = ", tJ
print "total number of samples to be re-created = ", totalSamplesMissing
print "		"
print "		"



#________________________________________________________________________________________________________




i = 0
while i < (tJ):

	#print namePaths[i]
	#print namePaths[i+1]
	
	t1  = Filename_epochsecs(namePaths[i])
	#print t1
	t2  = Filename_epochsecs(namePaths[i+1])
	#print t2
	gap = int(t2 - t1)

	#print "gap found   ", gap
	#print "________________________"
	#print "   "

	if gap >= (interval * 2):
		Gap_filler(interval, t1, t2, location, ScreenWidth, ScreenHeight, fillColour, inputDir)





		print "		"



	


	i+=1

















