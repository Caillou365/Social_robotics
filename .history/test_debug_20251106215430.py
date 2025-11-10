import serial
import threading
import numpy as np
import pygame
import time
from env.fauteuil_env import FauteuilEnv
from config import config

current_action = np.array([0.0, 0.0])
running = True

def read_arduino():
    global current_action, running
    try:
        arduino = serial.Serial('COM4', 9600, timeout=1)
        print("🔌 Connexion Arduino établie sur COM4.")
        while running:
            data = arduino.readline().decode('utf-8').strip()
            if data:
                try:
                    x, y = map(float, data.split(','))
                    current_action = np.array([x, y])
                    print(f"🕹️ Action lue : X={x:.2f}, Y={y:.2f}")
                except ValueError:
                    print(f"⚠️ Données invalides : {data}")
    except Exception as e:
        print(f"❌ Erreur Arduino : {e}")
    finally:
        if 'arduino' in locals():
            arduino.close()

# Lance le thread Arduino
arduino_thread = threading.Thread(target=read_arduino)
arduino_thread.daemon = True
arduino_thread.start()

# Initialise l'environnement
env = FauteuilEnv(config)
obs, _ = env.reset()
print("🚀 Environnement initialisé. Position initiale :", env.robot_pos)

try:
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("🚪 Fenêtre fermée par l'utilisateur.")
                running = False
                break

        # Utilise une action fixe pour tester
        current_action = np.array([0.5, 0.0])  # Déplace toujours vers la droite
        print(f"📌 Action appliquée : {current_action}")

        obs, reward, terminated, truncated, info = env.step(current_action)
        print(f"📌 Position après step() : {env.robot_pos}")

        env.render()

        if terminated:
            print("🎯 But atteint ! Réinitialisation...")
            obs, _ = env.reset()

except KeyboardInterrupt:
    print("\n⏹️ Arrêt demandé par l'utilisateur.")
