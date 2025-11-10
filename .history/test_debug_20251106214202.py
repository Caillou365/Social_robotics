import serial
import threading
import numpy as np
from env.fauteuil_env import FauteuilEnv
from config import config

current_action = np.array([0.0, 0.0])

def read_arduino():
    global current_action
    arduino = serial.Serial('COM4', 9600, timeout=1)
    while True:
        data = arduino.readline().decode('utf-8').strip()
        if data:
            try:
                x, y = map(float, data.split(','))
                current_action = np.array([x, y])
            except ValueError:
                pass

threading.Thread(target=read_arduino, daemon=True).start()

env = FauteuilEnv(config)
obs, _ = env.reset()

try:
    while True:
        env.step(current_action)
        env.render()
except KeyboardInterrupt:
    env.close()
