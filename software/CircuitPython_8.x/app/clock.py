# SPDX-FileCopyrightText: 2019 Sommersoft
# SPDX-FileCopyrightText: Copyright (c) 2021 Jeff Epler for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

# Simple demo of reading and writing the time for the PCF8563 real-time clock.
# Change the if False to if True below to set the time, otherwise it will just
# print the current date and time every second.  Notice also comments to adjust
# for working with hardware vs. software I2C.

import time
import board
import busio
from langcard import *
from adafruit_display_text import label

from adafruit_pcf8563.pcf8563 import PCF8563

WEEK_COLOR_NOW = 0xCCCCCC
WEEK_COLOR_NOTNOW=0x444444
CALENDAR_COLOR = 0xCCCCCC

# Change to the appropriate I2C clock & data pins here!
# i2c = busio.I2C(board.GP1, board.GP0)

# Create the RTC instance:
rtc = PCF8563(i2c)

# Lookup table for names of days (nicer printing).
days = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")


# pylint: disable-msg=using-constant-test
if False:  # change to True if you want to set the time!
    #                     year, mon, date, hour, min, sec, wday, yday, isdst
    t = time.struct_time((2024, 3, 17, 14, 9, 0, 6, -1, -1))
    # you must set year, mon, date, hour, min, sec and weekday
    # yearday is not supported, isdst can be set but we don't do anything with it at this time
    print("Setting time to:", t)  # uncomment for debugging
    rtc.datetime = t
    print()
# pylint: enable-msg=using-constant-test



display.show(None)
main_group = displayio.Group()

from adafruit_bitmap_font import bitmap_font
font_file = "fonts/LeagueSpartan-Bold-16.bdf"
font = bitmap_font.load_font(font_file)
# font = terminalio.FONT
time_now = rtc.datetime
# label

colon_label = label.Label(terminalio.FONT, color=0xffffff, scale=6)
colon_label.anchor_point = (0.0, 0.0)
colon_label.anchored_position = (160, 30)
colon_label.text = ":"


hour_label = label.Label(terminalio.FONT, color=0x00ff00, scale=8)
hour_label.anchor_point = (0.0, 0.0)
hour_label.anchored_position = (60, 20)
hour_label.text = "{:0>2d}".format(time_now.tm_hour)

minute_label = label.Label(terminalio.FONT, color=0x00ffff, scale=8)
minute_label.anchor_point = (0.0, 0.0)
minute_label.anchored_position = (200, 20)
minute_label.text ="{:0>2d}".format(time_now.tm_min)


calendar_label = label.Label(terminalio.FONT, color=CALENDAR_COLOR, scale=2)
calendar_label.anchor_point = (0.0, 0.0)
calendar_label.anchored_position = (160, 140)
calendar_label.text = "{}-{}-{}".format(time_now.tm_year, time_now.tm_mon, time_now.tm_mday)

# gc_label = label.Label(terminalio.FONT, color=0xff00ff, scale=1)
# gc_label.anchor_point = (0.5, 0.0)
# gc_label.anchored_position = (display.width / 2+40, 110)
# gc_label.text = "{}KB".format(gc.mem_free()/1024)


main_group.append(colon_label)
main_group.append(hour_label)
main_group.append(minute_label)
main_group.append(calendar_label)
# main_group.append(gc_label)


week_id = time_now.tm_wday
week_label=[]
weeks = ("MON","TUE","WED","THU","FRI","SAT","SUN")
for i in range(7):
    wlabel = label.Label(font, color=WEEK_COLOR_NOTNOW, scale=1)
    wlabel.anchor_point = (0.0, 0.0)
    wlabel.anchored_position = (0, i*25)
    wlabel.text = f"{weeks[i]}"
    week_label.append(wlabel)
    main_group.append(wlabel)
    
week_label[week_id].color = WEEK_COLOR_NOW


display.show(main_group)



now =  time.monotonic()
old=now
# Main loop:
while True:
    
    now =  time.monotonic()
    if (now-old) >= 1.0:
        old = now  
 
        if rtc.datetime_compromised:
            print("RTC unset")
        else:
            print("RTC reports time is valid")
        t = rtc.datetime
        # print(t)     # uncomment for debugging
        print(
            "The date is {} {}/{}/{}".format(
                days[int(t.tm_wday)], t.tm_mday, t.tm_mon, t.tm_year
            )
        )
        print("The time is {}:{:02}:{:02}".format(t.tm_hour, t.tm_min, t.tm_sec))
        time.sleep(1)  # wait a second
        
        colon_label.color = 0xffffff - colon_label.color
        hour_label.text = "{:0>2d}".format(t.tm_hour)
        minute_label.text = "{:0>2d}".format(t.tm_min)
        calendar_label.text = "{}-{}-{}".format(t.tm_year, t.tm_mon, t.tm_mday)
    
    time.sleep(0.01)
    key = getkey()    
    if key:
        if key=='q':
            print('exit')
            returnMainPage()     
        else: 
            pass
   
    
    