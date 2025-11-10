import gymnasium as gym
from gymnasium import spaces
import numpy as np
import pygame
import random

class FauteuilEnv(gym.Env):
    def __init__(self, config):
        super(FauteuilEnv, self).__init__()
        # Espaces d'action et d'observation
        self.action_space = spaces.Box(low=-1, high=1, shape=(2,), dtype=np.float32)
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(4,), dtype=np.float32)

        # Paramètres
        self.robot_pos = np.array([0.0, 0.0], dtype=np.float32)
        self.goal_pos = np.array([5.0, 5.0], dtype=np.float32)
        self.max_speed = 0.1

        # Initialisation de Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((600, 600))
        pygame.display.set_caption("Fauteuil Roulant Intelligent")
        self.clock = pygame.time.Clock()  # Initialise le clock ici !

    def reset(self, seed=None, options=None):
        self.robot_pos = np.array([0.0, 0.0], dtype=np.float32)
        return self._get_obs(), {}

    def step(self, action):
        self.robot_pos += action * self.max_speed
        reward = -0.1

        if np.linalg.norm(self.robot_pos - self.goal_pos) < 0.5:
            reward = 10.0
            terminated = True
        else:
            terminated = False

        return self._get_obs(), reward, terminated, False, {}

    def _get_obs(self):
        return np.concatenate([self.robot_pos, self.goal_pos])

    def render(self):
        if self.screen is None:
            pygame.init()
            self.screen = pygame.display.set_mode((600, 600))
            self.clock = pygame.time.Clock()  # Réinitialise le clock si nécessaire

        self.screen.fill((255, 255, 255))
        pygame.draw.circle(self.screen, (0, 255, 0), (int(self.goal_pos[0] * 100), int(self.goal_pos[1] * 100)), 10)
        pygame.draw.rect(self.screen, (0, 0, 0), (int(self.robot_pos[0] * 100) - 25, int(self.robot_pos[1] * 100) - 25, 50, 50))
        pygame.display.flip()
        self.clock.tick(30)  # Maintenant self.clock est toujours initialisé

    def close(self):
        if self.screen is not None:
            pygame.quit()
