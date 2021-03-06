import game

import numpy as np

import gym
from gym import spaces
from gym.utils import seeding

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

import game

class PongGym(gym.Env):

    def __init__(self):
        self.action_space = spaces.Discrete(3)
        self.observation_space = spaces.Tuple( (spaces.Box(low=0, high=(game.PongGame.BOARD_HEIGHT - 1), dtype=np.float32, shape=(5,1)),
                                                spaces.Box(low=0, high=(game.PongGame.BOARD_WIDTH - 1), dtype=np.float32, shape=(5,1)),
                                                spaces.Box(low=0, high=(game.PongGame.BOARD_HEIGHT - 1), dtype=np.float32, shape=(5,1)),
                                                spaces.Box(low=0, high=(game.PongGame.BOARD_WIDTH - 1), dtype=np.float32, shape=(5,1)),
                                                spaces.Box(low=0, high=(game.PongGame.BOARD_HEIGHT - 1), dtype=np.float32, shape=(5,1))))
        self.seed()
        self.reset()

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)

    def step(self, action):
        reward = 0
        done = False
        initialScore = self.game.getScore()
        initialBallDir = self.game.getBoardState(1)[3]
        self.dummy.setNextMove(action)
        self.game.updateGameState()
        newScore = self.game.getScore()
        if newScore[0] > initialScore[0]:
            reward = -1
            reward = -1 * (self.game.getBoardState(1)[0] - self.game.getBoardState(1)[2]) ** 2
            #print("CONCEDED")
            done = True
        if initialBallDir < 0 and self.game.getBoardState(1)[3] > 0:
            reward = 100
            print("RETURNED")
        #if newScore[1] > initialScore[1]:
        #    reward = 1.5

        return self.game.getBoardState(1), reward, done, {}

    def reset(self):
        self.dummy = game.DummyPongPlayer()
        self.game = game.PongGame(game.PerfectPongPlayer(), self.dummy)

        return self.game.getBoardState(1)


print("Initialising")
seed = 42
gamma = 0.99
max_steps_per_episode = 1000
env = PongGym()
env.seed(seed)
eps = np.finfo(np.float32).eps.item()

num_inputs = 5 # From the game state
num_actions = 3
num_hidden = 3

inputs = layers.Input(shape=(num_inputs,))
common = layers.Dense(num_hidden, activation="sigmoid")(inputs)
action = layers.Dense(num_actions, activation="softmax")(common)
critic = layers.Dense(1)(common)

model = keras.Model(inputs=inputs, outputs=[action, critic])

optimiser = keras.optimizers.Adam(learning_rate=0.05)
huber_loss = keras.losses.Huber()
action_probs_history = []
critic_value_history = []
rewards_history = []
running_reward = 0
episode_count = 0

print("Starting training")

while True:
    state = env.reset()
    episode_reward = 0
    with tf.GradientTape() as tape:
        for timestep in range(1, max_steps_per_episode):
            state = tf.convert_to_tensor(state)
            state = tf.expand_dims(state, 0)

            action_probs, critic_value = model(state)
            critic_value_history.append(critic_value[0, 0])

            action = np.random.choice(num_actions, p=np.squeeze(action_probs))
            action_probs_history.append(tf.math.log(action_probs[0, action]))

            state, reward, done, _ = env.step(action)
            rewards_history.append(reward)
            episode_reward += reward

            if done:
                break
        running_reward = 0.05 * episode_reward + (1 - 0.05) * running_reward

        returns = []
        discounted_sum = 0
        for r in rewards_history[::-1]:
            discounted_sum = r + gamma * discounted_sum
            returns.insert(0, discounted_sum)

        returns = np.array(returns)
        returns = (returns - np.mean(returns)) / (np.std(returns) + eps)
        returns = returns.tolist()

        history = zip(action_probs_history, critic_value_history, returns)
        actor_losses = []
        critic_losses = []
        for log_prob, value, ret in history:
            diff = ret - value
            actor_losses.append(-log_prob * diff)
            critic_losses.append(huber_loss(tf.expand_dims(value, 0), tf.expand_dims(ret, 0)))

        loss_value = sum(actor_losses) + sum(critic_losses)
        grads = tape.gradient(loss_value, model.trainable_variables)
        optimiser.apply_gradients(zip(grads, model.trainable_variables))

        action_probs_history.clear()
        critic_value_history.clear()
        rewards_history.clear()
    
    episode_count += 1
    print("Episodes completed:", episode_count)
    if episode_count % 10 == 0:
        print("running reward:", str(running_reward), "at episode", str(episode_count))
        model.save("models/episode_" + str(episode_count))
        model.save("models/final")
    
    if running_reward > 10000:
        print("Solved at episode", str(episode_count))
        break

model.save("models/final")
print("Training completed successfully")