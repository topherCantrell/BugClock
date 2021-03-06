
class RTC:
    
    def __init__(self,i2c,address=0x68):
        
        self._i2c = i2c        
        self._address = address
        
        # Enable the battery backup
        self._i2c.write_data(self._address,2,bytes([0]))
                
    def get_time(self):
                
        seconds = self._i2c.read(self._address,3) & 0x7F
        minutes = self._i2c.read(self._address,4) & 0x7F
        hours = self._i2c.read(self._address,5) & 0x3F
        
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
        
        self._i2c.write_data(self._address,5,bytes([hours]))
        self._i2c.write_data(self._address,4,bytes([minutes]))
        self._i2c.write_data(self._address,3,bytes([seconds]))
