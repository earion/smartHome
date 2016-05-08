#!/usr/bin/python
 
import lcddriver
import string
import os
from datetime import datetime
from tzlocal import get_localzone
from time import *
from pogodynka import *
from cpuInfo import *
from itertools import cycle
from dht11 import *
from math import *
 
lcd = lcddriver.lcd()
lcd.lcd_clear()

var = 1
cloudIter = 0
cloud = cycle(getDailyCloudFromPogodynka())
while var == 1: 
	cloudIter+=1
	lcd.lcd_display_string(strftime("%H:%M %d %B %Y", localtime()),1)
	if(cloudIter %40==0):
	    cloud = cycle(getDailyCloudFromPogodynka())	
	#get sliding if longer than 24 signs
	lcd.lcd_display_string(cloud.next(),2)
	lcd.lcd_display_string(getTemperatureAndHumudityInterior(),3)
	wind = getDailyWindFromPogodynka().strip()
	lcd.lcd_display_string("Tout=" + getDailyTemperatureFromPogdynka() + " Wind=" + wind, 4)
	sleep(1.5)
