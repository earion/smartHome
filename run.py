#!/usr/bin/python

from time import *
from itertools import cycle

import lcddriver
import lcd_moc
import platform
from pogodynka import *
from dht11 import *


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
