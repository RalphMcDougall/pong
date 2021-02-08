import pygame
import game

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)


SCORE_FONT_SIZE = 32
SCORE_FONT = None
PLAYER_FONT_SIZE = 16
PLAYER_FONT = None

FPS = 60

class DisplayScreen:

    screen = None
    running = False
    fpsClock = None

    def __init__(self, width, height):
        self.screen = pygame.display.set_mode((width,height)) #Start the screen
        pygame.display.set_caption("Pong")
        self.running = True
        self.fpsClock = pygame.time.Clock()
    
    def handleScreenUpdate(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
    
    def isRunning(self):
        return self.running

    def getScreen(self):
        return self.screen

    def clearScreen(self):
        self.screen.fill(BLACK)

    def refreshScreen(self):
        pygame.display.update()

    def controlFPS(self):
        self.fpsClock.tick(FPS)

class SelectionScreen:

    def __init__(self, options):
        self.options = [options, options]
        self.selected = [0, 0]
        self.focus = 0 # 0 = left, 1 = right
        self.done = False
    
    def isDone(self):
        return self.done

    def updateState(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.done = True
                elif event.key == pygame.K_LEFT:
                    self.focus = 0
                elif event.key == pygame.K_RIGHT:
                    self.focus = 1
                elif event.key == pygame.K_DOWN:
                    self.selected[self.focus] = self.selected[self.focus] + 1
                    if self.selected[self.focus] == len(self.options[self.focus]):
                        self.selected[self.focus] = 0
                elif event.key == pygame.K_UP:
                    self.selected[self.focus] = self.selected[self.focus] - 1
                    if self.selected[self.focus] == -1:
                        self.selected[self.focus] = len(self.options[self.focus]) - 1

    def drawSelection(self, displayScreen):
        rectWidth = game.PongGame.BOARD_WIDTH / 2 - 100
        rectHeight = 32
        hBuffer = 48
        vBuffer = 16
        for cInd, col in enumerate(self.options):
            playerTitle = SCORE_FONT.render("PLAYER " + str(cInd + 1), False, WHITE)
            displayScreen.screen.blit(playerTitle, (cInd * game.PongGame.BOARD_WIDTH / 2 + game.PongGame.BOARD_WIDTH / 4 - playerTitle.get_rect().width / 2, 
                                        playerTitle.get_rect().height / 2, rectWidth, rectHeight))
            for rInd, row in enumerate(col):
                pygame.draw.rect(displayScreen.screen, GREEN if self.selected[cInd] == rInd else WHITE, 
                                    (game.PongGame.BOARD_WIDTH / 2 * cInd + hBuffer, vBuffer + (rInd + 1) * (vBuffer + rectHeight), 
                                    rectWidth, rectHeight))
                pygame.draw.rect(displayScreen.screen, WHITE, 
                                    (game.PongGame.BOARD_WIDTH / 2 * cInd + hBuffer, vBuffer + (rInd + 1) * (vBuffer + rectHeight), 
                                    rectWidth, rectHeight), 5)
                
                op = PLAYER_FONT.render(row.name, True, BLACK)
                displayScreen.screen.blit(op, (game.PongGame.BOARD_WIDTH / 2 * cInd  + game.PongGame.BOARD_WIDTH / 4 - op.get_rect().width / 2, 
                                            vBuffer + (rInd + 1) * (vBuffer + rectHeight) + rectHeight / 2 - op.get_rect().height / 2, 
                                            rectWidth, rectHeight))

        pygame.draw.line(displayScreen.screen, WHITE, (game.PongGame.BOARD_WIDTH / 2, 0), 
                            (game.PongGame.BOARD_WIDTH / 2, game.PongGame.BOARD_HEIGHT), 1)
    
    def getSelection(self):
        return [ self.options[0][self.selected[0]], self.options[1][self.selected[1]] ]

screen = None

def setupDisplay():
    global SCORE_FONT, SCORE_FONT_SIZE, PLAYER_FONT, PLAYER_FONT_SIZE
    pygame.init()
    pygame.font.init()
    SCORE_FONT = pygame.font.Font("PressStart2P.ttf", SCORE_FONT_SIZE)
    PLAYER_FONT = pygame.font.Font("Roboto-Bold.ttf", PLAYER_FONT_SIZE)


def closeDisplay():
    pygame.quit() #Close the window