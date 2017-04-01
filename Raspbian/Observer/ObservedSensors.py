'''
Created on 01.04.2017

@author: patrik
'''
import time
import sys
sys.path += ['../util']
from Observer import Observer, Observable
sys.path += ['../sensors']
from HCSR04 import HCSR04

class SensorObserver:
    def __init__(self):
        self.isOpen = 0
        self.openNotifier = SensorObserver.OpenNotifier(self)
        self.closeNotifier= SensorObserver.CloseNotifier(self)
    def open(self): # Opens its petals
        self.isOpen = 1
        self.openNotifier.notifyObservers()
        self.closeNotifier.open()
    def close(self): # Closes its petals
        self.isOpen = 0
        self.closeNotifier.notifyObservers()
        self.openNotifier.close()
    def closing(self): return self.closeNotifier
    def signalIn(self,name,value):
        print
    
    class OpenNotifier(Observable):
        def __init__(self, outer):
            Observable.__init__(self)
            self.outer = outer
            self.alreadyOpen = 0
        def notifyObservers(self):
            if self.outer.isOpen and \
            not self.alreadyOpen:
                self.setChanged()
                Observable.notifyObservers(self)
                self.alreadyOpen = 1
        def close(self):
            self.alreadyOpen = 0

    class CloseNotifier(Observable):
        def __init__(self, outer):
            Observable.__init__(self)
            self.outer = outer
            self.alreadyClosed = 0
        def notifyObservers(self):
            if not self.outer.isOpen and \
            not self.alreadyClosed:
                self.setChanged()
                Observable.notifyObservers(self)
                self.alreadyClosed = 1
        def open(self):
            self.alreadyClosed = 0
            
class DistanceSensor:
    def __init__(self, name,trigger,echo):
        self.name = name
        self.hcsr04 = HCSR04(name,trigger,echo);
        self.running = True
        self.openObserver = DistanceSensor.OpenObserver(self)
        self.closeObserver = DistanceSensor.CloseObserver(self)
    # An inner class for observing openings:
    class OpenObserver(Observer):
        def __init__(self, outer):
            self.outer = outer
            print("HC-SR05 Sensor '" + self.outer.name + "' wird gestartet.")
        def update(self, observable, arg):
            while self.outer.running:
                dist = self.outer.hcsr04.measure()
                #print (self.outer.name + ": Gemessene Entfernung = %.1f cm" % dist)
                if dist<40:
                    observable.signalIn(self.outer.name,dist)
                time.sleep(1)
            
                
    # Another inner class for closings:
    class CloseObserver(Observer):
        def __init__(self, outer):
            self.outer = outer
        def update(self, observable, arg):
            print("Abstandsmessung '"+self.outer.name + "' wird abgeschaltet.")
            self.outer.running = False
            self.outer.hcsr04.close()            
            
if __name__ == '__main__':
    try:
        
        so = SensorObserver()
        lsens = DistanceSensor("LINKS",20,21)
        rsens = DistanceSensor("RECHTS",19,26)
        
        so.openNotifier.addObserver(lsens.openObserver)
        so.openNotifier.addObserver(rsens.openObserver)
        so.closeNotifier.addObserver(lsens.closeObserver)
        so.closeNotifier.addObserver(rsens.closeObserver)
        
        so.open()
        
        while True:
            time.sleep(1)
 
        # Beim Abbruch durch STRG+C resetten
    except KeyboardInterrupt:
        print("Sensorzentrale wird beendet")
        so.close()
       