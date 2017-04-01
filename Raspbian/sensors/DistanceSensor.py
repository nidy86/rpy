#Bibliotheken einbinden
import ../RPi.GPIO as GPIO
import time


class DistanceSensor:
	def __init__(self,name,trigger,echo):
		self.SENSOR_NAME = name
		#GPIO Pins zuweisen
		self.GPIO_TRIGGER = trigger
		self.GPIO_ECHO = echo
		self.doSetup()

	def doSetup(self):
		#GPIO Modus (BOARD / BCM)
		GPIO.setmode(GPIO.BCM)
 
		#Richtung der GPIO-Pins festlegen (IN / OUT)
		GPIO.setup(self.GPIO_TRIGGER, GPIO.OUT)
		GPIO.setup(self.GPIO_ECHO, GPIO.IN)
	
	def getName(self):
		return self.SENSOR_NAME 

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
		GPIO.cleanup()
 
if __name__ == '__main__':
    
    sensor = DistanceSensor("Front",20,21)
    try:
        while True:
            abstand = sensor.measure()
            print (sensor.getName(),": Gemessene Entfernung = %.1f cm" % abstand)
            time.sleep(1)
 
        # Beim Abbruch durch STRG+C resetten
    except KeyboardInterrupt:
        print("Messung vom User gestoppt")
        sensor.close()
