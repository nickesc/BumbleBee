import asyncio

class led:
    value=False

class Light:




    status = False

    def sync(self):
        self.led.value = self.status

    def __init__(self, target, power=False):
        self.led = led()
        #self.led.direction = digitalio.Direction.OUTPUT

        self.status = power
        self.sync()

    def on(self):
        self.status = True
        print("LED",self.status)
        self.sync()

    def off(self):
        self.status = False
        print("LED",self.status)
        self.sync()

    def toggle(self):
        self.status = not self.status
        print("LED",self.status)
        self.sync()

    async def blink(self, interval, count=10):
        x = 0.0
        while x != count:
            self.toggle()
            x += 0.5
            await asyncio.sleep(interval)
        self.off()
