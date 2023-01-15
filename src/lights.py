class dummyled:
    value=False

class RGB:
    try:
        import adafruit_rgbled
    except:
        print("USING DUMMY RGB")

    class Colors:
        WHITE=(255,255,255)
        BLACK=(0,0,0)
        RED=(255,0,0)
        GREEN=(0,255,0)
        BLUE=(0,0,255)
        YELLOW=(255,255,0)
        CYAN=(0,255,255)
        MAGENTA=(255,0,255)


    def __init__(self, targetR, targetG, targetB, color1=Colors.WHITE):

        self.powered=False

        self.rPin=targetR
        self.gPin=targetG
        self.bPin=targetB

        self.color=color1

    def error(self):
        print("LED is unreachable -- color: ", self.color, ", Power:", self.powered)

    def setColor(self,rgbTuple):
        self.color=rgbTuple
        if self.powered:
            try:
                self.led.color=self.color
            except:
                self.error()
        return self.color

    def on(self):
        if not self.powered:
            self.powered=True
            try:
                self.led=self.adafruit_rgbled.RGBLED(self.rPin, self.gPin, self.bPin, invert_pwm=True)
                self.led.color=self.color
            except:
                self.error()

    def off(self):
        self.powered=False
        try:
            self.led.deinit()
        except:
            self.error()

    def toggle(self):
        if self.powered:
            self.off()
        else:
            self.on()


class LED:
    try:
        import digitalio
    except:
        print("USING DUMMY LED")

    status = False
    def __init__(self, target, power=False):

        try:
            self.led = self.digitalio.DigitalInOut(target)
            self.led.direction = self.digitalio.Direction.OUTPUT
        except:
            self.led=dummyled()

        self.status = power
        self.sync()

    def sync(self):
        self.led.value = self.status

    def on(self):
        self.status = True
        self.sync()

    def off(self):
        self.status = False
        self.sync()

    def toggle(self):
        self.status = not self.status
        self.sync()
