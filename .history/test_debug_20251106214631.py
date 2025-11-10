import pygame
import serial
import threading
import numpy as np
import time
from env.fauteuil_env import FauteuilEnv
from config import config

# Initialise Pygame
pygame.init()
print("🎮 Pygame initialisé avec succès.")

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
obs, _ = env.reset()  # Utilise reset() pour initialiser, pas render()
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

        # Applique l'action
        obs, reward, terminated, truncated, info = env.step(current_action)
        step_count += 1

        if step_count % 10 == 0:
            print(f"📊 Étape {step_count} | Position : {env.robot_pos} | Récompense : {reward:.2f}")

        if terminated:
            print("🔄 Réinitialisation.")
            obs, _ = env.reset()

        env.render()  # Affiche simplement, sans retour

except KeyboardInterrupt:
    print("\n⏹️ Arrêt demandé par l'utilisateur.")
except Exception as e:
    print(f"❌ Erreur inattendue : {e}")
    import traceback
    traceback.print_exc()
finally:
    running = False
    env.close()
    pygame.quit()
    print("🧹 Nettoyage terminé.")
