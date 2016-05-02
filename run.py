#!/usr/bin/python
 
import lcddriver
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
	lcd.lcd_display_string(strftime("%H:%M", localtime()),1)
	lcd.lcd_display_string(strftime("%d %B %Y",localtime()),2)	
	lcd.lcd_display_string(getDailyCloudFromPogodynka()[0:20], 3)
	lcd.lcd_display_string(getDailyTemperatureFromPogdynka(), 4)
	sleep(1)
