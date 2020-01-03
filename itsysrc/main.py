import board
import busio
import os

i2c = busio.I2C(board.SCL, board.SDA)
i2c.try_lock()
 
i2c.writeto(0x70,b'\x21')
i2c.writeto(0x70,b'\xEF')
i2c.writeto(0x70,b'\x81')

# Hi Lo
i2c.writeto(0x70,b'\x00\x76\x00\x10\x00\x00\x00\x38\x00\x5C\x00\x00\x00\x00\x00\x00\x00')

i2c.unlock()