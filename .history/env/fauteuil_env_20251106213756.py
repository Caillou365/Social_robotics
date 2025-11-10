import gymnasium as gym
from gymnasium import spaces
import numpy as np
import pygame
import random

class FauteuilEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, config):
        super(FauteuilEnv, self).__init__()
        # Espace d'action : vitesse en x et y (entre -1 et 1)
        self.action_space = spaces.Box(low=-1, high=1, shape=(2,), dtype=np.float32)
        # Espace d'observation : [robot_x, robot_y, goal_x, goal_y, objets..., humains...]
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(2 + 2 + 100*3 + 100*2,), dtype=np.float32)

        # Paramètres
        self.robot_size = 0.5
        self.max_speed = 1.0
        self.dt = 0.1
        self.config = config
        self.robot_pos = np.zeros(2)
        self.goal_pos = np.array([5.0, 5.0])
        self.objects = []
        self.humans = []
        self.screen = None
        self.clock = None
        self.steps = 0
        self.max_steps = config.get('max_steps', 500)

        # Initialisation de la scène
        self._generate_scene()

    def _generate_scene(self):
        """Génère une scène aléatoire avec objets et humains."""
        self.objects = [
            {'pos': np.array([random.uniform(1, 4), random.uniform(1, 4)]), 'radius': random.uniform(0.3, 0.8)}
            for _ in range(self.config.get('num_objects', 3))
        ]
        self.humans = [
            np.array([random.uniform(1, 4), random.uniform(1, 4)])
            for _ in range(self.config.get('num_humans', 2))
        ]

    def reset(self, seed=None, options=None):
        self.robot_pos = np.zeros(2)
        self.steps = 0
        self._generate_scene()
        return self._get_obs(), {}

    def step(self, action):
        self.robot_pos += action * self.max_speed * self.dt  # Met à jour la position
        reward = -0.1
        terminated = False

        # Vérifie si le but est atteint
        if np.linalg.norm(self.robot_pos - self.goal_pos) < 0.5:
            reward = 10.0
            terminated = True

        # Vérifie les collisions
        for obj in self.objects:
            if np.linalg.norm(self.robot_pos - obj['pos']) < self.robot_size + obj['radius']:
                reward = -10.0
                terminated = True

        return self._get_obs(), reward, terminated, False, {}

    def _get_obs(self):
        """Retourne l'observation complète."""
        obs = np.concatenate([
            self.robot_pos,
            self.goal_pos,
            *[obj['pos'].tolist() + [obj['radius']] for obj in self.objects],
            *[human.tolist() for human in self.humans]
        ])
        return obs.astype(np.float32)

    def render(self):
        if self.screen is None:
            pygame.init()
            self.screen = pygame.display.set_mode((600, 600))
            pygame.display.set_caption("Fauteuil Roulant Intelligent")
            self.clock = pygame.time.Clock()

        self.screen.fill((255, 255, 255))
        # Dessiner le but (vert)
        pygame.draw.circle(self.screen, (0, 255, 0), (int(self.goal_pos[0] * 100), int(self.goal_pos[1] * 100)), 10)
        # Dessiner les objets (bleu)
        for obj in self.objects:
            pygame.draw.circle(self.screen, (0, 0, 255), (int(obj['pos'][0] * 100), int(obj['pos'][1] * 100)), int(obj['radius'] * 100))
        # Dessiner les humains (rouge)
        for human in self.humans:
            pygame.draw.circle(self.screen, (255, 0, 0), (int(human[0] * 100), int(human[1] * 100)), 30)
        # Dessiner le robot (noir)
        pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(int(self.robot_pos[0] * 100) - 25, int(self.robot_pos[1] * 100) - 25, 50, 50))
        pygame.display.flip()
        self.clock.tick(30)

    def close(self):
        if self.screen is not None:
            pygame.quit()
