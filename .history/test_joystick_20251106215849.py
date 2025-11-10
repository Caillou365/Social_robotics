import serial
import time

arduino = serial.Serial('COM4', 9600, timeout=1)
print("Connexion Arduino établie. Bouge le joystick !")

try:
    while True:
        data = arduino.readline().decode('utf-8').strip()
        if data:
            try:
                x, y = map(float, data.split(','))
                print(f"Joystick : X={x:.2f}, Y={y:.2f}")
            except ValueError:
                print(f"Données invalides : {data}")
        time.sleep(0.1)
except KeyboardInterrupt:
    arduino.close()
    print("Fermeture.")
