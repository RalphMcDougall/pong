import random
import display
import pygame

import tensorflow as tf
from tensorflow import keras

class PongGame:
    BOARD_WIDTH = 1000
    BOARD_HEIGHT = 600
    PADDLE_WIDTH = 10
    PADDLE_HEIGHT = 50

    PADDLE_HOR_BUFFER = 5

    PADDLE_VELOCITY = 4

    BALL_SIZE = 4
    BALL_VELOCITY_SCALAR = 6

    MOVE_UP = 0
    MOVE_DOWN = 1
    MOVE_STAY = 2

    def __init__(self, player1, player2):
        self.players = [player1, player2]
        self.resetBoardState()
        self.score = [0, 0]

    def updateGameState(self):
        self.ballPosition[0] += self.ballVelocity[0]
        self.ballPosition[1] += self.ballVelocity[1]

        # Ball out of bounds
        if self.ballPosition[0] < PongGame.PADDLE_HOR_BUFFER:
            self.score[1] += 1
            self.resetBoardState()
        elif self.ballPosition[0] > PongGame.BOARD_WIDTH - PongGame.PADDLE_HOR_BUFFER:
            self.score[0] += 1
            self.resetBoardState()
        
        # Top bounce
        if self.ballPosition[1] - PongGame.BALL_SIZE / 2 < 0:
            self.ballPosition[1] = PongGame.BALL_SIZE / 2
            self.ballVelocity[1] *= -1
        elif self.ballPosition[1] + PongGame.BALL_SIZE / 2 >= PongGame.BOARD_HEIGHT:
            self.ballPosition[1] = PongGame.BOARD_HEIGHT - PongGame.BALL_SIZE / 2
            self.ballVelocity[1] *= -1

        # Handle hitting ball back
        ballL = self.ballPosition[0] - PongGame.BALL_SIZE / 2
        ballR = self.ballPosition[0] + PongGame.BALL_SIZE / 2
        if (ballL > self.paddlePositionsX[0] - PongGame.PADDLE_WIDTH / 2) and (ballL <= self.paddlePositionsX[0] + PongGame.PADDLE_WIDTH / 2) and (self.ballVelocity[0] < 0) and (self.ballPosition[1] - PongGame.BALL_SIZE / 2 > self.paddlePositionsY[0] - PongGame.PADDLE_HEIGHT / 2) and (self.ballPosition[1] + PongGame.BALL_SIZE / 2 < self.paddlePositionsY[0] + PongGame.PADDLE_HEIGHT / 2):
            self.ballVelocity[0] *= -1
        elif (ballR < self.paddlePositionsX[1] + PongGame.PADDLE_WIDTH / 2) and (ballR >= self.paddlePositionsX[1] - PongGame.PADDLE_WIDTH / 2) and (self.ballVelocity[0] > 0) and (self.ballPosition[1] - PongGame.BALL_SIZE / 2 > self.paddlePositionsY[1] - PongGame.PADDLE_HEIGHT / 2) and (self.ballPosition[1] + PongGame.BALL_SIZE / 2 < self.paddlePositionsY[1] + PongGame.PADDLE_HEIGHT / 2):
            self.ballVelocity[0] *= -1

        # Player response
        for ind, p in enumerate(self.players):
            playerMove = p.makeMove(self.getBoardState(ind))
            if playerMove == PongGame.MOVE_UP:
                self.paddlePositionsY[ind] -= PongGame.PADDLE_VELOCITY
                if self.paddlePositionsY[ind] - PongGame.PADDLE_HEIGHT / 2 < 0:
                    self.paddlePositionsY[ind] = PongGame.PADDLE_HEIGHT / 2
            elif playerMove == PongGame.MOVE_DOWN:
                self.paddlePositionsY[ind] += PongGame.PADDLE_VELOCITY
                if self.paddlePositionsY[ind] + PongGame.PADDLE_HEIGHT / 2 >= PongGame.BOARD_HEIGHT:
                    self.paddlePositionsY[ind] = PongGame.BOARD_HEIGHT - PongGame.PADDLE_HEIGHT / 2 - 1
            elif playerMove == PongGame.MOVE_STAY:
                pass
            else:
                print("Invalid move (", playerMove, ") for player:", p)
    
    def getBoardState(self, currentPlayerInd):
        # The board state is [currPos, otherPos, ballPosX (depending on player), ballPosY]
        return [self.paddlePositionsY[currentPlayerInd],
                [self.ballPosition[0], PongGame.BOARD_WIDTH - self.ballPosition[0] - 1][currentPlayerInd], 
                self.ballPosition[1],
                [self.ballVelocity[0], self.ballVelocity[0] * (-1)][currentPlayerInd],
                self.ballVelocity[1]]

    def getScore(self):
        return self.score[::]

    def resetBoardState(self):
        self.paddlePositionsX = [
            0 + PongGame.PADDLE_WIDTH / 2 + PongGame.PADDLE_HOR_BUFFER,
            PongGame.BOARD_WIDTH - PongGame.PADDLE_WIDTH / 2 - PongGame.PADDLE_HOR_BUFFER
        ]
        self.paddlePositionsY = [
            PongGame.BOARD_HEIGHT / 2, 
            PongGame.BOARD_HEIGHT / 2
        ]
        self.ballPosition = [PongGame.BOARD_WIDTH / 2, PongGame.BOARD_HEIGHT / 2]
        self.ballVelocity = [PongGame.BALL_VELOCITY_SCALAR * (2 * random.randint(0, 1) - 1), PongGame.BALL_VELOCITY_SCALAR * (2 * random.randint(0, 1) - 1)]

    def drawToScreen(self, screenSurface):
        # Draw ball
        pygame.draw.rect(screenSurface, display.WHITE, ( int(self.ballPosition[0] - PongGame.BALL_SIZE / 2), 
                                                                int(self.ballPosition[1] - PongGame.BALL_SIZE / 2), 
                                                                PongGame.BALL_SIZE, 
                                                                PongGame.BALL_SIZE))
        # Draw paddles
        for i in range(len(self.players)):
            pygame.draw.rect(screenSurface, display.WHITE, ( int(self.paddlePositionsX[i] - PongGame.PADDLE_WIDTH / 2), 
                                                                    int(self.paddlePositionsY[i] - PongGame.PADDLE_HEIGHT / 2), 
                                                                    PongGame.PADDLE_WIDTH, 
                                                                    PongGame.PADDLE_HEIGHT))
        
        s1Surface = display.SCORE_FONT.render(str(self.score[0]), False, display.WHITE)
        s2Surface = display.SCORE_FONT.render(str(self.score[1]), False, display.WHITE)

        screenSurface.blit(s1Surface, (PongGame.BOARD_WIDTH / 2 - 50 - display.SCORE_FONT_SIZE / 2, 10))
        screenSurface.blit(s2Surface, (PongGame.BOARD_WIDTH / 2 + 50, 10))

        pygame.draw.line(screenSurface, display.WHITE, (PongGame.BOARD_WIDTH / 2, 0), (PongGame.BOARD_WIDTH / 2, PongGame.BOARD_HEIGHT), 1)


