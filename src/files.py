# get the file prefix
def getPrefix(circuitpython):

    # if the game is running on circuitpython, return /, otherwise return an empty string
    if circuitpython==True:
        return "/"
    else:
        return ""

# get the source dictionary file name
def getTwl06(circuitpython=False):
    return(getPrefix(circuitpython)+'assets/english35.txt')

# get the game dictionary file name
def getDictionary(circuitpython=False):
    return(getPrefix(circuitpython)+'dictionary/dictionary.json')

# get the game dictionary csv name
def getDictionaryCsv(circuitpython=False):
    return(getPrefix(circuitpython)+'dictionary/dictionary.csv')

# get the buzzword candidates file name
def getBuzzCandidates(circuitpython=False):
    return(getPrefix(circuitpython)+'dictionary/buzzCandidates.json')

# get the buzzword candidates csv  name
def getBuzzCandidatesCsv(circuitpython=False):
    return(getPrefix(circuitpython)+'dictionary/buzzCandidates.csv')

# get the buzzword game file
def getBuzzword(circuitpython=False):
    return(getPrefix(circuitpython)+"bee_state/buzzword")

# get the keyletter game file
def getKeyletter(circuitpython=False):
    return(getPrefix(circuitpython)+"bee_state/keyletter")

# get the letterlist game file
def getLetterlist(circuitpython=False):
    return(getPrefix(circuitpython)+"bee_state/letterlist")

# get the wordlist game file
def getWordlist(circuitpython=False):
    return(getPrefix(circuitpython)+"bee_state/wordlist")

# get the guess success game file
def getGuessSuccess(circuitpython=False):
    return(getPrefix(circuitpython)+"bee_state/guessSuccess")

# get the guess fail game file
def getGuessFail(circuitpython=False):
    return(getPrefix(circuitpython)+"bee_state/guessFail")

# return a dictionary with all file names
def getFiles(circuitpython=False):
    return {
        "twl06":getTwl06(circuitpython),
        "dictionary":getDictionary(circuitpython),
        "dictionaryCsv":getDictionaryCsv(circuitpython),
        "buzzCandidates":getBuzzCandidates(circuitpython),
        "buzzCandidatesCsv":getBuzzCandidatesCsv(circuitpython),
        "buzzword":getBuzzword(circuitpython),
        "keyletter":getKeyletter(circuitpython),
        "letterlist":getLetterlist(circuitpython),
        "wordlist":getWordlist(circuitpython),
        "guessSuccess":getGuessSuccess(circuitpython),
        "guessFail":getGuessFail(circuitpython)
    }

# print file names
def printFiles(circuitpython=False, printFiles=[]):

    # get file dictionary
    files=getFiles(circuitpython=circuitpython)

    # print the circuitpython status
    print("circuitpython: ",circuitpython)

    # if there are no specified files to print, print all file names in the file dictionary
    if printFiles == []:
        for file in files:
            print(files[file])

    # otherwise print the desired file names
    else:
        for file in printFiles:
            print(files[file])
