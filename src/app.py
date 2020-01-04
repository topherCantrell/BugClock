import time

from clock_display import ClockDisplay
from rtc import RTC

display = ClockDisplay()
clock = RTC()

while True:
    
    hours,minutes,seconds = clock.get_time()
    display.set_time(hours,minutes)
    
    time.sleep(10)




import smbus

class ClockDisplay:
   
#      0
#    ----
#  5 |  | 1
#    ----   6
#  4 |  | 2
#    ---- . 7
#     3
#     
# Center colon is bit 1
#                       
#                             ?   A    B  colon  C    D           
#                             |   |    |    |    |    |
# bus.write_block_data(0x70, 15, [0,0, 0,0, 0,0, 0,0, 0,0])

    DIGITS = [
        0x3F, # 0
        0x06, # 1    
        0x5B, # 2            
        0x4F, # 3        
        0x66, # 4        
        0x6D, # 5        
        0x7D, # 6        
        0x07, # 7
        0x7F, # 8
        0x6F, # 9
    ]
    
    def __init__(self,address=0x70):
        self._bus = smbus.SMBus(1)
        self._address = address           
        
        self._bus.write_byte(0x70,0x21)
        self._bus.write_byte(0x70,0xEF)
        self._bus.write_byte(0x70,0x81)        
        self.set_digits(0,0, 0, 0,0)
        
    def set_digits(self,a,b,colon,c,d):
        # TODO: still not sure why I have to start writing at 15 instead of 0
        # The JS block writer needs the 0 instead of 15
        self._bus.write_block_data(0x70, 15, [a,0, b,0, colon,0, c,0, d,0])        
    
    def set_time(self,hours,minutes,ampm=True):
        
        pm_led = False
        
        if ampm and hours>12:
            pm_led = True
            hours -= 12
        
        hours_a = int(hours/10)
        hours_b = hours - hours_a*10
        mins_a = int(minutes/10)
        mins_b = minutes - mins_a*10
        
        raw_ha = ClockDisplay.DIGITS[hours_a]
        raw_hb = ClockDisplay.DIGITS[hours_b]
        raw_ma = ClockDisplay.DIGITS[mins_a]
        raw_mb = ClockDisplay.DIGITS[mins_b]
        
        if ampm and hours_a==0:
            raw_ha = 0
            
        if pm_led:
            raw_mb |= 128
            
        self.set_digits(raw_ha,raw_hb,2,raw_ma,raw_mb)

import smbus

class RTC:
    
    def __init__(self,address=0x68):
        
        self._bus = smbus.SMBus(1)
        self._address = address
        
        # Enable the battery backup
        self._bus.write_byte_data(self._address,2,0) 
                
    def get_time(self):
                
        seconds = self._bus.read_byte_data(self._address,3) & 0x7F
        minutes = self._bus.read_byte_data(self._address,4) & 0x7F
        hours = self._bus.read_byte_data(self._address,5) & 0x3F
        
        # From BCD
        seconds = (seconds>>4)*10 + (seconds&15)
        minutes = (minutes>>4)*10 + (minutes&15)
        hours = (hours>>4)*10 + (hours&15)
                       
        return (hours,minutes,seconds)
    
    def set_time(self,hours,minutes,seconds=0):
        
        # To BCD
        seconds = (int(seconds/10)<<4) + (seconds%10)
        minutes = (int(minutes/10)<<4) + (minutes%10)
        hours = (int(hours/10)<<4) + (hours%10)
        
        self._bus.write_byte_data(self._address,5,hours)
        self._bus.write_byte_data(self._address,4,minutes)
        self._bus.write_byte_data(self._address,3,seconds)
        