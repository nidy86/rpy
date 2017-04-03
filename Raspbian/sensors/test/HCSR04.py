#Bibliotheken einbinden
from random import randint

class HCSR04:
	def __init__(self,name,trigger,echo):
		self.name = name
		

	def measure(self):
		#print("HCSR04: "+self.name+" Messung gestartet...")
		dist = randint(0,150) 
		return dist

	def close(self):
		print ("GPIO bereits geschlossen.")