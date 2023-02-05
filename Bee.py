from argparse import ArgumentParser, RawDescriptionHelpFormatter

program='python3 Bee.py'

epilogue='''
CLI commands:
  -new      generate a new Bee
  -grid     toggle the hint grid
  -cheat    toggle the wordlist
  -shuffle  shuffle the order of the letterlist

Running the CLI will start a Bee. By default, the game will use the data from the last saved Bee state. Enter words into the input to submit them as guesses or enter commands to execute them.

For more information visit:
  https://github.com/nickesc/BumbleBee#cli-gameplay
 '''

argParser = ArgumentParser(
    prog = program,
    formatter_class=RawDescriptionHelpFormatter,
    description = 'A CLI word game generator based on the New York Times Spelling Bee',
    epilog = epilogue
    )

argParser.add_argument('-n', '--new',
                action='store_true', help="start a new game; default is to use the Bee state stored in ./BumbleBee/bee_state")

newGame = argParser.parse_args().new

from src.bumbleBee import Bee

def main():
    cliBee = Bee(new=newGame)
    cliBee.guessCLI()

if __name__ == "__main__":
    main()
