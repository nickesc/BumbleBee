import busio
import terminalio
import displayio
from adafruit_display_text import label, bitmap_label
from adafruit_st7789 import ST7789
from adafruit_display_shapes import roundrect

from src.fonts import Fonts


class Display:


    def __init__(self, tft_cs, tft_dc, spi_mosi, spi_clk):
        self.fonts=Fonts()

        # Release any resources currently in use for the displays
        displayio.release_displays()

        # create the spi buss
        spi = busio.SPI(spi_clk, spi_mosi)

        # create the display
        display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs)
        self.display = ST7789(
            display_bus, rotation=90, width=240, height=135, rowstart=40, colstart=53
        )

        # create the gameuis
        self.game = displayio.Group()
        self.successes = displayio.Group()
        self.grid = displayio.Group()
        self.icons = displayio.Group()

        # hide hidden gameuis
        self.successes.hidden=True
        self.grid.hidden=True

        # create the device ui and add the gameuis
        self.ui = displayio.Group()
        self.ui.append(self.game)
        self.ui.append(self.grid)
        self.ui.append(self.successes)
        self.ui.append(self.icons)

        # show the display and switch to the game ui
        self.display.show(self.ui)
        self.switchUI(self.game)

    # switch to the desired gameui and hide the others
    def switchUI(self,ui):
        if ui=="game":
            self.game.hidden=False
            self.grid.hidden=True
            self.successes.hidden=True
            self.icons.hidden=False
        elif ui=="successes":
            self.game.hidden=True
            self.grid.hidden=True
            self.successes.hidden=False
            self.icons.hidden=False
        elif ui=="grid":
            self.game.hidden=True
            self.grid.hidden=False
            self.successes.hidden=True
            self.icons.hidden=True

    # draw a rectangle to the display
    def rectangle(self,x,y,w,h,r=0,color=0xFFFFFF):

        # create a round rectangle object
        rectangle=roundrect.RoundRect(x,y,w,h,r,fill=color)

        # add it to the game ui
        self.game.append(rectangle)

        # return the rectangle
        return rectangle

    # draw text to the display with [IBM Plex](https://github.com/IBM/plex)
    def plex(self, text, x=0, y=0, size=20, center=False,color=0xFFFFFF, succUi=False, gridUi=False, bit=False):

        # set font based on size and italics
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

        # return an adafruit label object from the show text function
        return self.showText(text,x,y,font,center,color,succUi,gridUi,bit)

    # draw an icon to the screen with [Fork Awesome Bitmap Icon Font](https://emergent.unpythonic.net/01606790241)
    def icon(self, code, x, y,color=0xFFFFFF, trueIcon=True, gridIcon=False):

        # set the icon font
        font=self.fonts.fork

        # create an adafruit label with the icon
        text_area = label.Label(font, text=code, color=color)

        # set the icon coordinates
        text_area.x = x
        text_area.y = y

        # if the icon is the grid icon, add it to the successes ui
        if gridIcon:
            self.successes.append(text_area)

        # if it is a true icon, add it to the icons ui
        if trueIcon:
            self.icons.append(text_area)

        # otherwise, add it to the game ui
        if not gridIcon and not trueIcon:
            self.game.append(text_area)

        # return the adafruit label
        return text_area

    # create and show text on the display using adafruit labels
    def showText(self, text, x=0, y=0, font=terminalio.FONT, center=False, color=0xFFFFFF, succUi=False, gridUi=False,bit=False):

        # if it should be a bitmap label, cretae a bitmap label, otherwise create a regular label
        if bit:
            text_area = bitmap_label.Label(font, text=text, color=color)
        else:
            text_area = label.Label(font, text=text, color=color)

        # if it should be centered, set the anchor points and anchored coordinates
        if center:
            text_area.anchor_point=(0.5,1)
            text_area.anchored_position=(x,y)

        # otherwise set the label coordinates
        else:
            text_area.x = x
            text_area.y = y

        # add successes ui labels to the successes ui
        if succUi:
            self.successes.append(text_area)

        # add grid ui labels to the grid ui
        if gridUi:
            self.grid.append(text_area)

        # add game ui labels to the game ui
        if not gridUi and not succUi:
            self.game.append(text_area)

        # return the adafruit label
        return text_area
