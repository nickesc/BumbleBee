import json
import random
import src.files as files
from src.guessCodes import Codes


class BeeState:
    def __init__(self, bee):
        self.buzzword=files.getBuzzword(bee.circuitpython)
        self.keyletter=files.getKeyletter(bee.circuitpython)
        self.letterlist=files.getLetterlist(bee.circuitpython)
        self.wordlist=files.getWordlist(bee.circuitpython)

        self.guessSuccess=files.getGuessSuccess(bee.circuitpython)
        self.guessFail=files.getGuessFail(bee.circuitpython)
        return

class Bee:


    circuitPython=False

    dictionary={}
    buzzCandidates={}

    buzzword=""
    keyletter=""
    letterlist=[]

    wordlist={}
    guessSuccess=[]
    guessFail=[]

    def __init__(self, minimum=10,maximum=90,on_board=False):

        self.circuitPython=on_board

        self.answersMin=minimum
        self.answersMax=maximum

        self.setDictionaries()
        self.setBuzzword()

        self.writeBeeToFiles()

        #self.guessCLI()

    def writeGuess(self,guess,file):
        with open(file, "a") as guessFile:
            guessFile.write(guess+" ")

    def writeBeeToFiles(self):

        try:
            with open(files.getBuzzword(self.circuitPython), "w") as buzzwordFile:
                buzzwordFile.write(self.buzzword)

            with open(files.getKeyletter(self.circuitPython), "w") as keyletterFile:
                keyletterFile.write(self.keyletter)

            with open(files.getLetterlist(self.circuitPython), "w") as letterlistFile:
                buffer=""
                for letter in self.letterlist:
                    buffer=buffer+letter+" "
                letterlistFile.write(buffer)

            with open(files.getWordlist(self.circuitPython), "w") as wordlistFile:
                json.dump(self.wordlist, wordlistFile)

            with open(files.getGuessSuccess(self.circuitPython), "w") as guessSuccessFile:
                guessSuccessFile.write("")

            with open(files.getGuessFail(self.circuitPython), "w") as guessFailFile:
                guessFailFile.write("")

        except:
            print("Device connected -- currently, the Bumblebee has a read only file-system, unplug it from your computer to write data to the device")

    def readBeeFromFile(self):
        return

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
                elif code==5:
                    print("Empty")
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
            guessCode=Codes.ALREADYFOUND
        else:
            guessCode=Codes.SUCCESS
            self.guessSuccess.append(guessString)
            self.writeGuess(guessString,files.getGuessSuccess(self.circuitPython))

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
        return guessCode

    def guess(self,guessString):
        if guessString in self.wordlist:
            return self.success(guessString)
        else:
            return self.fail(guessString)

    def getBuzzCandidate(self):
        # need a random int to count to to find a candidate
        return random.choice(self.buzzCandidates_list)

    def getWordlist(self, targetWord, keyletter):
        wordlist={}

        for word in self.dictionary:
            if keyletter in word:
                for letter in word:
                    fails=False
                    if letter in targetWord:
                        pass
                    else:
                        fails=True
                        break
                if not fails:
                    wordlist[word]=self.dictionary[word]

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
        candidate=self.getBuzzCandidate()
        lettersCandidate=self.getLetterlist(candidate)
        keyletterCandidate=lettersCandidate[3]
        listCandidate=self.getWordlist(lettersCandidate,keyletterCandidate)

        if (self.answersMin<len(listCandidate)<self.answersMax):
            self.buzzword=candidate
            self.wordlist=listCandidate
            self.letterlist=lettersCandidate
            self.keyletter=keyletterCandidate
        else:
            self.setBuzzword()


def main():
    testBee = Bee(2,16)

if __name__ == "__main__":
    main()
