from env.fauteuil_env import FauteuilEnv
from config import config
import numpy as np

env = FauteuilEnv(config)
obs, _ = env.reset()

for _ in range(100):
    action = env.action_space.sample()  # Action aléatoire
    obs, reward, terminated, truncated, info = env.step(action)
    env.render()
    if terminated:
        obs, _ = env.reset()

env.close()
