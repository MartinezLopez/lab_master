import Adafruit_BBIO.GPIO as gpio

class PinesFPGA:
  
  def __init__(self):
    pines = ["P8_8","P8_10","P8_12","P8_14","P8_16", "P8_18"]
    for i in pines:
      gpio.setup(i, gpio.OUT)
      gpio.output(i, gpio.LOW)
    self.reset(True)
  
  def setLength1(self, length):
    
    if length == 0:
      gpio.output("P8_8", gpio.LOW)
      gpio.output("P8_10", gpio.LOW)
    elif length == 1:
      gpio.output("P8_8", gpio.LOW)
      gpio.output("P8_10", gpio.HIGH)
    elif length == 2:
      gpio.output("P8_8", gpio.HIGH)
      gpio.output("P8_10", gpio.LOW)
    elif length == 3:
      gpio.output("P8_8", gpio.HIGH)
      gpio.output("P8_10", gpio.HIGH)
  
  def setRate1(self, rate):
    
    if rate == 0:
      gpio.output("P8_12", gpio.LOW)
      gpio.output("P8_14", gpio.LOW)
    elif rate == 1:
      gpio.output("P8_12", gpio.LOW)
      gpio.output("P8_14", gpio.HIGH)
    elif rate == 2:
      gpio.output("P8_12", gpio.HIGH)
      gpio.output("P8_14", gpio.LOW)
    elif rate == 3:
      gpio.output("P8_12", gpio.HIGH)
      gpio.output("P8_14", gpio.HIGH)
  
  def setLength2(self, length):
    
    if length == 0:
      gpio.output("P8_39", gpio.LOW)
      gpio.output("P8_41", gpio.LOW)
    elif length == 1:
      gpio.output("P8_39", gpio.LOW)
      gpio.output("P8_41", gpio.HIGH)
    elif length == 2:
      gpio.output("P8_39", gpio.HIGH)
      gpio.output("P8_41", gpio.LOW)
    elif length == 3:
      gpio.output("P8_39", gpio.HIGH)
      gpio.output("P8_41", gpio.HIGH)
  
  def setRate2(self, rate):
    
    if rate == 0:
      gpio.output("P8_40", gpio.LOW)
      gpio.output("P8_42", gpio.LOW)
    elif rate == 1:
      gpio.output("P8_40", gpio.LOW)
      gpio.output("P8_42", gpio.HIGH)
    elif rate == 2:
      gpio.output("P8_40", gpio.HIGH)
      gpio.output("P8_42", gpio.LOW)
    elif rate == 3:
      gpio.output("P8_40", gpio.HIGH)
      gpio.output("P8_42", gpio.HIGH)
  
  def setClock(self, clock):
    
    if clock == 0:
      gpio.output("P8_16", gpio.LOW)
    if clock == 1:
      gpio.output("P8_16", gpio.HIGH)
  
  def reset(self, state):
    
    if state:
      gpio.output("P8_18", gpio.LOW)
      for i in range(100): # Perdemos tiempo
        a = i+1
      gpio.output("P8_18" , gpio.HIGH)
    else:
      gpio.output("P8_18" , gpio.HIGH)
  
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
