import RPi.GPIO as GPIO
import time
 
GPIO.setmode(GPIO.BCM)
 
enable_pin = 18
coil_A_1_pin = 4
coil_A_2_pin = 17
coil_B_1_pin = 27
coil_B_2_pin = 22

enable_pin2 = 5
coil_A_1_pin2 = 6
coil_A_2_pin2 = 13
coil_B_1_pin2 = 19
coil_B_2_pin2 = 26
 
GPIO.setup(enable_pin, GPIO.OUT)
GPIO.setup(coil_A_1_pin, GPIO.OUT)
GPIO.setup(coil_A_2_pin, GPIO.OUT)
GPIO.setup(coil_B_1_pin, GPIO.OUT)
GPIO.setup(coil_B_2_pin, GPIO.OUT)
 
GPIO.setup(enable_pin2, GPIO.OUT)
GPIO.setup(coil_A_1_pin2, GPIO.OUT)
GPIO.setup(coil_A_2_pin2, GPIO.OUT)
GPIO.setup(coil_B_1_pin2, GPIO.OUT)
GPIO.setup(coil_B_2_pin2, GPIO.OUT)
 
GPIO.output(enable_pin, 1)

GPIO.output(enable_pin2, 1)
 
def forward(delay, steps):  
  for i in range(0, steps):
    setStep(0, 0, 0, 1, 1, 0, 0, 0)
    time.sleep(delay)
    setStep(0, 0, 1, 0, 0, 1, 0, 0)
    time.sleep(delay)
    setStep(0, 1, 0, 0, 0, 0, 1, 0)
    time.sleep(delay)
    setStep(1, 0, 0, 0, 0, 0, 0, 1)
    time.sleep(delay)
 
def backwards(delay, steps):  
  for i in range(0, steps):
    setStep(1, 0, 0, 0, 0, 0, 0, 1)
    time.sleep(delay)
    setStep(0, 1, 0, 0, 0, 0, 1, 0)
    time.sleep(delay)
    setStep(0, 0, 1, 0, 0, 1, 0, 0)
    time.sleep(delay)
    setStep(0, 0, 0, 1, 1, 0, 0, 0)
    time.sleep(delay)
 
  
def setStep(w1, w2, w3, w4, w5, w6, w7, w8):
  GPIO.output(coil_A_1_pin, w1)
  GPIO.output(coil_A_2_pin, w2)
  GPIO.output(coil_B_1_pin, w3)
  GPIO.output(coil_B_2_pin, w4)
  GPIO.output(coil_A_1_pin2, w5)
  GPIO.output(coil_A_2_pin2, w6)
  GPIO.output(coil_B_1_pin2, w7)
  GPIO.output(coil_B_2_pin2, w8)
 
try:
    i=0
    while i<1:
      steps = input("Ileri kac adim? ")
      forward(int(5) / 1000.0, int(steps))
      steps = input("Geri kac adim? ")
      backwards(int(5) / 1000.0, int(steps))
      i=i+1
      print("bitti")
      
except:
    GPIO.cleanup()
    print("temizledi")
