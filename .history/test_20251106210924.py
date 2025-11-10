import gymnasium as gym
from env.fauteuil_env import FauteuilEnv
from config import config

# Initialisation
env = FauteuilEnv(config)
obs, _ = env.reset()

# Boucle de test
for _ in range(1000):
    action = env.action_space.sample()  # Action aléatoire
    obs, reward, terminated, truncated, info = env.step(action)
    env.render()
    if terminated:
        obs, _ = env.reset()

env.close()
