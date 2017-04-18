#!/usr/bin/python
'''
Created on 16.04.2017

@author: patrik
'''

# Verwenden von GPIO
import RPi.GPIO as GPIO
import time

# Warnungen ausschalten
#GPIO.setwarnings(False)
# Pin Nummern verwenden
GPIO.setmode(GPIO.BOARD)

#GPIO Pins zuweisen
PIN_IN = 11
PIN_OUT = 12

# Pin 17 als Input
GPIO.setup(PIN_IN, GPIO.IN)
# Pin 18 als Output
GPIO.setup(PIN_OUT, GPIO.OUT)

if __name__ == '__main__':
    p = GPIO.PWM(PIN_OUT, 50)  # channel=12 frequency=50Hz
    try:
        while True:
          # Solange Button nicht gedrueckt wird (False)
          if not GPIO.input(PIN_IN):
            p.stop()
          # Wenn der Button gedrueckt wird
          else:
            p.start(0)
            for dc in range(0, 101, 5):
                p.ChangeDutyCycle(dc)
                time.sleep(0.1)
            for dc in range(100, -1, -5):
                p.ChangeDutyCycle(dc)
                time.sleep(0.1)
        # Beim Abbruch durch STRG+C resetten
    except KeyboardInterrupt:
        print("Programm vom User gestoppt")
        pass
        p.stop()
        GPIO.cleanup()