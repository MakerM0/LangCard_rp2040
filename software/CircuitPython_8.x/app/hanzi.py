from langcard import *
from adafruit_bitmap_font import bitmap_font
from displayio import Bitmap
from adafruit_display_text import label
FONTSCALE = 1
BACKGROUND_COLOR = 0x000000
TEXT_COLOR = 0x00FF0F
font = bitmap_font.load_font("fonts/Fontquan-XinYiGuanHeiTi-Regular.pcf", Bitmap)


# Make the display context
splash = displayio.Group()
display.root_group = splash

color_bitmap = displayio.Bitmap(display.width, display.height, 1)
color_palette = displayio.Palette(1)
color_palette[0] = BACKGROUND_COLOR

bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)

# Draw a label


title = "小池"
title_area = label.Label(font, text=title, color=0xff0000,scale =2)
title_area.anchor_point = (0.0, 0.0)
title_area.anchored_position = (10, 10)

author="朝代：宋朝 | 作者：杨万里"
author_area = label.Label(font, text=author, color=0xff00ff)
author_area.anchor_point = (0.0, 0.0)
author_area.anchored_position = (10, 50)

text = """泉眼无声惜细流，树阴照水爱晴柔。
小荷才露尖尖角，早有蜻蜓立上头。"""
text_area = label.Label(font, text=text, color=TEXT_COLOR)
text_area.anchor_point = (0.0, 0.0)
text_area.anchored_position = (10, 80)

splash.append(title_area)  # Subgroup for text scaling
splash.append(author_area)  # Subgroup for text scaling
splash.append(text_area)  # Subgroup for text scaling
 
 
while True:
    time.sleep(0.01)
    key = getkey()
    if key=='q':
        returnMainPage()