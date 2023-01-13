import board
import busio
import terminalio
import displayio
from adafruit_display_text import label
from adafruit_st7789 import ST7789
#from adafruit_bitmap_font import bitmap_font
from adafruit_display_shapes import roundrect

from src.fonts import Fonts


class Display:

    # Release any resources currently in use for the displays
    def __init__(self, tft_cs, tft_dc, spi_mosi, spi_clk):
        self.fonts=Fonts()



        displayio.release_displays()

        spi = busio.SPI(spi_clk, spi_mosi)

        display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs)
        self.display = ST7789(
            display_bus, rotation=90, width=240, height=135, rowstart=40, colstart=53
        )
        self.game = displayio.Group()
        self.successes = displayio.Group()
        self.successes.hidden=True
        #self.grid = displayio.Group()
        #self.grid.hidden=True
        self.icons = displayio.Group()
        self.ui = displayio.Group()
        self.ui.append(self.game)
        self.ui.append(self.successes)
        self.ui.append(self.icons)

        self.display.show(self.ui)
        self.switchUI(self.game)

        #self.gridText=label.Label(self.fonts.plex10, text=" "*1000, color=0xFFFFFF)
        #self.gridText.x = 0
        #self.gridText.y = 0
        #self.grid.append(self.gridText)



    def switchUI(self,ui):
        if ui=="game":
            self.game.hidden=False
            #self.grid.hidden=True
            self.successes.hidden=True
            self.icons.hidden=False
        elif ui=="successes":
            self.game.hidden=True
            #self.grid.hidden=True
            self.successes.hidden=False
            self.icons.hidden=False
        elif ui=="grid":
            self.game.hidden=True
            #self.grid.hidden=False
            self.successes.hidden=True
            self.icons.hidden=True

    def rectangle(self,x,y,w,h,r=0,color=0xFFFFFF):
        rectangle=roundrect.RoundRect(x,y,w,h,r,fill=color)
        self.game.append(rectangle)
        return rectangle

    def merriweather(self, text, x=0, y=0, size=20,color=0xFFFFFF, succUi=False):
        if size==10:
            font=self.fonts.merriweather10
        elif size==30:
            font=self.fonts.merriweather30
        else:
            font=self.fonts.merriweather20

        return self.showText(text,x,y,font,False,color,succUi)

    def plex(self, text, x=0, y=0, size=20, center=False,color=0xFFFFFF, succUi=False):
        if size==10:
            font=self.fonts.plex10
        elif size==30:
            font=self.fonts.plex30
        elif size==15:
            font=self.fonts.plex15
        elif size==14:
            font=self.fonts.italic15
        elif size==24:
            font=self.fonts.italic25
        elif size==19:
            font=self.fonts.italic20
        else:
            font=self.fonts.plex20

        return self.showText(text,x,y,font,center,color,succUi)

    def icon(self, code, x, y,color=0xFFFFFF, trueIcon=True, gridIcon=False):
        font=self.fonts.fork
        text_area = label.Label(font, text=code, color=color)

        text_area.x = x
        text_area.y = y


        if trueIcon:
            self.icons.append(text_area)
        #elif gridIcon:
        #    self.successes.append(text_area)
        else:
            self.game.append(text_area)
        return text_area

    def showText(self, text, x=0, y=0, font=terminalio.FONT, center=False, color=0xFFFFFF, succUi=False):
        #color =
        text_area = label.Label(font, text=text, color=color)

        if center:
            text_area.anchor_point=(0.5,1)
            text_area.anchored_position=(x,y)
        else:
            # Set the location
            text_area.x = x
            text_area.y = y

        if succUi:
            self.successes.append(text_area)
        else:
            self.game.append(text_area)
        return text_area



    """ color_bitmap = displayio.Bitmap(display.width, display.height, 1)
    color_palette = displayio.Palette(1)
    color_palette[0] = BACKGROUND_COLOR

    bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
    splash.append(bg_sprite)

    # Draw a smaller inner rectangle
    inner_bitmap = displayio.Bitmap(
        display.width - BORDER * 2, display.height - BORDER * 2, 1
    )
    inner_palette = displayio.Palette(1)
    inner_palette[0] = FOREGROUND_COLOR
    inner_sprite = displayio.TileGrid(
        inner_bitmap, pixel_shader=inner_palette, x=BORDER, y=BORDER
    )
    splash.append(inner_sprite)

    # Draw a label
    text = "Hello World!"
    text_area = label.Label(terminalio.FONT, text=text, color=TEXT_COLOR)
    text_width = text_area.bounding_box[2] * FONTSCALE
    text_group = displayio.Group(
        scale=FONTSCALE,
        x=display.width // 2 - text_width // 2,
        y=display.height // 2,
    )
    text_group.append(text_area)  # Subgroup for text scaling
    splash.append(text_group)

    while True:
        pass """
