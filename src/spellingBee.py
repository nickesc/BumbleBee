import json
import random
import src.files as files

from src.guessCodes import Codes

try:
    import board
except:
    from dummy.board import board

from src.lights import RGB,LED
# try:
#     from src.lights import LED
# except:
#     from dummy.lights import LED

class BeeState:

    buzzword=""
    keyletter=""
    letterlist=[]
    wordlist={}

    guessSuccess=[]
    guessFail=[]

    def __init__(self, circuitpython):

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

class Bee:

    busyLed = LED(board.LED)
    frontRgb = RGB(board.GP6,board.GP7,board.GP8)

    dictLen=8823

    circuitPython=False

    dictionary={}
    buzzCandidates={}

    buzzword=""
    keyletter=""
    letterlist=[]

    wordlist={}
    guessSuccess=[]
    guessFail=[]

    def __init__(self, minimum=10,maximum=90,on_board=False,new=False):



        self.circuitPython=on_board

        self.answersMin=minimum
        self.answersMax=maximum

        #self.setDictionaries()


        self.busyLed.on()
        try:
            if not new:
                self.readBeeFromState(BeeState(self.circuitPython))
            else:
                self.setBuzzword()
        except:
            self.setBuzzword()
        self.busyLed.off()

        self.writeBeeToFiles()

        #self.guessCLI()


    def createGrid(self):

        grid={"$":{}}

        maxLen=max(len(word) for word in self.wordlist)

        for letter in self.letterlist:
            value=4
            grid[letter]={}
            while value<=maxLen:
                grid[letter][str(value)]=0
                grid["$"][str(value)]=0
                value+=1

        for word in self.wordlist:
            firstLetter=word[0]
            grid[firstLetter][str(len(word))]+=1
            grid["$"][str(len(word))]+=1

        for row in grid:
            grid[row]["$"]=0
            #print(row,grid[row])
            for value in grid[row]:
                if value=="$":
                    pass
                else:
                    grid[row]["$"]=grid[row]["$"]+grid[row][value]

        return grid

    def writeGuess(self,guess,file):
        try:
            with open(file, "a") as guessFile:
                guessFile.write(guess+"\n")
        except:
            print("Device connected -- currently, the Bumblebee has a read only file-system, unplug it from your computer to write data to the device")

    def writeBeeToFiles(self):

        try:
            with open(files.getBuzzword(self.circuitPython), "w") as buzzwordFile:
                buzzwordFile.write(self.buzzword)

            with open(files.getKeyletter(self.circuitPython), "w") as keyletterFile:
                keyletterFile.write(self.keyletter)

            with open(files.getLetterlist(self.circuitPython), "w") as letterlistFile:
                buffer=""
                for letter in self.letterlist:
                    buffer=buffer+letter+"\n"
                letterlistFile.write(buffer)

            with open(files.getWordlist(self.circuitPython), "w") as wordlistFile:
                json.dump(self.wordlist, wordlistFile)

            with open(files.getGuessSuccess(self.circuitPython), "w") as guessSuccessFile:
                guessSuccessFile.write("")

            with open(files.getGuessFail(self.circuitPython), "w") as guessFailFile:
                guessFailFile.write("")

        except:
            print("Device connected -- currently, the Bumblebee has a read only file-system, unplug it from your computer to write data to the device")

    def readBeeFromState(self,state):

        self.buzzword=state.buzzword
        self.keyletter=state.keyletter
        self.letterlist=state.letterlist
        self.wordlist=state.wordlist
        self.guessSuccess=state.guessSuccess
        self.guessFail=state.guessFail

    def getRemainingNum(self):
        return len(self.wordlist)-len(self.guessSuccess)

    def printAnswerKey(self):
        print("Word List:")
        print(self.wordlist)
        print("\nBuzzword:", self.buzzword)

    def printBee(self):
        print('''
        %s
    %s      %s
        %s
    %s      %s
        %s
''' % (self.letterlist[0],self.letterlist[1],self.letterlist[2],self.letterlist[3],self.letterlist[4],self.letterlist[5],self.letterlist[6]))
        print("Found: (%s left)" % (self.getRemainingNum()))
        print(self.guessSuccess)

    def guessCLI(self):
        win=False
        while not win:
            self.printBee()
            guessString=input(">> ")
            if guessString=="-help":
                self.printAnswerKey()
            elif guessString=="-grid":
                print("\n")
                grid=self.createGrid()
                for row in grid:
                    rowString=row+"   "
                    index=4
                    maxLen=len(grid[row])+2
                    while index<=maxLen:
                        if(row=="$"):
                            rowString=rowString+str(grid[row][str(index)])+"("+str(index)+")"+"  "
                        else:
                            rowString=rowString+str(grid[row][str(index)])+"      "
                        index+=1
                    if(row=="$"):
                        rowString=rowString+str(grid[row]["$"])+"($)"+"   "
                    else:
                        rowString=rowString+str(grid[row]["$"])+"      "
                    if(row=="$"):
                        totalString=rowString
                    else:
                        print(rowString)
                print("\n"+totalString+"\n")

                #print("$",grid["$"])
            else:
                code=self.guess(guessString)

                if code==0:
                    print("Fail")
                elif code==1:
                    print("Success")
                elif code==2:
                    print("Already found")
                elif code==3:
                    print("Not found")
                elif code==4:
                    print("Missing key")
                elif code==5:
                    print("Empty")
                elif code==6:
                    print("Too short")
                elif code==7:
                    print("Pangram")
                elif code==10:
                    print("Buzzword")

            win=self.checkForWin()
        self.printBee()

    def checkForWin(self):
        checkedAgainst=list(self.wordlist.keys())
        for guess in self.guessSuccess:
            if guess in checkedAgainst:
                checkedAgainst.remove(guess)
        if len(checkedAgainst)==0:
            return True
        else:
            return False

    def success(self,guessString):
        if guessString in self.guessSuccess:
            guessCode=Codes.ALREADY_FOUND
        else:
            guessCode=Codes.SUCCESS
            self.guessSuccess.append(guessString)
            self.writeGuess(guessString,files.getGuessSuccess(self.circuitPython))

            panagram=True
            for letter in self.letterlist:
                if letter not in guessString:
                    panagram=False
                    break

            if panagram:
                guessCode=Codes.PANAGRAM
            if guessString==self.buzzword:
                guessCode=Codes.BUZZWORD

        return guessCode

    def fail(self,guessString):
        if guessString.strip()=="":
            guessCode=Codes.EMPTY
        else:
            self.guessFail.append(guessString)
            self.writeGuess(guessString,files.getGuessFail(self.circuitPython))
            guessCode = Codes.FAIL
            if self.keyletter not in guessString:
                guessCode=Codes.MISSING_KEY
            if len(guessString)<4:
                guessCode=Codes.TOO_SHORT
        return guessCode

    def guess(self,guessString):
        if guessString in self.wordlist:
            return self.success(guessString)
        else:
            return self.fail(guessString)

    def getBuzzCandidate(self, randIndex):

        with open(files.getBuzzCandidatesCsv(self.circuitPython), 'r') as buzzCandidates:
            indexCount=0

            for line in buzzCandidates:
                if indexCount==randIndex:
                    return line.strip()
                indexCount+=1

        #return random.choice(self.buzzCandidates_list)

        # need a random int to count to to find a candidate


    def getWordlist(self, targetWord, keyletter):
        wordlist={}

        with open(files.getDictionaryCsv(self.circuitPython),"r") as dictionaryCsv:
            for word in dictionaryCsv:
                word=word.strip()
                if keyletter in word:
                    for letter in word:
                        fails=False
                        if letter in targetWord:
                            pass
                        else:
                            fails=True
                            break
                    if not fails:
                        wordlist[word]=1
            return wordlist

    def getLetterlist(self, targetWord):
        letterlist=set()
        for letter in targetWord:
            letterlist.add(letter)
        return list(letterlist)

    def setDictionaries(self):

        with open(files.getDictionary(self.circuitPython)) as dictionaryFile:
            self.dictionary=json.load(dictionaryFile)

        with open(files.getBuzzCandidates(self.circuitPython)) as candidates:
            self.buzzCandidates=json.load(candidates)
            self.buzzCandidates_list=list(self.buzzCandidates.keys())

    def setBuzzword(self):
        randIndex=random.randint(0,self.dictLen)

        candidate=self.getBuzzCandidate(randIndex)
        lettersCandidate=self.getLetterlist(candidate)
        keyletterCandidate=lettersCandidate[3]
        print("Candidate:", lettersCandidate, keyletterCandidate)
        listCandidate=self.getWordlist(lettersCandidate,keyletterCandidate)

        if (self.answersMin<len(listCandidate)<self.answersMax):
            self.buzzword=candidate
            self.wordlist=listCandidate
            self.letterlist=lettersCandidate
            self.keyletter=keyletterCandidate
        else:
            self.setBuzzword()


def main():
    testBee = Bee()
    testBee.guessCLI()

if __name__ == "__main__":
    main()
