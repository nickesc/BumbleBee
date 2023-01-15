from src.spellingBee import Bee

def main():

    bumbleBee = Bee(new=False, on_board=True)
    bumbleBee.controller.startGame()

if __name__ == "__main__":
    main()
