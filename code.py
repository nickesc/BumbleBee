#import asyncio
#import board
#import digitalio
#import storage
#import supervisor
#from src.light import Light
from src.spellingBee import Bee
#import src.files as files
#import csv


#led = Light(board.LED)



def main():

    testBee = Bee(new=False)
    testBee.guessCLI()

    """ with open("dictionary/dictionary.csv", 'r') as dictionaryCsvFile:
        # Write the dictionary to the file in JSON format


        x=input(">> ").lower()

        for line in dictionaryCsvFile:
            if x==line.strip():
                print("Found")
                break """


if __name__ == "__main__":
    main()





#async def connectedLED():
#    while True:
#        if supervisor.runtime.usb_connected:
#            led.on()
#        else:
#            led.off()

#async def main():

    #connectedTask=asyncio.create_task(connectedLED())

    #try:
    #    with open("/testFile.txt", "w") as f:
    #        f.write("test run")
    #except:
    #    print("Device connected -- currently, the Bumblebee has a read only file-system, unplug it from your computer to write data to the device")

    #await asyncio.gather(connectedTask)

#asyncio.run(main())



