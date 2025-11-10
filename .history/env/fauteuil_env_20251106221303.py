import gymnasium as gym
from gymnasium import spaces
import numpy as np
import pygame

class FauteuilEnv(gym.Env):
    def __init__(self, config):
        super(FauteuilEnv, self).__init__()
        self.action_space = spaces.Box(low=-1, high=1, shape=(2,), dtype=np.float32)
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(4,), dtype=np.float32)

        self.robot_pos = np.array([0.0, 0.0], dtype=np.float32)
        self.goal_pos = np.array([5.0, 5.0], dtype=np.float32)
        self.max_speed = 0.5
        
        # Obstacles (cercles : x, y, rayon)
        self.objects = [{"pos": np.array([3.0, 4.0]), "radius": 0.5},
                        {"pos": np.array([6.0, 2.0]), "radius": 0.7}]

        # Personnes (points : x, y)
        self.humans = [np.array([2.0, 5.0]),
                    np.array([7.0, 8.0])]

        pygame.init()
        self.screen = pygame.display.set_mode((600, 600))
        pygame.display.set_caption("Fauteuil Roulant Intelligent")
        self.clock = pygame.time.Clock()

    def reset(self, seed=None, options=None):
        self.robot_pos = np.array([0.0, 0.0], dtype=np.float32)
        return self._get_obs(), {}

    def step(self, action):
        # Met à jour la position
        self.robot_pos += action * self.max_speed

        # Limite le fauteuil à l'écran (coordonnées entre 0 et 10 pour un affichage 600x600)
        self.robot_pos[0] = np.clip(self.robot_pos[0], 0, 10)  # Limite en X
        self.robot_pos[1] = np.clip(self.robot_pos[1], 0, 10)  # Limite en Y

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
        self.screen.fill((255, 255, 255))

        # Dessine le but (cercle vert)
        pygame.draw.circle(
            self.screen,
            (0, 255, 0),
            (int(self.goal_pos[0] * 50) + 300, int(self.goal_pos[1] * 50) + 300),
            10
        )

        # Dessine le fauteuil (carré noir)
        pygame.draw.rect(
            self.screen,
            (0, 0, 0),
            (
                int(self.robot_pos[0] * 50) + 275,
                int(self.robot_pos[1] * 50) + 275,
                50,
                50
            )
        )

        pygame.display.flip()
        self.clock.tick(30)

    def close(self):
        if self.screen is not None:
            pygame.quit()
