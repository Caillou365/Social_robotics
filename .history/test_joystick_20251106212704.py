import serial
import time

try:
    arduino = serial.Serial('COM4', 9600, timeout=1)
    print("Connexion réussie sur COM4 !")
    time.sleep(2)  # Attend que l'Arduino soit prêt

    while True:
        if arduino.in_waiting > 0:
            data = arduino.readline().decode('utf-8').strip()
            print("Données reçues :", data)

except serial.SerialException as e:
    print("Erreur :", e)
    print("Essaie de fermer tous les programmes utilisant COM4.")
finally:
    if 'arduino' in locals():
        arduino.close()
