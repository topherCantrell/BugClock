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
#                                 A    B  colon  C    D           
#                                 |    |    |    |    |
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
        self._address = address;              
        self._bus.write_block_data(self._address, 0x21, [])
        self._bus.write_block_data(self._address, 0xEF, [])
        self._bus.write_block_data(self._address, 0x81, [])        
        self.set_digits(0,0, 0, 0,0)
        
    def set_digits(self,a,b,colon,c,d):
        self._bus.write_block_data(0x70, 15, [a,0, b,0, colon,0, c,0, d,0])
    
    def set_time(self,hours,minutes,ampm):
        hours_a = int(hours/10)
        hours_b = hours - hours_a
        mins_a = int(minutes/10)
        min_b = minutes - mins_a
        

clock = ClockDisplay()
#clock.set_digits(clock.DIGITS[0],clock.DIGITS[1],2,clock.DIGITS[2],clock.DIGITS[3])    
#clock.set_digits(clock.DIGITS[4],clock.DIGITS[5],2,clock.DIGITS[6],clock.DIGITS[7])
#clock.set_digits(clock.DIGITS[8],clock.DIGITS[9],2,clock.DIGITS[8],clock.DIGITS[9])