from langcard import *

try:
    from pye_lcd import pye
    ret = pye('settings.toml')
except:
    pass
returnMainPage()
