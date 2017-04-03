'''
Created on 01.04.2017

@author: patrik
'''
import time

import sys
sys.path += ['../util/observer']
from Observer import Observer,Observable
#from observable import Observable

sys.path += ['../sensors/test']
from HCSR04 import HCSR04

#from thread import start_new_thread
from threading import Thread

class DistanceSensor(Observable):
    def __init__(self, name,trigger,echo,threshold):
        Observable.__init__(self)
        self.name = name
        self.hcsr04 = HCSR04(name,trigger,echo);
        self.running = True
        self.threshold = threshold
        #self.observable = Observable()
        
        print (self.name+": Sensor wird erzeugt.")
    
    def start(self):
        
        while self.running:
            dist = self.hcsr04.measure()
            if(dist<=self.threshold):
                self.update_observers(self.name,dist)
            time.sleep(1)
    #def register(self,observer):
    #    self.observable.register(observer)
    def stop(self):
        print(self.name+"Sensor wird gestoppt.")
        self.running=False
        self.hcsr04.close()
        
class SensorController(Observer):
    def update(self,*args,**kwargs):
        print(args[0]+": Gemessene Entfernung = %.1f cm." % args[1])


if __name__ == '__main__':
    try:
        
        sc = SensorController()
        rsens = DistanceSensor("RECHTS",19,26,50)
        lsens = DistanceSensor("LINKS",20,21,50)
        
        rsens.register(sc)
        lsens.register(sc)
        
        
        tl = Thread(target=lsens.start)
        tl.start()
        tr = Thread(target=rsens.start)
        tr.start()
        
        #start_new_thread(lsens.start())
        #start_new_thread(rsens.start())
       
         
        
 
        # Beim Abbruch durch STRG+C resetten
    except KeyboardInterrupt:
        print("SensorController wird beendet.")
        rsens.stop()
        lsens.stop()
        
      