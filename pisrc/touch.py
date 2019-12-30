import smbus

class Touch:
    
    def __init__(self,address=0xFF):
        self._bus = smbus.SMBus(1)
        self._address = address        
        