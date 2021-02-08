import game
import display

def run():
    display.setupDisplay()

    displayScreen = display.DisplayScreen(game.PongGame.BOARD_WIDTH, game.PongGame.BOARD_HEIGHT)
    currGame = game.PongGame(game.PongPlayer(), game.PongPlayer())

    selectionScreen = display.SelectionScreen([game.UserControlledPongPlayer(), game.RLPongPlayer(), 
                                                game.MLPongPlayer(), game.FirstMLPongPlayer(), game.PerfectPongPlayer()])
    
    currentDisplayMode = 0 # 0 = Selection Mode, 1 = Game Mode
    
    while displayScreen.isRunning():
        displayScreen.clearScreen()
        if currentDisplayMode == 0:
            selectionScreen.updateState()
            selectionScreen.drawSelection(displayScreen)
            if selectionScreen.isDone():
                currGame = game.PongGame(selectionScreen.getSelection()[0], selectionScreen.getSelection()[1])
                currentDisplayMode = 1
        elif currentDisplayMode == 1:
            currGame.updateGameState()
            currGame.drawToScreen(displayScreen.getScreen())
        
        displayScreen.handleScreenUpdate()
        displayScreen.refreshScreen()
        displayScreen.controlFPS()

    display.closeDisplay()   

if __name__ == "__main__":
    run()
