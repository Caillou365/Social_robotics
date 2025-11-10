import serial
import threading
import numpy as np
import pygame
import time
from env.fauteuil_env import FauteuilEnv
from config import config

# Variables globales
current_action = np.array([0.0, 0.0])
running = True

def read_arduino():
    global current_action, running
    arduino = serial.Serial('COM4', 9600, timeout=0.1)
    buffer = ""
    print("🔌 Connexion Arduino établie sur COM4. Bouge le joystick !")
    while running:
        data = arduino.read(arduino.in_waiting or 1).decode('utf-8')
        if data:
            buffer += data
            while '\n' in buffer:
                line, buffer = buffer.split('\n', 1)
                try:
                    x, y = map(float, line.strip().split(','))
                    current_action = np.array([x, y])
                    print(f"🕹️ Joystick : X={x:.2f}, Y={y:.2f}")
                except ValueError:
                    print(f"⚠️ Données invalides : {line.strip()}")
        time.sleep(0.01)

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

        # Applique l'action du joystick
        obs, reward, terminated
