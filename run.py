#!/usr/bin/env python

import logging
import logging.handlers
import argparse
import RPi.GPIO as GPIO

from four20lcd import *
from pogodynka import *
from dht11 import *
from cpuInfo import *


inPin1,inPin2 = 15,16
GPIO.setmode(GPIO.BOARD)
GPIO.setup(inPin1,GPIO.IN)
GPIO.setup(inPin2,GPIO.IN)


global i
i = 0

def buttonUpEventHandler (pin):
    global i
    print "handling buttonUp event"
    i=i+1
    
def buttonDownEventHandler (pin):
    global i
    print "handling buttonDown event"
    i=i-1
    
GPIO.add_event_detect(inPin1,GPIO.FALLING)
GPIO.add_event_callback(inPin1,buttonUpEventHandler)

GPIO.add_event_detect(inPin2,GPIO.FALLING)
GPIO.add_event_callback(inPin2,buttonDownEventHandler)

# Deafults
LOG_FILENAME = "/tmp/myservice.log"
LOG_LEVEL = logging.INFO  # Could be e.g. "DEBUG" or "WARNING"

# Define and parse command line arguments
parser = argparse.ArgumentParser(description="wStation")
parser.add_argument("-l", "--log", help="file to write log to (default '" + LOG_FILENAME + "')")

# If the log file is specified on the command line then override the default
args = parser.parse_args()
if args.log:
        LOG_FILENAME = args.log

# Configure logging to log to a file, making a new file at midnight and keeping the last 3 day's data
# Give the logger a unique name (good practice)
logger = logging.getLogger(__name__)
# Set the log level to LOG_LEVEL
logger.setLevel(LOG_LEVEL)
# Make a handler that writes to a file, making a new file at midnight and keeping 3 backups
handler = logging.handlers.TimedRotatingFileHandler(LOG_FILENAME, when="midnight", backupCount=3)
# Format each log message like this
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
# Attach the formatter to the handler
handler.setFormatter(formatter)
# Attach the handler to the logger
logger.addHandler(handler)



class MyLogger(object):
        def __init__(self, logger, level):
                """Needs a logger and a logger level."""
                self.logger = logger
                self.level = level

        def write(self, message):
                # Only log if there is a message (not just a new line)
                if message.rstrip() != "":
                        self.logger.log(self.level, message.rstrip())

if args.log:
# Replace stdout with logging to file at INFO level
    sys.stdout = MyLogger(logger, logging.INFO)
# Replace stderr with logging to file at ERROR level
    sys.stderr = MyLogger(logger, logging.ERROR)

print("Run my personal Weather station")

lcd = four20lcd()
pogodynka = Pogodynka()
lcd.lcd_display_line('Stacja Pogodowa',1)
lcd.lcd_display_line('    Mateusza   ',2)
sleep(2)
lcd.lcd_clear()




wStationData = ['                   ','                    ','                    ','                    ','                    ','                    ','                    ','                    ']
while True:
  wStationData[0] = strftime("%H:%M %d %B %Y", localtime())
  wStationData[1] = pogodynka.getCloudElement()
  wStationData[2] = getTemperatureAndHumudityInterior()
  wStationData[3] = "Tout=" + pogodynka.getDailyTemperatureFromPogdynka() + " Wind=" + pogodynka.getDailyWindFromPogodynka()
  wStationData[4] = "CPU=" + getCpuUse() + " Temp=" + getCpuTemperature() + "*C"
  print(wStationData[3])
  lcd.lcd_display_line(wStationData[i], 1)
  lcd.lcd_display_line(wStationData[i+1], 2)
  lcd.lcd_display_line(wStationData[i+2], 3)
  lcd.lcd_display_line(wStationData[i+3], 4)
