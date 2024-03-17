import time
import board
import busio
import digitalio
import analogio
import keypad
import displayio
import os
import supervisor
from digitalio import DigitalInOut
from micropython import const
import supervisor
import storage
import sdcardio
import  gc
import terminalio 

HW_VER = "1.1"



LCD_MODEL= "tft_1.9"
 
if LCD_MODEL == 'tft_1.9':
    from adafruit_st7789 import ST7789
else:
    pass





#硬件引脚定义

#spi
SPI_SCLK= board.GP18
SPI_MOSI= board.GP19 
SPI_MISO= board.GP20

#I2C DEVICES
I2C_SCL = board.GP1
I2C_SDA = board.GP0


#LCD

LCD_SCLK = SPI_SCLK
LCD_MOSI = SPI_MOSI
LCD_CS = board.GP17
LCD_BL = board.GP6
LCD_DC = board.GP21




#sdcard
SD_MOSI = SPI_MOSI
SD_MISO = SPI_MISO
SD_SCLK = SPI_SCLK
SD_CS = board.GP3


#battery
BAT_PIN = board.A3





KEY_ENTER = '\x0a'
KEY_DEL = '\x08'
KEY_ALT = 0x82
KEY_CAPS_R = 0x83
KEY_CAPS_L = 0x84

KEY_OK = '\r'


KEY_SPEAKER=0x88#speaker


KEY_WRITE = '\x13' #KEY_WRITE
KEY_NONE = '\x00'
KEY_UP  = '\x87'
KEY_DOWN = '\x88'
KEY_LEFT = '\x89'
KEY_RIGHT = '\x90'
KEY_QUIT = '\x11'
KEY_MIC = KEY_DOWN

KEY_SYM='$'
KEY_FUN1=KEY_WRITE
KEY_FUN2='edit'
KEY_FUN3=KEY_QUIT
KEY_FUN4=0x87
KEY_SPEAKER = KEY_RIGHT

km = keypad.KeyMatrix(
    row_pins=(board.GP22,board.GP23,board.BUTTON,board.LED),
    column_pins = (board.GP10,board.GP11,board.GP12,board.GP13,board.GP14,board.GP15,board.GP16,board.GP28,board.GP27,board.GP26)
    )


# 按键map的序号，从左到右，从上到下
PPC_KEYMAP=(30,31,32,33,34,35,36,37,38,39,
            20,21,22,23,24,25,26,27,28,29,
            10,11,12,13,14,15,16,17,18,19,
            0,1,2,3,4,5,6,7,8,9 )


PPC_KEY_NAMES=(
               "q","w","e","r","t","y","u","i","o","p",
               "a","s","d","f","g","h","j","k","l",KEY_DEL,
               KEY_ALT,"z","x","c","v","b","n","m",KEY_UP,KEY_ENTER,
               KEY_CAPS_L,"_","=","("," ",".",")",KEY_LEFT,KEY_DOWN,KEY_RIGHT
    
    )

PPC_KEY_NAMES_CAPS=(
               "Q","W","E","R","T","Y","U","I","O","P",
               "A","S","D","F","G","H","J","K","L",KEY_DEL,
               KEY_ALT,"Z","X","C","V","B","N","M",KEY_UP,KEY_ENTER,
               KEY_CAPS_L,"_","=","("," ",".",")",KEY_LEFT,KEY_DOWN,KEY_RIGHT
    
    )

PPC_KEY_NAMES_ALT=(
               "#","1","2","3","+","-","/","\\",":",";",
               "*","4","5","6","%","@","`","'",'"',KEY_DEL,
               KEY_ALT,"7","8","9","~","!","&","?","^",KEY_ENTER,
               KEY_CAPS_L,"|","0","["," ",",","]","<","$",">"
    
    )
# Create an event we will reuse over and over.
event = keypad.Event()

# Release the existing display, if any
displayio.release_displays()


spi = busio.SPI(SPI_SCLK,SPI_MOSI,SPI_MISO)

while not spi.try_lock():
    pass
spi.configure(baudrate=40000000) # Configure SPI for 24MHz
spi.unlock()


#sd
sd_valid = False
sdcard=""
try:
    sdcard = sdcardio.SDCard(spi, SD_CS)
    sd_valid = True
except Exception as r:
    print("no sd")
    sd_valid = False
if  sd_valid:   

    vfs = storage.VfsFat(sdcard)
    print(vfs)
    storage.mount(vfs, "/sd")
    # print("Files on filesystem:")
    # print("====================")
    # print_directory("/sd")

display = None

#display
if LCD_MODEL == 'mlcd_sharp':
    pass

elif LCD_MODEL == 'mlcd_jdi':
    pass

elif LCD_MODEL =='tft_1.9':    
    display_bus = displayio.FourWire(spi, command=LCD_DC, chip_select=LCD_CS,baudrate = 24000000)
    display = ST7789(    display_bus, rotation=270, width=320, height=170, colstart=35,backlight_pin=LCD_BL, backlight_on_high = True)
    display.root_group[0].hidden = False
    display.root_group[1].hidden = True # logo
    display.root_group[2].hidden = True # status bar
#     display.root_group[0].y = 0
#     TERMINAL_HEIGHT=display.height
#     #display.root_group.scale = SCALE
#     supervisor.reset_terminal(display.width,TERMINAL_HEIGHT) #130 #260 #55
    print("lcd init ok")
    pass


VSYS_ADC = analogio.AnalogIn(BAT_PIN)


 

def returnMainPage():
    display.show(None)  
    supervisor.set_next_code_file("code.py")
    supervisor.reload()






# tp_motion = digitalio.DigitalInOut(TP_MOTION)
# tp_motion.direction = digitalio.Direction.INPUT
# tp_motion.pull = digitalio.Pull.UP


# kb_backlight = digitalio.DigitalInOut(TP_BACKLIGHT)
# kb_backlight.direction = digitalio.Direction.OUTPUT
# kb_backlight.value = True
# time.sleep(0.2)
# kb_backlight.value = False

i2c = busio.I2C(I2C_SCL,I2C_SDA, frequency=400000,timeout=255)

while not i2c.try_lock():
    pass 
i2c.unlock()

 

key_names=[PPC_KEY_NAMES,PPC_KEY_NAMES_CAPS,PPC_KEY_NAMES_ALT]
layout=0
alt = False
lastlayout=layout
def getkey():
    global layout,alt,lastlayout

    keys=KEY_NONE 
    if km.events.get_into(event):
        if event.pressed :
            if event.key_number in PPC_KEYMAP:
                index = PPC_KEYMAP.index(event.key_number)
#                 print(key_names[layout][index])
                keys = key_names[layout][index]
#                 print(keys)            
                if keys==KEY_CAPS_L:
                    if layout==1:
                        layout=0
                        lastlayout=layout
                    else:
                        layout=1
                        lastlayout=layout
                    return  
                if keys==KEY_ALT:
                    alt = not alt
                    if alt:
                        layout=2
                    else:
                        layout = lastlayout
                        
                    return  
                return keys
    # try :
    #     direction =get_touch()
    
    #     if direction:
    #         return direction
 
    # except:
    #     pass
            
    return  


def show_terminal():
    display.show(None)
    # TERMINAL_HEIGHT=display.height+20
    # display.root_group.scale = 1
    #     
    # display.root_group[0].hidden = False
    # display.root_group[1].hidden = True # logo
    # display.root_group[2].hidden = True # status bar
    supervisor.reset_terminal(display.width,display.height)
    # display.root_group[0].y = 0



    display.show(display.root_group)


 
