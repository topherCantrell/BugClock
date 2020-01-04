import board
import busio
import time

from hardware import I2CBase
from clock_display import ClockDisplay
from rtc import RTC

class I2CBus(I2CBase):
    
    def __init__(self):
        self._i2c = busio.I2C(board.SCL, board.SDA)
        self._i2c.try_lock()
    
    def read(self,address,register):
        self._i2c.writeto(address,bytes([register]),stop=False)
        ret = bytearray(1)
        self._i2c.readfrom_into(address,ret)
        return ret[0]
    
    def write(self,address,value):
        self._i2c.writeto(address,bytes([value]))
        
    def write_data(self, address, register, data):
        ndata = bytes([register]) + data
        self._i2c.writeto(address,ndata)

i2c = I2CBus()

display = ClockDisplay(i2c,0x70)
clock = RTC(i2c,0x68)

while True:
        
    hours,minutes,seconds = clock.get_time()
    display.set_time(hours,minutes)
    
    time.sleep(10)
    
#i2c.unlock()