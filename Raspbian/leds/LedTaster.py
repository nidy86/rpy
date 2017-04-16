#!/usr/bin/python
'''
Created on 16.04.2017

@author: patrik
'''

# Verwenden von GPIO
import RPi.GPIO as GPIO

# Warnungen ausschalten
#GPIO.setwarnings(False)
# Pin Nummern verwenden
GPIO.setmode(GPIO.BOARD)

#GPIO Pins zuweisen
GPIO_INPUT = 17
GPIO_OUTPUT = 18

# Pin 11 als Input
GPIO.setup(GPIO_INPUT, GPIO.IN)
# Pin 12 als Output
GPIO.setup(GPIO_OUTPUT, GPIO.OUT)


if __name__ == '__main__':
    try:
        while True:
          # Solange Button nicht gedrueckt wird (False)
          if not GPIO.input(GPIO_INPUT):
            GPIO.output(GPIO_OUTPUT, True)
          # Wenn der Button gedrueckt wird
          else:
            GPIO.output(GPIO_OUTPUT, False)

        # Beim Abbruch durch STRG+C resetten
    except KeyboardInterrupt:
        print("Programm vom User gestoppt")
        GPIO.cleanup()