import gymnasium as gym
from env.fauteuil_env import FauteuilEnv
from config import config
import serial
import numpy as np
import time
import pygame

# Initialise Pygame pour les événements clavier
pygame.init()

try:
    # Connexion à l'Arduino
    arduino = serial.Serial('COM4', 9600, timeout=1)
    print("Connexion Arduino établie sur COM4")
    time.sleep(2)  # Attend que l'Arduino soit prêt

    # Initialise l'environnement
    env = FauteuilEnv(config)
    obs, _ = env.reset()

    while True:
        # Lit les données du joystick
        if arduino.in_waiting > 0:
            data = arduino.readline().decode('utf-8').strip()
            if data:
                try:
                    x, y = map(float, data.split(','))
                    action = np.array([x, y])

                    # Exécute un pas dans l'environnement
                    obs, reward, terminated, truncated, info = env.step(action)
                    env.render()

                    # Réinitialise si terminé
                    if terminated:
                        obs, _ = env.reset()

                    # Gère les événements clavier (touche R)
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                            obs, _ = env.reset()

                except ValueError:
                    print("Données invalides :", data)

except serial.SerialException as e:
    print("Erreur de connexion Arduino :", e)
except KeyboardInterrupt:
    print("Fermeture...")
finally:
    env.close()
    if 'arduino' in locals():
        arduino.close()
