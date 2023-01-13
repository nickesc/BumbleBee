from src.spellingBee import Bee

def main():

    testBee = Bee(new=False, on_board=True)
    testBee.controller.startGame()

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



