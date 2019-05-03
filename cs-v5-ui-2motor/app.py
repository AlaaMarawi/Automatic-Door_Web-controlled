from flask import Flask,render_template
import RPi.GPIO as GPIO
import time

app = Flask(__name__)
GPIO.setmode(GPIO.BCM)

numara=510

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
 
 
# Create a dictionary called pins to store the pin number, name, and pin state:
pins = {
   18 : {'name' : 'coffee maker', 'state' : GPIO.LOW},
   25 : {'name' : 'lamp', 'state' : GPIO.LOW}
   }

# Set each pin as an output and make it low:
for pin in pins:
   GPIO.setup(pin, GPIO.OUT)
   GPIO.output(pin, GPIO.LOW)


@app.route("/")
def main():
   # For each pin, read the pin state and store it in the pins dictionary:
   for pin in pins:
      pins[pin]['state'] = GPIO.input(pin)
   # Put the pin dictionary into the template data dictionary:
   templateData = {
      'pins' : pins,
      'durum' : 'kapı kapalı'
    }
   # Pass the template data into the template main.html and return it to the user
   return render_template('arayuz.html', **templateData)

@app.route("/opendoor")
def open():


    forward(int(3) / 1000.0, int(numara)) 
    templateData = {
        'durum' : 'kapı açık'
    }
    backwards(int(3) / 1000.0, int(numara))
    return render_template('arayuz.html', **templateData)


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
 




# The function below is executed when someone requests a URL with the pin number and action in it:
@app.route("/<changePin>/<action>")
def action(changePin, action):
   # Convert the pin from the URL into an integer:
   changePin = int(changePin)
   # Get the device name for the pin being changed:
   deviceName = pins[changePin]['name']
   # If the action part of the URL is "on," execute the code indented below:
   if action == "on":
      # Set the pin high:
      GPIO.output(changePin, GPIO.HIGH)
      # Save the status message to be passed into the template:
      message = "Turned " + deviceName + " on."
   if action == "off":
      GPIO.output(changePin, GPIO.LOW)
      message = "Turned " + deviceName + " off."
   if action == "toggle":
      # Read the pin and set it to whatever it isn't (that is, toggle it):
      GPIO.output(changePin, not GPIO.input(changePin))
      message = "Toggled " + deviceName + "."

   # For each pin, read the pin state and store it in the pins dictionary:
   for pin in pins:
      pins[pin]['state'] = GPIO.input(pin)

   # Along with the pin dictionary, put the message into the template data dictionary:
   templateData = {
      'message' : message,
      'pins' : pins
   }

   return render_template('pin.html', **templateData)

#for button:
@app.route("/readPin/<pin>")
def readPin(pin):
   try:
      GPIO.setup(int(pin), GPIO.IN, pull_up_down=GPIO.PUD_UP)
      if GPIO.input(int(pin)) == True:
         response = "Pin number " + pin + " is high!"
      else:
         response = "Pin number " + pin + " is low!"
   except:
      response = "There was an error reading pin " + pin + "."

   templateData = {
      'title' : 'Status of Pin' + pin,
      'response' : response
      }

   return render_template('pin.html', **templateData)


if __name__ == '__main__':
    app.run(debug=True, host='172.16.220.47')
