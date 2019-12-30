import time

from clock_display import ClockDisplay
from rtc import RTC

display = ClockDisplay()
clock = RTC()

while True:
    
    hours,minutes,seconds = clock.get_time()
    display.set_time(hours,minutes)
    
    time.sleep(10)
