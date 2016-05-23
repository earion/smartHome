import lcddriver
import lcd_moc
import sys
import platform

class four20lcd:
  screenContent = ['','','','','']

  def __init__(self):
    if platform.processor() != 'x86_64':
      self.lcd = lcddriver.lcd()
      self.lcd.lcd_clear()
    else:
      self.lcd = lcd_moc.LcdMoc()
      
  def lcd_clear(self):
    self.lcd.lcd_clear()
    for idx in range(0, len(self.screenContent)):
      self.screenContent[idx] = ''
      
   #clear line
  def lcd_clear_line(self,line):
    self.lcd.lcd_display_string('                    ',line)
  
  #Print line on lcd screen if line was changed        
  def lcd_display_line(self,string,line):
     if self.screenContent[line] != string:
       self.lcd_clear_line(line)
       self.lcd.lcd_display_string(string,line) 
       self.screenContent[line] = string
       


