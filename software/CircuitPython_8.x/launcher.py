from langcard import  *
import os
import time
import board
import displayio
import adafruit_imageload
import terminalio 
from adafruit_display_text import label
from adafruit_display_shapes.rect import Rect
from adafruit_display_shapes.roundrect import RoundRect
import audiocore
import audiobusio

# Icon Positions
ICONSIZE = 48
SPACING = 20
LEFTSPACE = 35
# LEFTSPACE = 5
TOPSPACE = 10
TEXTSPACE = 10
ICONSACROSS = 4
ICONSDOWN = 2
PAGEMAXFILES = ICONSACROSS * ICONSDOWN  # For the chosen display, this is the
#                                     maximum number of file icons that will fit
#                                     on the display at once (display dependent)
# File Types
BLANK = 0
FILE = 1
DIR = 2
BMP = 3
WAV = 4
PY = 5
RIGHT = 6
LEFT = 7

filecount = 0
xpos = LEFTSPACE
ypos = TOPSPACE
# Use the builtin display
 
WIDTH = display.width
HEIGHT = display.height
ts = None
display.show(None)
# Create base display group
launchgroup = displayio.Group()
display.show(launchgroup)
# Load the bitmap (this is the "spritesheet")
sprite_sheet, palette = adafruit_imageload.load("/images/icons.bmp")

background = Rect(0, 0, WIDTH - 1, HEIGHT - 1, fill=0x000000)
launchgroup.append(background)
     
