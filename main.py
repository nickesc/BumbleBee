from src.spellingBee import Bee, BeeState

def main():
    testBee = Bee(new=False)

    testBee.guessCLI()
    #print(testBee.getWordlist("flapjack","f"))

if __name__ == "__main__":
    main()
