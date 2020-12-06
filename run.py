import game
import display

def setup():
    display.setupDisplay()

    displayScreen = display.DisplayScreen(game.PongGame.BOARD_WIDTH, game.PongGame.BOARD_HEIGHT)

    p1 = game.PongPlayer()
    p2 = game.PongPlayer()
    currGame = game.PongGame(p1, p2)

    while displayScreen.isRunning():
        displayScreen.clearScreen()
        currGame.updateGameState()
        displayScreen.handleScreenUpdate()
        currGame.drawToScreen(displayScreen.getScreen())

        displayScreen.refreshScreen()
        displayScreen.controlFPS()

    display.closeDisplay()   

if __name__ == "__main__":
    setup()