import gym
import numpy as np
from gym import spaces
import pygame
import random
import math

class CatchEnv(gym.Env):
    def __init__(self):
        super(CatchEnv, self).__init__()
        self.width = 400
        self.height = 400
        self.bucket_width = 40
        self.bucket_height = 20
        self.ball_radius = 10
        self.speed = 5

        self.action_space = spaces.Discrete(3)  # 0 = left, 1 = stay, 2 = right
        self.observation_space = spaces.Box(low=0, high=1, shape=(5,), dtype=np.float32)

        self.window = None
        self.clock = None
        self.font = None
        self.score = 0
        self.BLACK = (0, 0, 0)

        self._setup_pygame()
        self.reset()

    def _setup_pygame(self):
        pygame.init()
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Catch Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 24)

    def reset(self):
        self.bucket_x = 200
        self.ball_x = np.random.randint(0, self.width)
        self.ball_y = 0

        self.angle = random.randint(60, 120)
        rad = math.radians(self.angle)
        self.ball_vx = self.speed * math.cos(rad)
        self.ball_vy = self.speed * math.sin(rad)

        self.direction_locked = None
        return self._get_obs()

    def step(self, action):
        reward = 0

        # Store pre-movement position
        prev_bucket_x = self.bucket_x

        # Lock direction on first move
        if self.direction_locked is None:
            if action == 0:
                self.direction_locked = "left"
            elif action == 2:
                self.direction_locked = "right"

        # Move if direction matches lock
        if self.direction_locked == "left" and action == 0:
            self.bucket_x -= 10
        elif self.direction_locked == "right" and action == 2:
            self.bucket_x += 10

        # Clip bucket position
        self.bucket_x = np.clip(self.bucket_x, 0, self.width - self.bucket_width)

        # Penalize if clipped (wall collision)
        if (prev_bucket_x != self.bucket_x) and (self.bucket_x == 0 or self.bucket_x == self.width - self.bucket_width):
            reward -= 0.1

        # Move the ball
        self.ball_x += self.ball_vx
        self.ball_y += self.ball_vy

        # Bounce off walls
        if self.ball_x <= 0 or self.ball_x >= self.width:
            self.ball_vx *= -1
            self.ball_x = np.clip(self.ball_x, 0, self.width)

        # Done if ball hits bottom
        done = False
        if self.ball_y > self.height:
            done = True
            distance = abs((self.bucket_x + self.bucket_width / 2) - self.ball_x)
            reward = -distance / (self.width / 2)

            if distance < self.bucket_width / 2:
                reward += 1
                self.score += 1
            else:
                reward -= 1
                self.score -= 1

        return self._get_obs(), reward, done, {}

    def _get_obs(self):
        return np.array([
            self.bucket_x / self.width,
            self.ball_x / self.width,
            self.ball_y / self.height,
            self.ball_vx / self.width,
            self.ball_vy / self.height
        ], dtype=np.float32)

    def render(self, mode='human'):
        if self.window is None:
            self._setup_pygame()

        pygame.event.pump()
        self.window.fill((255, 255, 255))

        # Draw the bucket
        pygame.draw.rect(
            self.window,
            (0, 0, 255),
            (int(self.bucket_x), self.height - self.bucket_height - 10,
             self.bucket_width, self.bucket_height)
        )

        # Draw the ball
        pygame.draw.circle(
            self.window,
            (255, 0, 0),
            (int(self.ball_x), int(self.ball_y)),
            self.ball_radius
        )

        # Draw score
        score_text = self.font.render(f"Score: {round(self.score, 2)}", True, self.BLACK)
        self.window.blit(score_text, (10, 10))

        pygame.display.flip()
        self.clock.tick(60)

    def close(self):
        if self.window:
            pygame.quit()