# Create enough sprites & labels for the icons that will fit on screen
sprites = []
labels = []
for i in range(PAGEMAXFILES):
    sprite = displayio.TileGrid(sprite_sheet, pixel_shader=palette,
                                width=1, height=1, tile_height=48,
                                tile_width=48,)
    sprite.x = xpos + (SPACING + ICONSIZE) * (i%ICONSACROSS)
    sprite.y = ypos + (ICONSIZE + SPACING + TEXTSPACE)*(i//ICONSACROSS%ICONSDOWN)
    sprites.append(sprite)  # Append the sprite to the sprite array
    launchgroup.append(sprite)
    filelabel = label.Label(terminalio.FONT, color=0xFFFFFF)
    labels.append(filelabel)
    launchgroup.append(filelabel)

print(len(sprites))

selectbox = RoundRect(LEFTSPACE-5+(SPACING + ICONSIZE)*0, TOPSPACE-6 +(ICONSIZE + SPACING + TEXTSPACE)*0, ICONSIZE+10, ICONSIZE+28, 5, fill=None, outline=0x70ff50,stroke=2)
launchgroup.append(selectbox)

pagenumlabel = label.Label(terminalio.FONT, color=0xffffff)
pagenumlabel.anchor_point = (1.0, 1.0)
pagenumlabel.anchored_position = (display.width-1, display.height-1)
pagenumlabel.text=' / '
launchgroup.append(pagenumlabel)

 







def playwave(filename):
    audiopwr_on()
    i2s = audiobusio.I2SOut(AUDIO_BCK,AUDIO_WS,AUDIO_DATA)
    try :
        wave_file = open(filename, "rb")
        wave = audiocore.WaveFile(wave_file)
        i2s.play(wave)
        while i2s.playing:
            pass
        wave.deinit()
        wave_file.close()
        wave_file=None
        gc.collect()
         
    except Exception as e : 
        print (e)
    i2s.deinit()
    audiopwr_off()
    pass


class Options:
    def __init__(self,path='/',options_per_page = PAGEMAXFILES):
        self.path = path
        self.options = self.get_files(path)
        self.options_per_page = options_per_page
        # Define the current page
        self.current_page = 0
        # Define the starting index for the current page
        self.start_index = self.current_page * self.options_per_page

        # Define the ending index for the current page
        self.end_index = self.start_index + self.options_per_page
        self.current_options = self.options[self.start_index:self.end_index]
        
    def get_files(self,base):
        files = os.listdir(base)
        file_names = []
        for isdir, filetext in enumerate(files):
            if not filetext.startswith("."):
                if filetext not in ('boot_out.txt', 'System Volume Information'):
                    stats = os.stat(base + filetext)
                    isdir = stats[0] & 0x4000
                    if isdir:
                        file_names.append((filetext, True))
                    else:
                        file_names.append((filetext, False))
        return file_names
    
    def page_update(self):
        self.start_index = self.current_page * self.options_per_page
        self.end_index = self.start_index + self.options_per_page
        self.current_options = self.options[self.start_index:self.end_index]



displaybase = "/"  # Get file names in base directory            
opt = Options(displaybase,PAGEMAXFILES)

 

 
 
def display_current_page(options):
    for i,option in enumerate(options.current_options):

        filename, dirfile = options.current_options[i]
        if dirfile:
            filetype = DIR
        elif filename.endswith(".bmp"):
            filetype = BMP
        elif filename.endswith(".wav"):
            filetype = WAV
        elif filename.endswith(".py"):
            filetype = PY
        else:
            filetype = FILE
        
        # Set icon location information and icon type
        
        sprites[i].x = xpos + (SPACING + ICONSIZE) * (i%ICONSACROSS)
        sprites[i].y = ypos + (ICONSIZE + SPACING + TEXTSPACE)*(i//ICONSACROSS%ICONSDOWN)
        sprites[i][0] = filetype
        #
        # Set filename
        labels[i].x = sprites[i].x
        labels[i].y = sprites[i].y + ICONSIZE +10
        # The next line gets the filename without the extension, first 11 chars
        labels[i].text = filename.rsplit('.', 1)[0][0:10]
        
      
#         if i == index:
#             print(f"> {i+1}. {option}")
#         else:
#             print(f"  {i+1}. {option}")
        
    length = len(options.current_options)
    if (length<options.options_per_page):
        free = options.options_per_page - length
        for i in range(length,options.options_per_page):
            print(i) 
            sprites[i][0] = BLANK
            labels[i].text = ''
            
    selectbox.x =  LEFTSPACE-5+(SPACING + ICONSIZE)*(index%ICONSACROSS)
    selectbox.y =  TOPSPACE-6 +(ICONSIZE + SPACING + TEXTSPACE)*(index//ICONSACROSS)        
    print(f"Page {options.current_page+1}/{len(options.options)//options.options_per_page+1}")
    pagenumlabel.text=f"{options.current_page+1}/{len(options.options)//options.options_per_page+1}"
    
    
    
 
    
# Display the initial page
index = 0
display_current_page(opt)     
     
while True :
    key =getkey()
    if key == KEY_RIGHT or key =='d'or key =='D':
        index += 1
        if index >= len(opt.current_options):
            index = 0
            opt.current_page += 1
        if opt.current_page > len(opt.options)//opt.options_per_page:
            opt.current_page = 0
        opt.page_update()      
        display_current_page(opt)
    elif key == KEY_LEFT or key =='a'or key =='A':
        index -= 1
        if index < 0:
            opt.current_page -= 1
            index = 0
            
            
        if opt.current_page < 0:
            opt.current_page = len(opt.options)//opt.options_per_page

        opt.page_update()       
        display_current_page(opt)
    elif key == KEY_DOWN or key =='s'or key =='S':
        index += ICONSACROSS
        if index >= len(opt.current_options):
            index = 0
            opt.current_page += 1
            if opt.current_page > len(opt.options)//opt.options_per_page:
                opt.current_page = 0
            opt.page_update()
        display_current_page(opt)
    elif key == KEY_UP or key =='w'or key =='W':
        index -= ICONSACROSS
        if index < 0:
            index = 0
            opt.current_page -= 1
            if opt.current_page < 0:
                opt.current_page = len(opt.options)//opt.options_per_page
            opt.page_update()
        display_current_page(opt)
    elif key == 'q':
        break
    elif key == KEY_OK or key== KEY_ENTER:        
        if opt.current_options[index][1]==True:#dir
            print(f'open directory: {opt.current_options[index][0]}')
            displaybase = displaybase +opt.current_options[index][0]+'/'
            print(displaybase)
            opt.options = opt.get_files(displaybase)
            opt.page_update()
            index = 0
            display_current_page(opt)
            
             
            pass
        elif opt.current_options[index][0].endswith(".py"):
            startApp=displaybase+ opt.current_options[index][0]
            supervisor.set_next_code_file(startApp)
            print("\033[2J",end="") #clear screen
            print("Free memory:"+str(gc.mem_free()))
            print("Next boot set to:")
            print(startApp)
            try:
                gc.collect()
                exec(open(startApp).read())
            except Exception as err:
                print(err)
            print("Program finished ...")
            print("\033[2J",end="") #clear screen
            gc.collect()
            display.show(launchgroup)
            pass
        elif opt.current_options[index][0].endswith(".wav"):
            try:
                playwave(displaybase+ opt.current_options[index][0])
            except Exception as e:
                print(e)
        else:
            print('unsupported filetype')
    
    elif key==KEY_FUN3:
        if displaybase=='/':
            pass
        else:
            
            segments  = displaybase.split('/')
#             print(segments )
            base=''
            for i,seg in enumerate( segments):
                if i <len(segments)-2 :
                    base = base+seg+'/'
            
            displaybase = base
            opt.options = opt.get_files(displaybase)
            opt.page_update()
            index = 0
            display_current_page(opt)
            
#             print(displaybase)
            pass
    elif key == KEY_FUN1:
        if opt.current_options[index][1]==False:
             
            startApp=displaybase+ opt.current_options[index][0]
            print(startApp)
            try:
                from pye_lcd import pye
                print("start edit")
            
                ret = pye(startApp)
            except Exception as e:
                print(e)
            returnMainPage()
    #         opt.options = opt.get_files(displaybase)
    #         opt.page_update()
    #         display_current_page(opt)
    #         index = 0
        
        
        
    time.sleep(0.02)
    
 





