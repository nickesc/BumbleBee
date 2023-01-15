from digitalio import DigitalInOut, Direction, Pull
import time

class Button:

    def __init__(self, buttonPin, label):

        # set the button pin and label
        self.pin=buttonPin
        self.label=label

        # initialize a button object using digital io
        self.btn = DigitalInOut(self.pin)
        self.btn.direction = Direction.INPUT
        self.btn.pull = Pull.UP

    # return whether the button is pressed
    def pressed(self):
        return not self.btn.value

    # function to test if the button is working
    def checkButton(self):

        # print that the button is up to start and set pressed to false
        print(self.label, "is up")
        pressed=False

        # while the button is not pressed
        while not pressed:

            # if the value of the button changes, set pressed to true and print that the button is down
            if not self.btn.value:
                print(self.label, "is down")
                pressed=True
            # otherwise pass
            else:
                pass

            # sleep for button debouncing
            time.sleep(0.1)
