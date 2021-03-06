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
    try:
        while True:
          # Solange Button nicht gedrueckt wird (False)
          if not GPIO.input(PIN_IN):
            GPIO.output(PIN_OUT, False)
          # Wenn der Button gedrueckt wird
          else:
            GPIO.output(PIN_OUT, True)
            time.sleep(0.25)
            GPIO.output(PIN_OUT, False)
            time.sleep(0.25)
        # Beim Abbruch durch STRG+C resetten
    except KeyboardInterrupt:
        print("Programm vom User gestoppt")
        GPIO.cleanup()