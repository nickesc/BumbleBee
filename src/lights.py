# dummy led class with a False value
class dummyled:
    value=False

# RGB LED class
class RGB:

    # try to import adafruit rgb led
    try:
        import adafruit_rgbled
    except:
        pass

    # set available rgb colors
    class Colors:
        WHITE=(255,255,255)
        BLACK=(0,0,0)
        RED=(255,0,0)
        GREEN=(0,255,0)
        BLUE=(0,0,255)
        YELLOW=(255,255,0)
        CYAN=(0,255,255)
        MAGENTA=(255,0,255)

    def __init__(self, targetR, targetG, targetB, color1=Colors.RED):

        # initialize with power off
        self.powered=False

        # set rgb pins
        self.rPin=targetR
        self.gPin=targetG
        self.bPin=targetB

        # set the initial color
        self.color=color1

    # print an error message for if LED is not usable/found
    def error(self):
        print("LED is unreachable -- color: ", self.color, ", Power:", self.powered)

    # set the color of the LED
    def setColor(self,rgbTuple):

        # set the color variable to the rgb tuple
        self.color=rgbTuple

        # if the LED is powered, try to set the color, otherwise print an error
        if self.powered:
            try:
                self.led.color=self.color
            except:
                self.error()

        # return the current color
        return self.color

    # turn the LED on
    def on(self):

        # if the LED is not powered
        if not self.powered:

            # set the LED to powered
            self.powered=True

            # try to create an adafruit rgb led and set the color to the current color, otherwise print an error
            try:
                self.led=self.adafruit_rgbled.RGBLED(self.rPin, self.gPin, self.bPin, invert_pwm=True)
                self.led.color=self.color
            except:
                self.error()

    # turn the LED off
    def off(self):

        # set the LED power to false
        self.powered=False

        # try to deinitialize the adafruit rgb led, otherwise print an error
        try:
            self.led.deinit()
        except:
            self.error()

    # toggle the LED based on the current power state
    def toggle(self):
        if self.powered:
            self.off()
        else:
            self.on()

# Board LED class
class LED:

    # try to import digitalio
    try:
        import digitalio
    except:
        print("USING DUMMY LED")

    # initialize the power status as false
    status = False
    def __init__(self, target, power=False):

        # try to initialize the LED object using digitalio, otherwise use a dummyled
        try:
            self.led = self.digitalio.DigitalInOut(target)
            self.led.direction = self.digitalio.Direction.OUTPUT
        except:
            self.led=dummyled()

        # set the starting power status
        self.status = power

        # sync the LED
        self.sync()

    # sync the LED value to the power status
    def sync(self):
        self.led.value = self.status

    # set the power status to on and sync the LED
    def on(self):
        self.status = True
        self.sync()

    # set the power status to off and sync the LED
    def off(self):
        self.status = False
        self.sync()

    # toggle the power status and sync the LED
    def toggle(self):
        self.status = not self.status
        self.sync()
