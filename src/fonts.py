from adafruit_bitmap_font import bitmap_font


class Fonts:

    def __init__(self):
        self.merriweather30 = bitmap_font.load_font("/fonts/Merriweather-Regular-30.pcf")
        self.merriweather20 = bitmap_font.load_font("/fonts/Merriweather-Regular-20.pcf")
        self.merriweather10 = bitmap_font.load_font("/fonts/Merriweather-Regular-10.pcf")

        self.plex30= bitmap_font.load_font("/fonts/IBMPlexMono-Medium-30.pcf")
        self.plex20= bitmap_font.load_font("/fonts/IBMPlexMono-Medium-20.pcf")
        self.plex15= bitmap_font.load_font("/fonts/IBMPlexMono-Medium-15.pcf")
        self.plex10= bitmap_font.load_font("/fonts/IBMPlexMono-Medium-10.pcf")

        self.italic15= bitmap_font.load_font("/fonts/IBMPlexMono-LightItalic-15.pcf")
        self.italic20= bitmap_font.load_font("/fonts/IBMPlexMono-LightItalic-20.pcf")
        self.italic25= bitmap_font.load_font("/fonts/IBMPlexMono-LightItalic-25.pcf")

        self.fork= bitmap_font.load_font("/fonts/forkawesome-12.pcf")
