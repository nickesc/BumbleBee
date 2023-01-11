import digitalio
import asyncio


class Light:

    status = False

    def sync(self):
        self.led.value = self.status

    def __init__(self, target, power=False):
        self.led = digitalio.DigitalInOut(target)
        self.led.direction = digitalio.Direction.OUTPUT

        self.status = power
        self.sync()

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
