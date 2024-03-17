from langcard import *
from adafruit_simple_text_display import SimpleTextDisplay


import microcontroller
# print(microcontroller.cpu.frequency)
# print(microcontroller.cpu.temperature)

def display_text(
    title: Optional[str] = None,
    title_scale: int = 3,
    title_length: int = 80,
    text_scale: int = 1,
    font: Optional[str] = None,
    ) -> SimpleTextDisplay:
    return SimpleTextDisplay(
            title=title,
            title_color=SimpleTextDisplay.YELLOW,
            title_scale=title_scale,
            title_length=title_length,
            text_scale=text_scale,
            font=font,
            colors=(SimpleTextDisplay.GREEN,
                    SimpleTextDisplay.GREEN,
                    SimpleTextDisplay.GREEN,
                    SimpleTextDisplay.GREEN,
                    SimpleTextDisplay.GREEN,
                    SimpleTextDisplay.GREEN,
                    SimpleTextDisplay.GREEN,
                    SimpleTextDisplay.AQUA,),
            display=display,
        )



text_lines = display_text(title=" Sys Info")


# while True:
text_lines[1].text=" CPY   : " + os.uname().version
text_lines[2].text=" CPU   : " + os.uname().sysname
text_lines[3].text=" Freq  : " + str(microcontroller.cpu.frequency/1000000)+ 'MHz'
text_lines[4].text=" HW ver: " + HW_VER
text_lines[5].text=" SW ver: " + "0.1.0"
text_lines[6].text=" DISP  : " +LCD_MODEL

# text_lines[7].text=os.uname().machine



text_lines.show()
time.sleep(1.0)

while True:
    time.sleep(0.1)
    key = getkey()
    if key:
        returnMainPage()
        break
#         supervisor.set_next_code_file('code.py')
#         supervisor.reload()
gc.collect()
pass
