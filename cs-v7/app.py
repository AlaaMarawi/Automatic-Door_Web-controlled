from flask import Flask,render_template
import RPi.GPIO as GPIO
import time

app = Flask(__name__)
GPIO.setmode(GPIO.BCM)

password = "123"
counter = "0"

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
 
GPIO.setup(18, GPIO.OUT)
GPIO.output(18, GPIO.LOW)

@app.route("/user")
def main():
   # Put the pin dictionary into the template data dictionary:
   templateData = {
      'password' : password
    }
   # Pass the template data into the template main.html and return it to the user
   return render_template('keypad.html', **templateData)

@app.route("/yonetici")
def main2():
    try:
        GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        if GPIO.input(18) == True:
            BellStat = 0
        else:
            BellStat = 1
    except:
        BellStat = -1

    templateData = {
        'BellStat':BellStat,
        'Stat' : 'closed',
        'counter' : counter
    }
   # Pass the template data into the template main.html and return it to the user
    return render_template('yonetim.html', **templateData)

@app.route("/opendooruser")
def openuser():
    global counter
    counter = int(counter) + 1
    forward(int(3) / 1000.0, int(200)) 
    templateData = {
        'password' : password
    }
    backwards(int(3) / 1000.0, int(200))

    return render_template('keypad.html', **templateData)

@app.route("/opendoor")
def open():
    global counter
    counter = int(counter) + 1
    forward(int(3) / 1000.0, int(200)) 
    templateData = {
        'Stat' : 'closed',
        'counter' : counter
    }
    backwards(int(3) / 1000.0, int(200))

    return render_template('yonetim.html', **templateData)

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
 



if __name__ == '__main__':
    app.run(debug=True, host='172.16.155.50')
