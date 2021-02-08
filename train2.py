import tensorflow as tf 

import game
import random

p1 = game.PerfectPongPlayer()
p2 = game.PerfectPongPlayer()
trainingGame = game.PongGame(p1, p2)

train_inputs = []
train_outputs = []
test_inputs = []
test_outputs = []
"""
for i in range(10000):
    train_inputs.append(trainingGame.getBoardState(0))
    train_outputs.append(p1.makeMove(trainingGame.getBoardState(0)))

    test_inputs.append(trainingGame.getBoardState(1))
    test_outputs.append(p2.makeMove(trainingGame.getBoardState(1)))

    trainingGame.updateGameState()
"""

def generateState():
    return [
        random.randint(int(game.PongGame.PADDLE_HEIGHT / 2), int(game.PongGame.BOARD_HEIGHT - game.PongGame.PADDLE_HEIGHT / 2)),
        random.randint(int(game.PongGame.BALL_SIZE / 2), int(game.PongGame.BOARD_HEIGHT - game.PongGame.BALL_SIZE / 2)),
        random.randint(0, game.PongGame.BOARD_WIDTH),
        [game.PongGame.BALL_VELOCITY_SCALAR, game.PongGame.BALL_VELOCITY_SCALAR * (-1)][random.randint(0, 1)],
        [game.PongGame.BALL_VELOCITY_SCALAR, game.PongGame.BALL_VELOCITY_SCALAR * (-1)][random.randint(0, 1)]
    ]

for i in range(10000):
    state = generateState()
    train_inputs.append(state)
    train_outputs.append(p1.makeMove(state))

    state = generateState()
    test_inputs.append(state)
    test_outputs.append(p1.makeMove(state))


model = tf.keras.Sequential([
    tf.keras.layers.Flatten(input_shape=(5, 1)),
    tf.keras.layers.Dense(16, activation="relu"),
    tf.keras.layers.Dense(3)
])

model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

model.fit(train_inputs, train_outputs, epochs=5000)

test_loss, test_acc = model.evaluate(test_inputs, test_outputs, verbose=2)
print("\nTest accuracy:", test_acc)

model.save("ml_models/final")