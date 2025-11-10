import gymnasium as gym
from gymnasium import spaces
import numpy as np
import pygame

class FauteuilEnv(gym.Env):
    def __init__(self, config):
        super().__init__()
        self.action_space = spaces.Box(low=-1, high=1, shape=(2,), dtype=np.float32)
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(4,), dtype=np.float32)
        self.robot_pos = np.array([0.0, 0.0])
        self.screen = None
        self.clock = None

    def reset(self, seed=None, options=None):
        self.robot_pos = np.array([0.0, 0.0])
        return self._get_obs(), {}

    def step(self, action):
        self.robot_pos += action * 0.1  # Déplacement simple
        return self._get_obs(), 0, False, False, {}

    def _get_obs(self):
        return np.concatenate([self.robot_pos])

    def render(self):
        if self.screen is None:
            pygame.init()
            self.screen = pygame.display.set_mode((600, 600))
            self.clock = pygame.time.Clock()

        self.screen.fill((255, 255, 255))
        pygame.draw.rect(self.screen, (0, 0, 0), (int(self.robot_pos[0] * 100) + 250, int(self.robot_pos[1] * 100) + 250, 50, 50))
        pygame.display.flip()
        self.clock.tick(30)

    def close(self):
        if self.screen:
            pygame.quit()
