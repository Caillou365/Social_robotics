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
    try:
        arduino = serial.Serial('COM4', 9600, timeout=1)
        print("🔌 Connexion Arduino établie sur COM4.")
        while running:
            data = arduino.readline().decode('utf-8').strip()
            if data:
                try:
                    x, y = map(float, data.split(','))
                    current_action = np.array([x, y])
                    print(f"🕹️ Action lue : X={x:.2f}, Y={y:.2f}")  # Affiche les actions du joystick
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
    last_time = time.time()
    step_count = 0

    while running:
        # Gère les événements Pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("🚪 Fenêtre fermée par l'utilisateur.")
                running = False
                break

        # Applique l'action et met à jour l'environnement
        obs, reward, terminated, truncated, info = env.step(current_action)
        step_count += 1

        # Affiche l'état toutes les 10 itérations pour éviter le spam
        if step_count % 10 == 0:
            print(
                f"📊 Étape {step_count} | "
                f"Position : X={env.robot_pos[0]:.2f}, Y={env.robot_pos[1]:.2f} | "
                f"Action : X={current_action[0]:.2f}, Y={current_action[1]:.2f} | "
                f"Récompense : {reward:.2f} | "
                f"Terminé : {terminated}"
            )

        # Réinitialise si nécessaire
        if terminated:
            print("🔄 Réinitialisation (collision ou but atteint).")
            obs, _ = env.reset()

        # Met à jour l'affichage
        env.render()

        # Vérifie si la boucle tourne trop lentement
        current_time = time.time()
        if current_time - last_time > 1.0:  # Si plus d'1 seconde entre les étapes
            print(f"⏳ Boucle lente : {current_time - last_time:.2f}s par étape.")
            last_time = current_time

except KeyboardInterrupt:
    print("\n⏹️ Arrêt demandé par l'utilisateur (Ctrl+C).")
except Exception as e:
    print(f"❌ Erreur inattendue : {e}")
    import traceback
    traceback.print_exc()
finally:
    running = False
    env.close()
    print("🧹 Nettoyage terminé. Programme arrêté.")
