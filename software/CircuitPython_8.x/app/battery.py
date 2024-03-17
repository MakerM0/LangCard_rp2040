'''
v0.1.1
    20231020
    add 'quit action'


v0.1.0
    20231008

'''



from langcard import *
import time
import board
import analogio


display.show(None)

TERMINAL_HEIGHT=display.height+20
display.root_group.scale = 1

display.root_group[0].hidden = False
display.root_group[1].hidden = True # logo
display.root_group[2].hidden = True # status bar
supervisor.reset_terminal(display.width,TERMINAL_HEIGHT)
display.root_group[0].y = 0

display.show(display.root_group)

analog_pin = VSYS_ADC

def get_voltage(pin):
    return (pin.value * 3.3) / 65535 *3

get_voltage(analog_pin)
time.sleep(0.5)

now = 0
old = 0

while True:
    now =  time.monotonic()
    if (now-old) >= 2.0:
        old= now
        print(f'\033[32;1m{get_voltage(analog_pin)} V')

    key = getkey()
    if key:
        print('exit')
        returnMainPage()
    time.sleep(0.2)
