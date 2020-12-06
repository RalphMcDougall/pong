import game
import display

def run():
    display.setupDisplay()

    displayScreen = display.DisplayScreen(game.PongGame.BOARD_WIDTH, game.PongGame.BOARD_HEIGHT)

    p1 = game.UserControlledPongPlayer()
    p2 = game.BasicPongPlayer()
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
    run()
