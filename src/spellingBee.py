import json
import random
import time

# import game resources
import src.files as files
from src.guessCodes import Codes

# try to import circuitpython modules
try:
    import board
    import gc
    import displayio
    import storage
    from src.buttons import Button
    from src.display import Display
    from src.lights import RGB,LED

# otherwise import a dummy board
except Exception as e:
    print(e)
    from dummy.board import board

class BeeState:

    # instantiate BeeState variables
    buzzword=""
    keyletter=""
    letterlist=[]
    wordlist={}
    score=0
    guessSuccess=[]
    guessFail=[]

    def __init__(self, circuitpython):

        # read the game state from game files
        with open(files.getBuzzword(circuitpython)) as buzzFile:
            self.buzzword=buzzFile.readlines()[0].strip()
        with open(files.getKeyletter(circuitpython)) as keyFile:
            self.keyletter=keyFile.readlines()[0].strip()
        with open(files.getLetterlist(circuitpython)) as letterFile:
            for letter in letterFile:
                self.letterlist.append(letter.strip())
        with open(files.getWordlist(circuitpython)) as wordFile:
            self.wordlist=json.load(wordFile)

        with open(files.getGuessSuccess(circuitpython)) as successFile:
            for succ in successFile:
                self.guessSuccess.append(succ.strip())
        with open(files.getGuessFail(circuitpython)) as failFile:
            for fail in failFile:
                self.guessFail.append(fail.strip())

        # for each success in the state's guess successes, add the guess's score from the word list to the state score
        for success in self.guessSuccess:
            self.score=self.score+self.wordlist[success]

