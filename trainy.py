from stable_baselines3 import DQN
from stable_baselines3.common.callbacks import BaseCallback
from catch_env import CatchEnv
import pygame
import time

class RenderEveryNCallback(BaseCallback):
    def __init__(self, env, render_freq=5000, verbose=0):
        super().__init__(verbose)
        self.env = env
        self.render_freq = render_freq

    def _on_step(self) -> bool:
        if self.n_calls % self.render_freq == 0:
            obs = self.env.reset()
            done = False
            while not done:
                action, _ = self.model.predict(obs)
                obs, _, done, _ = self.env.step(action)
                self.env.render()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.env.close()
                        exit()
                time.sleep(0.01)
        return True

# Create envs
train_env = CatchEnv()
render_env = CatchEnv()

model = DQN("MlpPolicy", train_env, verbose=1)

# Train and show rendering every 5000 steps
model.learn(total_timesteps=1000000, callback=RenderEveryNCallback(render_env, render_freq=5000))

# Save trained model
model.save("model/catch_model")
train_env.close()
render_env.close()
