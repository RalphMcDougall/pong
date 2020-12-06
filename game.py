import random

class PongGame:
    BOARD_WIDTH = 800
    BOARD_HEIGHT = 600
    PADDLE_WIDTH = 10
    PADDLE_HEIGHT = 50

    PADDLE_HOR_BUFFER = 5

    PADDLE_VELOCITY = 5

    BALL_SIZE = 4
    BALL_VELOCITY_SCALAR = 1

    MOVE_UP = 0
    MOVE_DOWN = 1
    MOVE_STAY = 2

    players = []
    paddlePositionsX = []
    paddlePositionsY = []

    ballPosition = []
    ballVelocity = []

    score = []

    def __init__(self, player1, player2):
        self.players = [player1, player2]
        self.paddlePositionsX = [
            0 + PongGame.PADDLE_WIDTH / 2 + PongGame.PADDLE_HOR_BUFFER,
            PongGame.BOARD_WIDTH - PongGame.PADDLE_WIDTH / 2 - PongGame.PADDLE_HOR_BUFFER
        ]
        self.paddlePositionsY = [
            PongGame.BOARD_HEIGHT / 2, 
            PongGame.BOARD_HEIGHT / 2
        ]
        self.resetBallPosition()
        self.score = [0, 0]

    def updateGameState(self):
        ballPosition[0] += ballVelocity[0]
        ballPosition[1] += ballVelocity[1]

        # Ball Physics
        if self.ballPosition[0] < PongGame.PADDLE_HOR_BUFFER:
            self.score[1] += 1
            self.resetBallPosition()
        elif self.ballPosition[0] > PongGame.BOARD_WIDTH - PongGame.PADDLE_HOR_BUFFER:
            self.score[0] += 1
            self.resetBallPosition()
        
        if self.ballPosition[1] - PongGame.BALL_SIZE / 2 < 0:
            self.ballPosition[1] = PongGame.BALL_SIZE / 2
            self.ballVelocity[1] *= -1
        elif self.ballPosition[1] + PongGame.BALL_SIZE / 2 >= PongGame.BOARD_HEIGHT:
            self.ballPosition[1] = PongGame.BOARD_HEIGHT - PongGame.BALL_SIZE / 2
            self.ballVelocity[1] *= -1

        # Handle hitting ball back
        ballL = self.ballPosition[0] - PongGame.BALL_SIZE / 2
        ballR = self.ballPosition[0] + PongGame.BALL_SIZE / 2
        if ballL > self.paddlePositionsX[0] and ballL <= self.paddlePositionsX[0] and self.ballVelocity[0] < 0:
            self.ballVelocity[0] *= -1
        elif ballR < self.paddlePositionsX[1] and ballR >= self.paddlePositionsX[1] and self.ballVelocity[0] > 0:
            self.ballVelocity[0] *= -1

        # Player response
        for ind, p in enumerate(players):
            playerMove = p.makeMove(getBoardState(ind))
            if playerMove == PongGame.MOVE_UP:
                self.paddlePositionsY[ind] -= PongGame.PADDLE_VELOCITY
                if self.paddlePositionsY[1] - PongGame.PADDLE_HEIGHT / 2 < 0:
                    self.paddlePositionsY[1] = PongGame.PADDLE_HEIGHT / 2
            elif playerMove == PongGame.MOVE_DOWN:
                self.paddlePositionsY[ind] += PongGame.PADDLE_VELOCITY
                if self.paddlePositionsY[1] + PongGame.PADDLE_HEIGHT / 2 >= PongGame.BOARD_HEIGHT:
                    self.paddlePositionsY[1] = PongGame.BOARD_HEIGHT - PongGame.PADDLE_HEIGHT / 2 - 1
            elif playerMove == PongGame.MOVE_STAY:
                pass
            else:
                print("Invalid move (", playerMove, ") for player:", p)
    
    def getBoardState(self, currentPlayerInd):
        # The board state is [currPos, otherPos, ballPos]
        return [self.paddlePositionsY[currentPlayerInd][::], self.paddlesPositionsY[1 - currentPlayerInd][::], self.ballPosition[::]]

    def getScore(self):
        return self.score[::]

    def resetBallPosition(self):
        self.ballPosition = [PongGame.BOARD_WIDTH / 2, PongGame.BOARD_HEIGHT / 2]
        self.ballVelocity = [PongGame.BALL_VELOCITY_SCALAR * (2 * random.randint(0, 1) - 1), PongGame.BALL_VELOCITY_SCALAR * (2 * random.randint(0, 1) - 1)]


class PongPlayer:

    def __init__(self):
        pass

    # Provide the board state and return the desired move
    def makeMove(boardState):
        resultMove = PongGame.MOVE_STAY

        return resultMove