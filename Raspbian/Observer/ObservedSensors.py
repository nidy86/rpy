'''
Created on 01.04.2017

@author: patrik
'''
import time
import sys
sys.path += ['../util']
from Observer import Observer, Observable
sys.path += ['../sensors']
from ObservedDistanceSensor import ObservedDistanceSensor

class SensorObserver:
    def __init__(self):
        self.isOpen = 0
        self.openNotifier = Flower.OpenNotifier(self)
        self.closeNotifier= Flower.CloseNotifier(self)
    def open(self): # Opens its petals
        self.isOpen = 1
        self.openNotifier.notifyObservers()
        self.closeNotifier.open()
    def close(self): # Closes its petals
        self.isOpen = 0
        self.closeNotifier.notifyObservers()
        self.openNotifier.close()
    def closing(self): return self.closeNotifier
    
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
            
            
            
if __name__ == '__main__':
    try:
        
        so = SensorObserver()
        lsens = ObservedDistanceSensor("LINKS",20,21)
        rsens = ObservedDistanceSensor("RECHTS",19,26)
        
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
       