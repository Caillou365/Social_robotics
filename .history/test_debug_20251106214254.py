import serial
import threading
import numpy as np
import pygame
from env.fauteuil_env import FauteuilEnv
from config import config

# Variable globale pour l'action du joystick
current_action = np.array([0.0, 0.0])
running = True

def read_arduino():
    global current_action, running
    try:
        arduino = serial.Serial('COM4', 9600, timeout=1)
        while running:
            data = arduino.readline().decode('utf-8').strip()
            if data:
                try:
                    x, y = map(float, data.split(','))
                    current_action = np.array([x, y])
                except ValueError:
                    pass
    except Exception as e:
        print(f"Erreur Arduino : {e}")
    finally:
        if 'arduino' in locals():
            arduino.close()

# Lance le thread pour lire l'Arduino en arrière-plan
arduino_thread = threading.Thread(target=read_arduino)
arduino_thread.daemon = True  # Le thread s'arrête avec le programme principal
arduino_thread.start()

# Initialise l'environnement
env = FauteuilEnv(config)
obs, _ = env.reset()

try:
    while running:
        # Gère les événements Pygame (fermeture de fenêtre)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

        # Applique l'action et met à jour l'affichage
        obs, reward, terminated, truncated, info = env.step(current_action)
        env.render()

        # Réinitialise si l'épisode est terminé (optionnel)
        if terminated:
            obs, _ = env.reset()

except KeyboardInterrupt:
    print("Arrêt demandé par l'utilisateur.")
except Exception as e:
    print(f"Erreur inattendue : {e}")
finally:
    running = False
    env.close()
    arduino_thread.join(timeout=1)  # Attend la fin du thread Arduino
    print("Programme terminé proprement.")