class Bee:

    # set the length of the dictionary
    dictLen=8823

    #circuitPython=False

    # instantiate the dictionaries to empty objects
    dictionary={}
    buzzCandidates={}

    # instantiate the game variables
    buzzword=""
    keyletter=""
    letterlist=[]
    wordlist={}

    # instantiate the guess lists
    guessSuccess=[]
    guessFail=[]

    # instantiate the score variable
    score=0

    # set up a controller variable
    controller=None


    # create the microcontroller object -- handles the hardware initialization as well as the game
    class Controller:

        # initialize the hardware
        def initHardware(self):

            # create the light objects
            self.boardLed = LED(board.LED)
            self.frontRgb = RGB(board.GP6,board.GP7,board.GP8)

            # create the button objects and adds them to a buttons list
            self.A= Button(board.GP12, "a")
            self.B= Button(board.GP13, "b")
            self.X= Button(board.GP14, "x")
            self.Y= Button(board.GP15, "y")
            self.buttons=[self.A, self.B, self.X, self.Y]

            # create the display object
            self.display=Display(tft_cs = board.GP17, tft_dc = board.GP16, spi_mosi = board.GP19, spi_clk = board.GP18)

        # checks each button in an list and returns their pressed states
        def checkButtons(self, buttons):

            # create a list of button states by checking the pressed value of each
            pressed=[]
            for button in buttons:
                pressed.append(button.pressed())

            # return the list of button states
            return pressed

        # set alert text and color from a guess code
        def getShortCode(self,code,alert):
            if code==0 or code==3:
                alert.color=0xFF0000
                return "not found"
            elif code==1:
                alert.color=0x00FF00
                return "found"
            elif code==2:
                alert.color=0xFFFF00
                return "already found"
            elif code==4:
                alert.color=0xFF0000
                return "missing keyletter"
            elif code==5:
                alert.color=0xFF0000
                return "empty"
            elif code==6:
                alert.color=0xFF0000
                return "too short"
            elif code==7:
                alert.color=0x00FF00
                return "pangram!"
            elif code==10:
                alert.color=0x00FF00
                return "buzzword!"
            else:
                alert.color=0xFF0000
                return "error: bad guess code"

        # print the currently selected letter for REPL monitoring
        def printCurrLetter(self,letterIndex):
            print(" "+("   "*letterIndex)+self.Bee.letterlist[letterIndex])
            return (" "*letterIndex)+self.Bee.letterlist[letterIndex]

        # move the letter selector
        def moveCursorX(self,cursor,interval):
            # add the interval to the current x coordinate of the cursor
            cursor.x=cursor.x+interval

        # print the current guess for REPL monitoring
        def printGuess(self, guess):
            print(guess)
            return guess

        # test if there are any successes in the guessSuccess list
        def testSucc(self,successList,successIndex):
            # try to return the current success index, otherwise return and empty string
            try:
                return successList[successIndex]
            except:
                return ""

        # set latter labels to the current letterlist
        def setLetterLabels(self, labels):

            # for each letter in the label list
            index=0
            for label in labels:
                # set the label to the letter with the same index
                label.text=self.Bee.letterlist[index].upper()
                index+=1

        # update the scores on various screens
        def updateScoreDisplay(self,score,gotten,succ,found):

            # update the score on the game and successes screens
            score.text=str(self.Bee.score)
            succ.text="Score: "+str(self.Bee.score)

            # update the number found on the game and successes screen
            gotten.text=str(len(self.Bee.guessSuccess))+"/"+str(len(self.Bee.wordlist))
            found.text="Found: "+str(len(self.Bee.guessSuccess))+"/"+str(len(self.Bee.wordlist))

        # update the game on startup and newgame
        def updateGame(self, labels, score, gotten,succ,found):

            # build the hint grid
            self.buildGrid()

            # reset scores
            self.updateScoreDisplay(score,gotten,succ,found)

            # set letter labels
            self.setLetterLabels(labels)

            # run the garbage collector
            gc.collect()
            print("Memory 4:", gc.mem_free())

        # build the hint grid and set the grid screen
        def buildGrid(self):

            # get the current grid
            gridInfo=self.Bee.createGrid()

            # delete the current gridui and remove it from memory
            self.display.ui.remove(self.display.grid)
            try:
                del self.display.grid
                gc.collect()
                print("Memory 3:", gc.mem_free())
            except:
                pass

            # create a new gridui
            self.display.grid = displayio.Group()
            self.display.ui.append(self.display.grid)
            self.display.grid.hidden=True

            # set formatting parameters for the grid
            boldSize=15
            columnSize=14
            xStart=8
            xEnd=232
            yStart=20
            yInterval=16
            xInterval=(xEnd-xStart)/(len(gridInfo[self.Bee.keyletter]))

            # create an empty row list
            rows=[]

            # for each letter in the grid
            index=0
            for letter in gridInfo:
                # skip the middle row to leave it for the keyletter
                if index==3:
                    index+=1

                # if the letter is not the keyletter or total
                if letter!="$" and letter!=self.Bee.keyletter:
                    # add a new row to the list with the first cell as the letter of the row
                    rows.append(
                        {
                            "row":{
                                "letter": letter,
                                "height":yStart+(index*yInterval),
                                "cells":[
                                    self.display.plex(letter,xStart,yStart+(index*yInterval),boldSize,center=True,color=0xFFFFFF,gridUi=True),
                                    ]
                                }
                            }
                        )

                    # for each word length for the letter in the grid
                    lengthIndex=0
                    for length in gridInfo[letter]:
                        # get the text for the label -- the number of words associated with the word length
                        text=str(gridInfo[letter][length])

                        # set the text to a - if there are no words for that length
                        if text=='0':
                            text="-"

                        # create the label and add the cell to the gridui
                        self.display.plex(text,xStart+((lengthIndex+1)*xInterval),yStart+(index*yInterval),columnSize,center=True,color=0xFFFFFF,gridUi=True)
                        lengthIndex+=1

                    index+=1

            # add a new row to the list for totals with a $ in the first cell
            rows.append(
                {
                    "row":{
                        "letter": "$",
                        "height":yStart+(index*yInterval),
                        "cells":[
                            self.display.plex("$",xStart,yStart+(index*yInterval),boldSize,center=True,color=0xFFFFFF,gridUi=True),
                            ]
                        }
                    }
                )
            # for each word length total
            lengthIndex=0
            for length in gridInfo["$"]:
                # get the text for the label -- the total number of words for each word length
                text=str(gridInfo["$"][length])

                # set the text to a - if there are no words for that length
                if text=='0':
                    text="-"

                # if we're on the total-total cell, move the value 4 pixels to the left and add a $ to the front
                extra=0
                if length=="$":
                    text="$"+text
                    extra=-4

                # create the label and add the cell to the gridui
                self.display.plex(text,xStart+((lengthIndex+1)*xInterval)+extra,yStart+(index*yInterval),columnSize,center=True,color=0xFFFFFF,gridUi=True)
                lengthIndex+=1

            # add a new row for the keyletter
            rows.insert(3,
                {
                    "row":{
                        "letter": self.Bee.keyletter,
                        "height":yStart+(3*yInterval),
                        "cells":[
                            self.display.plex(self.Bee.keyletter,xStart,yStart+(3*yInterval),boldSize,center=True,color=0xFFFFFF,gridUi=True),
                            ]
                        }
                    }
                )

            # for each keyletter word length
            lengthIndex=0
            for length in gridInfo[self.Bee.keyletter]:
                # get the text for the label -- the number of words associated with the word length
                text=str(gridInfo[self.Bee.keyletter][length])

                # set the text to a - if there are no words for that length
                if text=='0':
                    text="-"

                # create the label and add the cell to the gridui
                self.display.plex(text,xStart+((lengthIndex+1)*xInterval),yStart+(3*yInterval),columnSize,center=True,color=0xFFFFFF,gridUi=True)
                lengthIndex+=1

        # start the game loop on the controller
        def startGame(self):

            # turn on the thinking rgb
            self.frontRgb.setColor(self.frontRgb.Colors.RED)
            self.frontRgb.on()

            # set up the alert state
            alerting=False
            alertStart=0


            print('''\nBumblebee Dev Console:\n
    Use X to move the letter selector left, use A to move the letter selector right. Press B to select
    the current letter and add it to the guess string, press Y to delete the last character in the guess
    string. Hold down B to submit a guess, hold down A to shuffle the letters, hold down Y to see the
    words guessed successfully, hold X to generate a new game\n''')

            # set the guess to empty
            guess=""

            # put the letter selector at the beginning
            letterIndex=0
            maxIndex=len(self.Bee.letterlist)-1

            # REPL monitoring
            print("Letters:",self.Bee.letterlist)
            print("Keyletter:", self.Bee.keyletter)
            print("")

            # set up the game's button icons on the different screens
            leftIcon=self.display.icon("\uf0d9", 3,100)
            rightIcon=self.display.icon("\uf0da", 232,100)
            backIcon=self.display.icon("\uf191", 3,10)
            checkIcon=self.display.icon("\uf14a", 222,10,trueIcon=False)
            gridIcon=self.display.icon("\uf00a", 222,10,trueIcon=False,gridIcon=True)

            # set up the letter selector and guess input field on the game screen
            curr=self.display.plex("_", x=30, y=120, size=30, center=True)
            curr.hidden=True
            guessInput=self.display.plex(" "*30, x=5, y=45, size=24)
            line=self.display.rectangle(5,65,230,3)

            # set up the score and fraction found parts of the game screen
            score=self.display.plex("     ",193,75,size=14)
            gotten=self.display.plex("     ",10,75,size=14)

            # set up the alert label
            alert=self.display.plex(" "*20,120,15,15,center=True)

            # set up the successes screen
            scoreSucc=self.display.plex("Score: "+str(self.Bee.score)+"           ", 5, 40, 20,succUi=True)
            foundSucc=self.display.plex("Found:            ", 5,65,20,succUi=True)
            displaySucc=self.display.plex("                        ", 120,107,19,center=True,succUi=True)

            # set up letter labels
            keyletterBackground=self.display.rectangle(110,85,20,26,r=3)
            keyletterBackground.hidden=True
            letterLabels=[self.display.plex(" ",30,110,30, True),
                          self.display.plex(" ",60,110,30, True),
                          self.display.plex(" ",90,110,30, True),
                          self.display.plex(" ",120,110,30, True,0x000000),
                          self.display.plex(" ",150,110,30, True),
                          self.display.plex(" ",180,110,30, True),
                          self.display.plex(" ",210,110,30, True)]

            # set the dynamic portions of the game -- letters, the grid, and the score display
            self.updateGame(letterLabels,score,gotten,scoreSucc,foundSucc)

            # unhide elements before the game starts
            keyletterBackground.hidden=False
            curr.hidden=False

            # set the initial button state
            prevButtons=self.checkButtons(self.buttons)

            # turn off the thinking rgb
            self.frontRgb.off()

            # while the game has not ended:
            end=False
            while not end:
                # set the letter selector to the current index
                #currLetter=self.Bee.letterlist[letterIndex]

                # check if there is an active alert on the screen
                if alerting:
                    # if the alert has been displayed for 5 seconds, remove the alert
                    if time.monotonic_ns()>alertStart+5000000000:
                        alert.text=""

                # check the current button state
                buttonCheck=self.checkButtons(self.buttons)

                # get the current time for comparisons on held buttons
                currTime=time.monotonic_ns()

                # if the A button is pressed and had a different value than the last cycle
                if buttonCheck[0]==True and buttonCheck[0]!=prevButtons[0]:

                    # if the button is held, shuffle the letterlist
                    passSelect=False
                    while self.buttons[0].pressed():
                        if time.monotonic_ns()>currTime+2000000000:
                            passSelect=True

                            # shuffle the bee letters
                            self.Bee.shuffle()

                            # set the letter labels
                            self.setLetterLabels(letterLabels)

                            # REPL monitoring
                            print("Shuffled letters:",self.Bee.letterlist)
                            print("Keyletter:", self.Bee.keyletter)
                            print("")
                            self.printCurrLetter(letterIndex)

                            break

                    # if the button is pressed move the letter selector to the right
                    if not passSelect and letterIndex<maxIndex:
                        # update the letter index and move the cursor
                        letterIndex+=1
                        self.moveCursorX(curr,30)

                        # REPL monitoring
                        self.printCurrLetter(letterIndex)

                # if the X button is pressed and had a different value than the last cycle
                elif buttonCheck[2]==True and buttonCheck[2]!=prevButtons[2]:

                    # if the button is held, set a new puzzle
                    passSelect=False
                    while self.buttons[2].pressed():
                        if time.monotonic_ns()>currTime+4000000000:
                            passSelect=True

                            # set an alert that show the game is being made and something is happening
                            alert.color=0x00FF00
                            alert.text="making new game..."

                            # set the new buzzword and update the screen
                            self.Bee.setBuzzword()
                            self.updateGame(letterLabels,score,gotten,scoreSucc,foundSucc)

                            # turn off the alert
                            alert.text=""

                            # REPL monitoring
                            print(self.Bee.letterlist)

                            # reset the guess string
                            guess=""
                            guessInput.text=self.printGuess(guess)

                            break

                    # if the button is pressed, move the letter selector to the left
                    if not passSelect and letterIndex>0:
                        # update the letter index and move the cursor
                        letterIndex-=1
                        self.moveCursorX(curr,-30)

                        # REPL monitoring
                        self.printCurrLetter(letterIndex)

                # if the B button is pressed and had a different value than the last cycle
                elif buttonCheck[1]==True and buttonCheck[1]!=prevButtons[1]:

                    # if the button is held, submit the current guess
                    passSelect=False
                    while self.buttons[1].pressed():
                        if time.monotonic_ns()>currTime+2000000000:
                            passSelect=True

                            # submit the guess and update the score display
                            code=self.Bee.guess(guess)
                            self.updateScoreDisplay(score,gotten,scoreSucc,foundSucc)

                            # start alerts for different guess codes
                            shortCode=self.getShortCode(code,alert)
                            alert.text=shortCode
                            alerting=True
                            alertStart=time.monotonic_ns()

                            # REPL monitoring
                            print(self.Bee.getGuessCode(code,guess))

                            # check if the bee was won with that guess
                            if self.Bee.checkForWin():
                                # set an alert that show the game is being made and something is happening
                                alert.color=0x00FF00
                                alert.text="making new game..."

                                # set the new buzzword and update the screen
                                self.Bee.setBuzzword()
                                self.updateGame(letterLabels,score,gotten,scoreSucc,foundSucc)
                                #self.buildGrid()

                                # turn off the alert
                                alert.text=""

                                # REPL monitoring
                                print(self.Bee.letterlist)

                            # reset the guess string
                            guess=""
                            guessInput.text=self.printGuess(guess)

                            break

                    # if the button is pressed, selects the current letter and adds to the guess string if there's room
                    if not passSelect and len(guess)<15:
                        guess=guess+self.Bee.letterlist[letterIndex]
                        guessInput.text=self.printGuess(guess)

                # if the Y button is pressed and had a different value than the last cycle
                elif buttonCheck[3]==True and buttonCheck[3]!=prevButtons[3]:

                    # if the button is held, show the successes screen
                    passSelect=False
                    while self.buttons[3].pressed():
                        if time.monotonic_ns()>currTime+2000000000:
                            passSelect=True

                            # switch the UI
                            self.display.switchUI("successes")

                            # REPL monitoring
                            print("Left:",self.Bee.getRemainingNum(), "\nScore:", self.Bee.score, "\nFound words:")

                            # set the previous buttons (it wont reach end of the main loop to set them for the next ui)
                            prevButtons=buttonCheck

                            # set up the success screen
                            successIndex=0
                            maxSucc=len(self.Bee.guessSuccess)-1
                            currSucc=self.testSucc(self.Bee.guessSuccess,successIndex)
                            displaySucc.text=currSucc

                            # REPL monitoring
                            print(currSucc)

                            # while the back button hasn't been pressed
                            back=False
                            while not back:

                                # set the current success to the success index and display it
                                #currSucc=self.testSucc(self.Bee.guessSuccess,successIndex)
                                #displaySucc.text=currSucc

                                # check the buttons
                                buttonCheck=self.checkButtons(self.buttons)

                                # get the current time for comparisons on held buttons
                                currTime=time.monotonic_ns()

                                # if the A button is pressed and had a different value than the last cycle
                                if buttonCheck[0]==True and buttonCheck[0]!=prevButtons[0]:

                                    # update the success index and display (?) the current success
                                    if successIndex<maxSucc:
                                        successIndex+=1
                                        currSucc=self.testSucc(self.Bee.guessSuccess,successIndex)
                                        displaySucc.text=currSucc

                                        # REPL monitoring
                                        print(currSucc)

                                # if the B button is pressed and had a different value than the last cycle
                                elif buttonCheck[1]==True and buttonCheck[1]!=prevButtons[1]:

                                    # switch to the grid ui and set the previous buttons
                                    self.display.switchUI("grid")

                                    # set up the gridui?
                                    # self.buildGrid()
                                    prevButtons=buttonCheck

                                    # display the grid until a button is pressed
                                    grid=True
                                    while grid:

                                        # if any element in the button check is true
                                        buttonCheck=self.checkButtons(self.buttons)
                                        if any(ele==True for ele in buttonCheck) and buttonCheck!=prevButtons:

                                            # switch back to the successes ui
                                            grid=False
                                            self.display.switchUI("successes")
                                            prevButtons=buttonCheck

                                            # REPL monitoring
                                            print("")

                                            break

                                        # set the previous buttons
                                        prevButtons=buttonCheck

                                # if the X button is pressed and had a different value than the last cycle
                                elif buttonCheck[2]==True and buttonCheck[2]!=prevButtons[2]:

                                    # if the button is held, enter dev mode
                                    passSelect=False
                                    while self.buttons[2].pressed():
                                        if time.monotonic_ns()>currTime+10000000000:
                                            passSelect=True

                                            # set the dev mode alert
                                            alert.color=0xFF00FF
                                            alert.text="DEV MODE"
                                            alerting=True
                                            alertStart=time.monotonic_ns()+60000000000

                                            # unmount the storage system to allow code/file upload from computer
                                            #storage.unmount("/")

                                            # go back
                                            back=True
                                            break

                                    # update the success index and display (?) the current success
                                    if not passSelect and successIndex>0:
                                        successIndex-=1
                                        currSucc=self.testSucc(self.Bee.guessSuccess,successIndex)
                                        displaySucc.text=currSucc

                                        # REPL monitoring
                                        print(currSucc)

                                # if the Y button is pressed and had a different value than the last cycle
                                elif buttonCheck[3]==True and buttonCheck[3]!=prevButtons[3]:

                                    # go back
                                    back=True

                                # set the previous buttons
                                prevButtons=buttonCheck

                            # switch back to the game ui
                            self.display.switchUI("game")
                            break


                    # if the button is pressed, delete the last letter from the guess string
                    if guess!="" and not passSelect:
                        guess=guess[:-1]
                        guessInput.text=self.printGuess(guess)

                        # REPL monitoring
                        print(guess)

                # set the next cycle's previous button state
                prevButtons=buttonCheck

        # get the Bee buzzword
        def getBuzzword(self):
            return self.Bee.buzzword

        def __init__(self, parentBee):

            # set the controller's Bee
            self.Bee=parentBee

            # set the Bee's controller
            parentBee.controller=self

            # initiate the hardware
            self.initHardware()


    def __init__(self, minimum=10,maximum=90,on_board=False,new=False):

        # set whether the game is playing with circuitpython or python
        self.circuitPython=on_board

        # set the minimum and maximum number of answers for a new game
        self.answersMin=minimum
        self.answersMax=maximum

        # if the game is played on circuitpython, create a controller object
        if self.circuitPython:
            self.controller=self.Controller(self)

        # try to read a bee from files, but if it fails make a new one
        try:
            # if the game is set to make a new bee
            if not new:
                self.readBeeFromState(BeeState(self.circuitPython))
            else:
                self.setBuzzword()
        except:
            self.setBuzzword()

    # get the cli response for guesses from guess code
    def getGuessCode(self,code,guess):
        if code==0 or code==3:
            return guess+" was not found"
        elif code==1:
            return guess+" was found!"
        elif code==2:
            return guess+" was already found"
        elif code==4:
            return guess+" is missing the keyletter"
        elif code==5:
            return "Empty guess"
        elif code==6:
            return guess+" is too short"
        elif code==7:
            return guess+" was a pangram!"
        elif code==10:
            return guess+" was the Buzzword!"
        else:
            return "Error: bad guess code"

    # create and return the game's hint grid information
    def createGrid(self):

        # create an empty dict with a $ entry for totals
        grid={"$":{}}

        # get the length of the longest word in the Bee wordlist
        maxLen=max(len(word) for word in self.wordlist)

        # for each letter in the Bee's letterlist
        for letter in self.letterlist:
            # starting from 4, because 4 is the minimum word length
            value=4

            # create an empty dict for each letter in the grid dict
            grid[letter]={}

            # for each word length up to the maximum length
            while value<=maxLen:
                # create the space for the number of words and the word totals set to 0
                grid[letter][str(value)]=0
                grid["$"][str(value)]=0
                value+=1

        # for each word in the Bee wordlist
        for word in self.wordlist:
            # grab the first letter
            firstLetter=word[0]

            # add one to the letter total and word length values in the grid dict
            grid[firstLetter][str(len(word))]+=1
            grid["$"][str(len(word))]+=1

        # for each letter in the grid
        for row in grid:
            # set the total number of words for that letter to 0
            grid[row]["$"]=0

            #check the values of each word count and add it to the letter total, skipping the total
            for value in grid[row]:
                if value=="$":
                    pass
                else:
                    grid[row]["$"]=grid[row]["$"]+grid[row][value]

        # return the grid dictionary
        return grid

    # append a guess to a guessfile
    def writeGuess(self,guess,file):
        # tries to add the current guess to the guess file, skipping the write if it is connected to a computer
        try:
            with open(file, "a") as guessFile:
                guessFile.write(guess+"\n")
        except:
            print("Device connected -- currently, the Bumblebee has a read only file-system, unplug it from your computer to write data to the device")

    # write the current bee to the system files
    def writeBeeToFiles(self):

        try:
            # write the buzzword to the buzzword file
            with open(files.getBuzzword(self.circuitPython), "w") as buzzwordFile:
                buzzwordFile.write(self.buzzword)

            # write the keyletter to the keyletter file
            with open(files.getKeyletter(self.circuitPython), "w") as keyletterFile:
                keyletterFile.write(self.keyletter)

            # write the letterlist to the letterlist file with each letter on a new line
            with open(files.getLetterlist(self.circuitPython), "w") as letterlistFile:
                buffer=""
                for letter in self.letterlist:
                    buffer=buffer+letter+"\n"
                letterlistFile.write(buffer)

            # write the wordlist dictionary to the wordlist file
            with open(files.getWordlist(self.circuitPython), "w") as wordlistFile:
                json.dump(self.wordlist, wordlistFile)

            # reset the guess success file
            with open(files.getGuessSuccess(self.circuitPython), "w") as guessSuccessFile:
                guessSuccessFile.write("")

            # reset the guess fail file
            with open(files.getGuessFail(self.circuitPython), "w") as guessFailFile:
                guessFailFile.write("")

        # skip writing if the device is connected to a computer/has a filesystem mounted
        except:
            print("Device connected -- currently, the Bumblebee has a read only file-system, unplug it from your computer to write data to the device")

    # set Bee variables from a BeeState object
    def readBeeFromState(self,state):

        self.buzzword=state.buzzword
        self.keyletter=state.keyletter
        self.letterlist=state.letterlist
        self.wordlist=state.wordlist
        self.guessSuccess=state.guessSuccess
        self.guessFail=state.guessFail
        self.score=state.score

    # return the remaining number of words in the wordlist
    def getRemainingNum(self):
        return len(self.wordlist)-len(self.guessSuccess)

    # shuffle the letters in the Bee letterlist
    def shuffle(self):
        # create a list of the non-keyletters in the letterlist
        shufflee=[self.letterlist[0],self.letterlist[1],self.letterlist[2],self.letterlist[4],self.letterlist[5],self.letterlist[6]]

        # create an empty list to shuffle them into
        shuffled=[None,None,None,None,None,None]

        # for each of the non-keyletter letters, choose one at random and move it to the shuffled list until there are none left
        shuffled[0]=random.choice(shufflee)
        shufflee.remove(shuffled[0])
        shuffled[1]=random.choice(shufflee)
        shufflee.remove(shuffled[1])
        shuffled[2]=random.choice(shufflee)
        shufflee.remove(shuffled[2])
        shuffled[3]=random.choice(shufflee)
        shufflee.remove(shuffled[3])
        shuffled[4]=random.choice(shufflee)
        shufflee.remove(shuffled[4])
        shuffled[5]=random.choice(shufflee)
        shufflee.remove(shuffled[5])

        # set all but the keyletter in the Bee letterlist
        self.letterlist[0]=shuffled[0]
        self.letterlist[1]=shuffled[1]
        self.letterlist[2]=shuffled[2]
        self.letterlist[4]=shuffled[3]
        self.letterlist[5]=shuffled[4]
        self.letterlist[6]=shuffled[5]

    # print the wordlist and buzzword -- part of the CLI
    def printAnswerKey(self):
        print("Word List:")
        print(self.wordlist)
        print("Buzzword:", self.buzzword)

    # print the Bee's hint grid -- part of the CLI
    def printGrid(self):
        print("\n")

        # create the grid information
        grid=self.createGrid()

        # for each letter in the grid
        for row in grid:
            # create a rowstring with an indent
            rowString=row+"   "

            # starting at 4, while the index is less than the longest word length in the grid information
            index=4
            maxLen=len(grid[row])+2
            while index<=maxLen:

                # if the current letter is for the totals, grab the totals
                if(row=="$"):
                    rowString=rowString+str(grid[row][str(index)])+"("+str(index)+")"+"  "

                # otherwise add the number of words starting with that letter to the grid
                else:
                    val=str(grid[row][str(index)])

                    # if the  value is 0, set it to -
                    if val=="0":
                        val="-"

                    rowString=rowString+val+"      "
                index+=1

            # handle letter totals
            if(row=="$"):
                rowString=rowString+str(grid[row]["$"])+"($)"+"   "
            else:
                rowString=rowString+str(grid[row]["$"])+"      "

            # print the row strings
            if(row=="$"):
                totalString=rowString
            else:
                print(rowString)
        print("\n"+totalString+"\n")

    # print the current Bee CLI interface -- part of the CLI
    def printBee(self):
        # print the traditional NYTSB hexagon
        print('''
        %s
    %s      %s
        %s
    %s      %s
        %s
''' % (self.letterlist[0],self.letterlist[1],self.letterlist[2],self.letterlist[3],self.letterlist[4],self.letterlist[5],self.letterlist[6]))

        # print the current correct guesses and score
        print("Found: (%s left)" % (self.getRemainingNum()))
        print("Score:",self.score)
        print(self.guessSuccess)

    # the starting function for the Bee CLI -- part of the CLI
    def guessCLI(self):

        # set initial parameters
        win=False
        guessCode=None
        gridOn=None
        cheatOn=None

        # while the game has not been won
        while not win:
            print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")

            # if the grid is on, print the grid
            if gridOn:
                self.printGrid()
            # if cheats are on, print the wordlist
            if cheatOn:
                self.printAnswerKey()

            # if there is a guess code, print and reset the guess code
            if guessCode:
                print("\n"+guessCode)
                guessCode=None

            # print the hexagon
            self.printBee()

            # ask to input a guess
            guessString=input(">> ")

            # if the guess string asks for cheats, turn on cheats
            if guessString=="-cheat":
                cheatOn=not cheatOn

            # if the guess string asks for a grid, turn on the grid
            elif guessString=="-grid":
                gridOn=not gridOn

            # if the guess string asks for the letters to be shuffled, shuffle the letters
            elif guessString=="-shuffle":
                self.shuffle()

            # if the guess string asks for a new game, set a new buzzword
            elif guessString=="-new":
                self.setBuzzword()

            # otherwise, submit the guess and get the guess code
            else:
                code=self.guess(guessString)
                guessCode=self.getGuessCode(code,guessString)

            # check if the game has been won
            win=self.checkForWin()

        # print the Bee one last time with the finished game
        self.printBee()

    # check if all words have been guessed
    def checkForWin(self):

        # copy the wordlist to check the successful guesses against
        checkedAgainst=list(self.wordlist.keys())

        # for each successful guess
        for guess in self.guessSuccess:

            # if the current guess is in the checked against list, remove it from the checked against list
            if guess in checkedAgainst:
                checkedAgainst.remove(guess)

        # if all the words have been removed from the checked against list return true, otherwise return false
        if len(checkedAgainst)==0:
            return True
        else:
            return False

    # check if a word contains all the letters in a letterlist
    def checkPanagram(self,word,letters):

        # for each letter in the letterlist
        panagram=True
        for letter in letters:

            # if the letter is not found in the word, return false
            if letter not in word:
                panagram=False
                break

        # otherwise return true
        return panagram

    # executed if a guess is in the wordlist
    def success(self,guessString):

        # if the guess has already been guessed, set the guesscode to already found
        if guessString in self.guessSuccess:
            guessCode=Codes.ALREADY_FOUND

        # otherwise check for the kind of success
        else:
            # set the guesscode to success
            guessCode=Codes.SUCCESS

            # add the guess to the guess successes
            self.guessSuccess.append(guessString)
            self.writeGuess(guessString,files.getGuessSuccess(self.circuitPython))

            # if the guess is a panagram, set the guesscode to panagram
            panagram=self.checkPanagram(guessString,self.letterlist)
            if panagram:
                guessCode=Codes.PANAGRAM

            # if the guess string is the Bee's buzzword, set the guesscode to buzzword
            if guessString==self.buzzword:
                guessCode=Codes.BUZZWORD

            # add the guess's associated score from the wordlist to the bee's score
            self.score=self.score+self.wordlist[guessString]

        # return the guesscode
        return guessCode

    # executed if a guess is not in the wordlist
    def fail(self,guessString):

        # if the guess is empty, set the
        if guessString.strip()=="":
            guessCode=Codes.EMPTY

        # otherwise, if there are letters in the guess
        else:
            # add the unsuccessful guess to the guess fails
            self.guessFail.append(guessString)
            self.writeGuess(guessString,files.getGuessFail(self.circuitPython))

            # set the guesscode to fail
            guessCode = Codes.FAIL

            # if the keyletter is missing from the guess string, set the guesscode to missing keyletter
            if self.keyletter not in guessString:
                guessCode=Codes.MISSING_KEY

            # if the guess is shorter than 4 letters, set the guesscode to too short
            if len(guessString)<4:
                guessCode=Codes.TOO_SHORT

        # return the guesscode
        return guessCode

    # submit a guess
    def guess(self,guessString):

        # if the guess is in the wordlist, return the success
        if guessString in self.wordlist:
            return self.success(guessString)

        # if the guess is not in the wordlist, return the fail
        else:
            return self.fail(guessString)

    # get a candidate for the buzzword from a random index
    def getBuzzCandidate(self, randIndex):

        # open the buzzword candidate file
        with open(files.getBuzzCandidatesCsv(self.circuitPython), 'r') as buzzCandidates:

            # for each line in the candidate file
            indexCount=0
            for line in buzzCandidates:

                # if it reaches the random index, return the line, stripped
                if indexCount==randIndex:
                    return line.strip()
                indexCount+=1

    # generate a wordlist from a target word and a keyletter
    def getWordlist(self, targetWord, keyletter):

        # create an empty wordlist dictionary
        wordlist={}

        # open the dictionary csv
        with open(files.getDictionaryCsv(self.circuitPython),"r") as dictionaryCsv:

            # for each word in the dictionary
            for word in dictionaryCsv:

                # strip the word
                word=word.strip()

                # if the keyletter is in the word
                if keyletter in word:

                    # for each letter in the word
                    for letter in word:

                        # if the letter is also in the target word, it passes, if the letter is not found it fails
                        fails=False
                        if letter in targetWord:
                            pass
                        else:
                            fails=True
                            break

                    # if the word doesn't fail
                    if not fails:

                        # if the length of the word is exactly 4 the word's score is 1
                        if len(word)==4:
                            score=1

                        # otherwise the score is the length of the word
                        else:
                            score=len(word)

                            # if the word is a panagram, add an extra 7 to the score
                            if self.checkPanagram(word,targetWord):
                                score=score+7

                            # the the word is the target word, add an extra 3 to the score
                            if word==targetWord:
                                score=score+3

                        # add the word to the wordlist dictionary, with the word as the key and the score as the value
                        wordlist[word]=score

            # return the wordlist
            return wordlist

    # get a letterlist for a target word
    def getLetterlist(self, targetWord):

        # create an empty set for the letterlist to jumble them up
        letterlist=set()

        # for each letter in the target word, add the word to the letterlist set
        for letter in targetWord:
            letterlist.add(letter)

        # return the letterlist as a list
        return list(letterlist)

    # set the Bee dictionaries -- DEPRICATED: NOT ENOUGH RAM ON LIPO PICO
    def setDictionaries(self):

        # open the dictionary json and set its contents to the Bee dictionary variable
        with open(files.getDictionary(self.circuitPython)) as dictionaryFile:
            self.dictionary=json.load(dictionaryFile)

        # open the buzzword candidate json and set its contents to the Bee buzzcandidates variable
        with open(files.getBuzzCandidates(self.circuitPython)) as candidates:
            self.buzzCandidates=json.load(candidates)
            self.buzzCandidates_list=list(self.buzzCandidates.keys())

    # set the Bee's buzzword
    def setBuzzword(self):

        # try to run the garbage collector and print free memory -- for use with CircuitPython
        try:
            gc.collect()
            print("Memory 1:", gc.mem_free())
        except:
            pass

        # get a random index for the buzzword from the length of the dictionary
        randIndex=random.randint(0,self.dictLen)

        # try to turn on the front thinking rgb -- for use with CircuitPython
        try:
            self.controller.frontRgb.setColor(self.controller.frontRgb.Colors.RED)
            self.controller.frontRgb.on()
        except Exception as e: print(e)

        # select a buzzword candidate and make lists for it
        candidate=self.getBuzzCandidate(randIndex)
        lettersCandidate=self.getLetterlist(candidate)
        keyletterCandidate=lettersCandidate[3]
        listCandidate=self.getWordlist(lettersCandidate,keyletterCandidate)
        print("Candidate:", lettersCandidate, keyletterCandidate)

        # if the number of words in the wordlist candidate is between the minimum and the maximum
        if (self.answersMin<len(listCandidate)<self.answersMax):

            # set the Bee game variables to the candidate
            self.buzzword=candidate
            self.wordlist=listCandidate
            self.letterlist=lettersCandidate
            self.keyletter=keyletterCandidate

            # reset the guesses and game score
            self.guessSuccess=[]
            self.guessFail=[]
            self.score=0

            # write the Bee state to files
            self.writeBeeToFiles()

            # try to run the garbage collector and print free memory -- for use with CircuitPython
            try:
                gc.collect()
                print("Memory 2:", gc.mem_free())
            except:
                pass

            # try to turn off the front thinking rgb -- for use with CircuitPython
            try:
                self.controller.frontRgb.off()
            except Exception as e: print(e)

        # otherwise, try to set a new buzzword
        else:
            self.setBuzzword()


def main():
    testBee = Bee()
    testBee.guessCLI()

if __name__ == "__main__":
    main()
