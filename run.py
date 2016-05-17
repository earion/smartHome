#!/usr/bin/env python
import lcddriver
import lcd_moc
import logging
import logging.handlers
import argparse
import sys

from pogodynka import *
from dht11 import *




# Deafults
LOG_FILENAME = "/tmp/myservice.log"
LOG_LEVEL = logging.INFO  # Could be e.g. "DEBUG" or "WARNING"

# Define and parse command line arguments
parser = argparse.ArgumentParser(description="My simple Python service")
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

# Replace stdout with logging to file at INFO level
sys.stdout = MyLogger(logger, logging.INFO)
# Replace stderr with logging to file at ERROR level
sys.stderr = MyLogger(logger, logging.ERROR)

logger.info("Run my personal Weather station")

if platform.processor() != 'x86_64':
    lcd = lcddriver.lcd()
    lcd.lcd_clear()
else:
    lcd = lcd_moc.LcdMoc()

pogodynka = Pogodynka()
while 1:
    lcd.lcd_display_string(strftime("%H:%M %d %B %Y", localtime()), 1)
    lcd.lcd_display_string(pogodynka.getCloudElement(), 2)
    lcd.lcd_display_string(getTemperatureAndHumudityInterior(), 3)
    wind = pogodynka.getDailyWindFromPogodynka()
    lcd.lcd_display_string("Tout=" + pogodynka.getDailyTemperatureFromPogdynka() + " Wind=" + wind, 4)
    sleep(1.5)
    lcd.lcd_clear_line(2)
