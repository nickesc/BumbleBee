from digitalio import DigitalInOut, Direction, Pull
import time

class Button:

    def __init__(self, buttonPin, label):

        self.pin=buttonPin
        self.label=label

        self.btn = DigitalInOut(self.pin)
        self.btn.direction = Direction.INPUT
        self.btn.pull = Pull.UP


    def pressed(self):
        return not self.btn.value

    def checkButton(self):

        print(self.label, "is up")

        pressed=False

        while not pressed:
            if not self.btn.value:
                print(self.label, "is down")
                pressed=True
            else:
                pass

            time.sleep(0.1)
