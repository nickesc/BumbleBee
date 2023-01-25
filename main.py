#import sys, getopt
import argparse
from src.bumbleBee import Bee

def main():

    epilogue='''
'''

    argParser = argparse.ArgumentParser(
        prog = 'BumbleBee',
        description = 'A CLI word game generator based on the New York Times Spelling Bee',
        epilog = epilogue
        )

    argParser.add_argument('-n', '--new',
                    action='store_true', help="start a new game; default is to use the game state stored in ./BumbleBee/bee_state")

    newGame = argParser.parse_args().new

    print("New game: ",newGame)


    cliBee = Bee(new=newGame)
    cliBee.guessCLI()

if __name__ == "__main__":
    main()
