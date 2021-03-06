#Bibliotheken einbinden
import sys
sys.path += ['../util']
from Observer import Observer, Observable
import RPi.GPIO as GPIO
import time


class ObservedDistanceSensor:
	
	def measure(self):
    		# setze Trigger auf HIGH
    		GPIO.output(self.GPIO_TRIGGER, True)
 
    		# setze Trigger nach 0.01ms aus LOW
    		time.sleep(0.00001)
    		GPIO.output(self.GPIO_TRIGGER, False)
 
    		StartZeit = time.time()
    		StopZeit = time.time()
 
    		# speichere Startzeit
    		while GPIO.input(self.GPIO_ECHO) == 0:
        		StartZeit = time.time()
 
    		# speichere Ankunftszeit
    		while GPIO.input(self.GPIO_ECHO) == 1:
        		StopZeit = time.time()
 
    		# Zeit Differenz zwischen Start und Ankunft
    		TimeElapsed = StopZeit - StartZeit
    		# mit der Schallgeschwindigkeit (34300 cm/s) multiplizieren
    		# und durch 2 teilen, da hin und zurueck
    		distance = (TimeElapsed * 34300) / 2
 
    		return distance

	def close(self):
		self.running = 0
		GPIO.cleanup()
		
	def __init__(self,name,trigger,echo):
		self.name = name
		self.GPIO_TRIGGER = trigger
		self.GPIO_ECHO = echo
		GPIO.setmode(GPIO.BCM)
 		GPIO.setup(self.GPIO_TRIGGER, GPIO.OUT)
		GPIO.setup(self.GPIO_ECHO, GPIO.IN)
		self.running = 0
		self.openObserver = ObservedDistanceSensor.OpenObserver(self)
        self.closeObserver = ObservedDistanceSensor.CloseObserver(self)
        
		
	
	# An inner class for observing openings:
    class OpenObserver(Observer):
        def __init__(self, outer):
            self.outer = outer
            self.outer.running = 1
        def update(self, observable, arg):
        	try:
          		while self.outer.running==1:
		            dist = self.outer.measure()
		            print (self.outer.name + ": Gemessene Entfernung = %.1f cm" % dist)
		            time.sleep(1)
              
    # Another inner class for closings:
    class CloseObserver(Observer):
        def __init__(self, outer):
            self.outer = outer
        def update(self, observable, arg):
            print("Abstandsmessung '"+self.outer.name + "' wird abgeschaltet.")
        	self.outer.close()

