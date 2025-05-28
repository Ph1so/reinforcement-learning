import pygame
import imageio
import numpy as np
from stable_baselines3 import DQN
from catch_env import CatchEnv

# Setup
env = CatchEnv()
model = DQN.load("model/catch_model.zip")
frames = []

NUM_EPISODES = 3

for _ in range(NUM_EPISODES):
    obs = env.reset()
    done = False

    while not done:
        action, _ = model.predict(obs)
        obs, reward, done, _ = env.step(action)

        # Render and capture frame
        env.render()
        frame = pygame.surfarray.array3d(env.window)
        frame = np.transpose(frame, (1, 0, 2))  # (W, H, C) -> (H, W, C)
        frames.append(frame)

# Save to GIF
imageio.mimsave("catcher_agent.gif", frames, fps=30)

env.close()
