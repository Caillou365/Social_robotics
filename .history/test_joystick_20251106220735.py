import serial
import time

arduino = serial.Serial('COM4', 9600, timeout=0.1)  # Timeout court
print("Connexion Arduino établie. Bouge le joystick !")

buffer = ""  # Buffer pour accumuler les données

try:
    while True:
        # Lit les données disponibles
        data = arduino.read(arduino.in_waiting or 1).decode('utf-8')
        if data:
            buffer += data
            # Cherche la fin de ligne
            while '\n' in buffer:
                line, buffer = buffer.split('\n', 1)
                try:
                    x, y = map(float, line.strip().split(','))
                    print(f"Joystick : X={x:.2f}, Y={y:.2f}")
                except ValueError:
                    print(f"Données invalides : {line.strip()}")
        time.sleep(0.01)  # Délai très court
except KeyboardInterrupt:
    arduino.close()
    print("Fermeture.")
