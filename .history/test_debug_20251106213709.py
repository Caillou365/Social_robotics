import serial
import time
import numpy as np
from env.fauteuil_env import FauteuilEnv
from config import config
import pygame

# Initialise Pygame et l'environnement
pygame.init()
env = FauteuilEnv(config)
obs, _ = env.reset()

# Connexion Arduino
arduino = serial.Serial('COM4', 9600, timeout=1)
print("Connexion Arduino établie. Déplace le joystick !")

try:
    while True:
        data = arduino.readline().decode('utf-8').strip()
        if data:
            try:
                x, y = map(float, data.split(','))
                action = np.array([x, y])  # Convertit en action pour Gymnasium
                print(f"Action : {action}")  # Affiche l'action

                # Applique l'action dans l'environnement
                obs, reward, terminated, truncated, info = env.step(action)
                env.render()  # Met à jour l'affichage

                # Réinitialise si nécessaire
                if terminated:
                    print("Réinitialisation...")
                    obs, _ = env.reset()

                # Gère la fermeture de la fenêtre
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        raise KeyboardInterrupt

            except ValueError:
                print(f"Données invalides : {data}")

except KeyboardInterrupt:
    print("Arrêt demandé.")
finally:
    env.close()
    arduino.close()
