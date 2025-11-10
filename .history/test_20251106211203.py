import gymnasium as gym
from env.fauteuil_env import FauteuilEnv
from config import config
import serial
import time

# Initialise la communication série avec l'Arduino
arduino = serial.Serial('COM3', 9600)  # Remplace 'COM3' par le port de ton Arduino
time.sleep(2)  # Attend que la connexion s'établisse

env = FauteuilEnv(config)
obs, _ = env.reset()

try:
    while True:
        # Lit les données du joystick (format : "X,Y\n")
        data = arduino.readline().decode('utf-8').strip()
        if data:
            x, y = map(float, data.split(','))
            action = np.array([x, y])  # Convertit en action pour Gymnasium

            # Exécute un pas dans l'environnement
            obs, reward, terminated, truncated, info = env.step(action)
            env.render()

            if terminated:
                obs, _ = env.reset()

except KeyboardInterrupt:
    env.close()
    arduino.close()
