from stable_baselines3 import DQN
from catch_env import CatchEnv
import time

env = CatchEnv()
model = DQN.load("model/catch_model.zip")  

NUM_EPISODES = 10 

for episode in range(NUM_EPISODES):
    obs = env.reset()
    done = False
    while not done:
        action, _ = model.predict(obs)
        obs, reward, done, _ = env.step(action)
        env.render()

env.close()
