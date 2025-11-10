import serial
import time
import numpy as np
from env.fauteuil_env import FauteuilEnv
from config import config

try:
    arduino = serial.Serial('COM4', 9600, timeout=1)
    print("Connexion Arduino établie. Attente des données...")
    time.sleep(2)

    env = FauteuilEnv(config)
    obs, _ = env.reset()

    while True:
        data = arduino.readline().decode('utf-8').strip()
        if data:
            print(f"Données brutes : {data}")  # 1. Vérifie le format des données
            try:
                x, y = map(float, data.split(','))
                print(f"Action calculée : [{x}, {y}]")  # 2. Vérifie les valeurs de l'action
                action = np.array([x, y])

                obs, reward, terminated, truncated, info = env.step(action)
                print(f"Récompense : {reward}, Terminé : {terminated}")  # 3. Vérifie la récompense
                env.render()

                if terminated:
                    print("Réinitialisation...")
                    obs, _ = env.reset()

            except ValueError as e:
                print(f"Erreur : {e}")

except Exception as e:
    print(f"Erreur critique : {e}")
finally:
    env.close()
    arduino.close()
