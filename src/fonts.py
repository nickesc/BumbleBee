from adafruit_bitmap_font import bitmap_font

class Fonts:
    def __init__(self):

        #  load ibm plex font in 30,20,15,10 pixel sizes
        self.plex30= bitmap_font.load_font("/fonts/IBMPlexMono-Medium-30.pcf")
        self.plex20= bitmap_font.load_font("/fonts/IBMPlexMono-Medium-20.pcf")
        self.plex15= bitmap_font.load_font("/fonts/IBMPlexMono-Medium-15.pcf")
        self.plex10= bitmap_font.load_font("/fonts/IBMPlexMono-Medium-10.pcf")

        #  load ibm plex font in 15,20,25 pixel sizes and italics
        self.italic15= bitmap_font.load_font("/fonts/IBMPlexMono-LightItalic-15.pcf")
        self.italic20= bitmap_font.load_font("/fonts/IBMPlexMono-LightItalic-20.pcf")
        self.italic25= bitmap_font.load_font("/fonts/IBMPlexMono-LightItalic-25.pcf")

        # load fork awesome font at 12 pixel size
        self.fork= bitmap_font.load_font("/fonts/forkawesome-12.pcf")
