#!/usr/bin/python
 
import lcddriver
import string
import os
from datetime import datetime
from tzlocal import get_localzone
from time import *
from pogodynka import *
 
lcd = lcddriver.lcd()
lcd.lcd_clear()

def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    return(res.replace("temp=","").replace("'C\n",""))

def getCPUuse():
    return(str(os.popen("top -n1 | awk '/Cpu\(s\):/ {print $2}'").readline().strip(\
)))
var = 1
while var == 1: 
	lcd.lcd_display_string(strftime("%H:%M %d %B %Y", localtime()),1)
	cloud = getDailyCloudFromPogodynka().strip(',').split(' ');	
	lcd.lcd_display_string(cloud[0],2)
	lcd.lcd_display_string(cloud[1],3)
	wind = getDailyWindFromPogodynka().strip()
	lcd.lcd_display_string(getDailyTemperatureFromPogdynka() + " " + wind, 4)
	sleep(1)
