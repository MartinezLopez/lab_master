#!/usr/bin/python

#import Adafruit_BBIO.GPIO as gpio #BBB
import RPi.GPIO as gpio #RbP

class PinesFPGA:
  
  #pines = {'l1_ls': "P8_10",'l1_ms': "P8_8", 'r1_ls': "P8_14", 'r1_ms': "P8_12",'l2_ls': "P8_9",'l2_ms': "P8_7", 'r2_ls': "P8_13", 'r2_ms': "P8_11", 'sync_ls': "P8_18", 'sync_ms': "P8_16", 'rst': "P8_17"} #BBB
  pines = {'l1_ls': 12,'l1_ms': 11, 'r1_ls': 22, 'r1_ms': 21,'l2_ls': 16,'l2_ms': 15, 'r2_ls': 24, 'r2_ms': 23, 'sync_ls': 19, 'sync_ms': 18, 'rst': 13} #RbP
  
  def __init__(self):
    
    gpio.setmode(gpio.BOARD) #RbP
    
    for i in self.pines.keys():
      gpio.setup(self.pines[i], gpio.OUT)
      gpio.output(self.pines[i], gpio.LOW)
    self.reset(True)
  
  def setLength1(self, length):
    if length == 0:
      gpio.output(self.pines["l1_ms"], gpio.LOW)
      gpio.output(self.pines["l1_ls"], gpio.LOW)
    elif length == 1:
      gpio.output(self.pines["l1_ms"], gpio.LOW)
      gpio.output(self.pines["l1_ls"], gpio.HIGH)
    elif length == 2:
      gpio.output(self.pines["l1_ms"], gpio.HIGH)
      gpio.output(self.pines["l1_ls"], gpio.LOW)
    elif length == 3:
      gpio.output(self.pines["l1_ms"], gpio.HIGH)
      gpio.output(self.pines["l1_ls"], gpio.HIGH)
  
  def setRate1(self, rate):
    if rate == 0:
      gpio.output(self.pines["r1_ms"], gpio.LOW)
      gpio.output(self.pines["r1_ls"], gpio.LOW)
    elif rate == 1:
      gpio.output(self.pines["r1_ms"], gpio.LOW)
      gpio.output(self.pines["r1_ls"], gpio.HIGH)
    elif rate == 2:
      gpio.output(self.pines["r1_ms"], gpio.HIGH)
      gpio.output(self.pines["r1_ls"], gpio.LOW)
    elif rate == 3:
      gpio.output(self.pines["r1_ms"], gpio.HIGH)
      gpio.output(self.pines["r1_ls"], gpio.HIGH)
  
  def setLength2(self, length):
    if length == 0:
      gpio.output(self.pines["l2_ms"], gpio.LOW)
      gpio.output(self.pines["l2_ls"], gpio.LOW)
    elif length == 1:
      gpio.output(self.pines["l2_ms"], gpio.LOW)
      gpio.output(self.pines["l2_ls"], gpio.HIGH)
    elif length == 2:
      gpio.output(self.pines["l2_ms"], gpio.HIGH)
      gpio.output(self.pines["l2_ls"], gpio.LOW)
    elif length == 3:
      gpio.output(self.pines["l2_ms"], gpio.HIGH)
      gpio.output(self.pines["l2_ls"], gpio.HIGH)
  
  def setRate2(self, rate):
    if rate == 0:
      gpio.output(self.pines["r2_ms"], gpio.LOW)
      gpio.output(self.pines["r2_ls"], gpio.LOW)
    elif rate == 1:
      gpio.output(self.pines["r2_ms"], gpio.LOW)
      gpio.output(self.pines["r2_ls"], gpio.HIGH)
    elif rate == 2:
      gpio.output(self.pines["r2_ms"], gpio.HIGH)
      gpio.output(self.pines["r2_ls"], gpio.LOW)
    elif rate == 3:
      gpio.output(self.pines["r2_ms"], gpio.HIGH)
      gpio.output(self.pines["r2_ls"], gpio.HIGH)
  
  def setClock(self, clock):
    if clock == 1:
      gpio.output(self.pines["sync_ms"], gpio.LOW)
      gpio.output(self.pines["sync_ls"], gpio.LOW)
    if clock == 2:
      gpio.output(self.pines["sync_ms"], gpio.HIGH)
      gpio.output(self.pines["sync_ls"], gpio.LOW)
    if clock == 3: #SoF1
      gpio.output(self.pines["sync_ms"], gpio.LOW)
      gpio.output(self.pines["sync_ls"], gpio.HIGH)
    if clock == 4: #SoF2
      gpio.output(self.pines["sync_ms"], gpio.HIGH)
      gpio.output(self.pines["sync_ls"], gpio.HIGH)
  
  def reset(self, state):
    if state:
      gpio.output(self.pines["rst"], gpio.LOW)
      for i in range(100): # Perdemos tiempo
        a = i+1
      gpio.output(self.pines["rst"] , gpio.HIGH)
    else:
      gpio.output(self.pines["rst"], gpio.HIGH)
  
  def quitGPIO(self):
    gpio.cleanup()


'''
def main():
  pines = PinesFPGA()
  print("inicializado")
  #pines.reset(True)
  pines.setClock(1)
  pines.setRate(3)
  pines.setLength(3)
  #pines.quitGPIO()
  while True:
    a = 5
  print("fin")

if __name__ == '__main__':
  main()'''