class PongPlayer:

    def __init__(self):
        pass

    # Provide the board state and return the desired move
    def makeMove(self, boardState):
        resultMove = PongGame.MOVE_STAY

        return resultMove


class UserControlledPongPlayer(PongPlayer):

    def __init__(self):
        pass

    def makeMove(self, boardState):
        resultMove = PongGame.MOVE_STAY

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]:
            resultMove = PongGame.MOVE_UP
        elif pressed[pygame.K_DOWN]:
            resultMove = PongGame.MOVE_DOWN

        return resultMove


class BasicPongPlayer(PongPlayer):

    def __init__(self):
        pass

    def makeMove(self, boardState):
        resultMove = PongGame.MOVE_STAY
        if boardState[0] < boardState[2]:
            resultMove = PongGame.MOVE_DOWN
        elif boardState[0] > boardState[2]:
            resultMove = PongGame.MOVE_UP
        return resultMove

class PerfectPongPlayer(PongPlayer):

    def __init__(self):
        pass

    def makeMove(self, boardState):
        resultMove = PongGame.MOVE_STAY
        
        # This can be more efficient, but it's fine for now
        targetY = -1

        ballX = boardState[1]
        ballY = boardState[2]
        ballVX = boardState[3]
        ballVY = boardState[4]

        while ballX > PongGame.PADDLE_HOR_BUFFER + PongGame.PADDLE_WIDTH:
            ballX += ballVX
            ballY += ballVY

            if ballY - PongGame.BALL_SIZE / 2 < 0:
                ballY = PongGame.BALL_SIZE / 2
                ballVY *= -1
            elif ballY + PongGame.BALL_SIZE / 2 >= PongGame.BOARD_HEIGHT:
                ballY = PongGame.BOARD_HEIGHT - PongGame.BALL_SIZE / 2 - 1
                ballVY *= -1
            
            if ballX + PongGame.BALL_SIZE / 2 >= PongGame.BOARD_WIDTH - PongGame.PADDLE_HOR_BUFFER - PongGame.PADDLE_WIDTH:
                ballX = PongGame.BOARD_WIDTH - PongGame.PADDLE_HOR_BUFFER - PongGame.PADDLE_WIDTH - PongGame.BALL_SIZE / 2
                ballVX *= -1
        targetY = ballY
        
        if abs(boardState[0] - targetY) < PongGame.PADDLE_HEIGHT / 4:
            resultMove = PongGame.MOVE_STAY
        elif boardState[0] < targetY:
            resultMove = PongGame.MOVE_DOWN
        elif boardState[0] > targetY:
            resultMove = PongGame.MOVE_UP


        return resultMove


class RLPongPlayer(PongPlayer):

    def __init__(self):
        print("Loading model")
        self.model = keras.models.load_model("models/final")
        print(self.model.summary())
        print("Model: " + str(self.model))

    def makeMove(self, boardState):
        state = tf.convert_to_tensor(boardState)
        state = tf.expand_dims(state, 0)

        action_probs, critic_value = self.model(state)

        print(action_probs.numpy())
        #mVal = max(action_probs[0])
        #print(mVal)
        #print(mVal.numpy())

        nextMoveInd = tf.math.argmax(action_probs[0]).numpy()
        print(nextMoveInd)

        return nextMoveInd