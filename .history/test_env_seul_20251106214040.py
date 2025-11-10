from env.fauteuil_env import FauteuilEnv
from config import config
import time

env = FauteuilEnv(config)
obs, _ = env.reset()

for _ in range(100):
    env.render()  # Doit afficher un carré noir
    time.sleep(0.1)

env.close()
