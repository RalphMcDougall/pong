import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

SCORE_FONT_SIZE = 30
SCORE_FONT = None

FPS = 30

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

screen = None

def setupDisplay():
    global SCORE_FONT, SCORE_FONT_SIZE
    pygame.init()
    pygame.font.init()
    SCORE_FONT = pygame.font.SysFont("Arial", SCORE_FONT_SIZE)


def closeDisplay():
    pygame.quit() #Close the window