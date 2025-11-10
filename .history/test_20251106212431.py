import gymnasium as gym
from env.fauteuil_env import FauteuilEnv
from config import config
import serial
import numpy as np
import time
import pygame  # Pour gérer les événements clavier

# Initialise la communication série avec l'Arduino
arduino = serial.Serial('COM4', 9600)  # Remplace 'COM3' par ton port Arduino
time.sleep(2)  # Attend que la connexion s'établisse

# Initialise Pygame pour gérer les événements clavier
pygame.init()

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

            # Réinitialise si l'épisode est terminé
            if terminated:
                obs, _ = env.reset()

            # Gère les événements clavier (pour réinitialiser manuellement)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # Appuie sur 'R' pour réinitialiser
                        obs, _ = env.reset()

except KeyboardInterrupt:
    env.close()
    arduino.close()
