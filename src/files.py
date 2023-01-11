def getPrefix(circuitpython):
    if circuitpython==True:
        return "/"
    else:
        return ""

def getTwl06(circuitpython=False):
    return(getPrefix(circuitpython)+'assets/english35.txt')

def getDictionary(circuitpython=False):
    return(getPrefix(circuitpython)+'dictionary/dictionary.json')

def getDictionaryCsv(circuitpython=False):
    return(getPrefix(circuitpython)+'dictionary/dictionary.csv')

def getBuzzCandidates(circuitpython=False):
    return(getPrefix(circuitpython)+'dictionary/buzzCandidates.json')

def getBuzzCandidatesCsv(circuitpython=False):
    return(getPrefix(circuitpython)+'dictionary/buzzCandidates.csv')

def getBuzzword(circuitpython=False):
    return(getPrefix(circuitpython)+"bee_state/buzzword")

def getKeyletter(circuitpython=False):
    return(getPrefix(circuitpython)+"bee_state/keyletter")

def getLetterlist(circuitpython=False):
    return(getPrefix(circuitpython)+"bee_state/letterlist")

def getWordlist(circuitpython=False):
    return(getPrefix(circuitpython)+"bee_state/wordlist")

def getGuessSuccess(circuitpython=False):
    return(getPrefix(circuitpython)+"bee_state/guessSuccess")

def getGuessFail(circuitpython=False):
    return(getPrefix(circuitpython)+"bee_state/guessFail")


""" x=getTwl06(True)
y=getDictionary(True)
z=getBuzzCandidates(True)

a=getTwl06(False)
b=getDictionary(False)
c=getBuzzCandidates(False) """
