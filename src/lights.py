import digitalio
import asyncio
import adafruit_rgbled
import time

class dummyled:
    value=False

class RGB:

    color=(255,255,255)

    def __init__(self, targetR, targetG, targetB, color1=(255,255,255)):

        self.powered=False

        self.rPin=targetR
        self.gPin=targetG
        self.bPin=targetB

        self.color=color1

    def error(self):
        print("LED is unreachable -- color: ", self.color, ", Power:", self.powered)

    def setColor(self, r, g, b):
        self.color=(r,g,b)
        if self.powered:
            try:
                self.led.color=self.color
            except:
                self.error()
        return self.color

    def on(self, onColor=color):
        self.powered=True
        try:
            self.led=adafruit_rgbled.RGBLED(self.rPin, self.gPin, self.bPin, invert_pwm=True)
            self.color=onColor
            self.led.color=self.color
        except:
            self.error()

    def off(self):
        self.powered=False
        try:
            self.led.deinit()
        except:
            self.error()


class LED:

    status = False
    def __init__(self, target, power=False):

        try:
            self.led = digitalio.DigitalInOut(target)
            self.led.direction = digitalio.Direction.OUTPUT
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

    async def blink(self, interval, count=10):
        x = 0.0
        while x != count:
            self.toggle()
            x += 0.5
            await asyncio.sleep(interval)
        self.off()
