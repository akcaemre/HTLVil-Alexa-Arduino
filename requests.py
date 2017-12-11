import logging
import serial
from flask import Flask
from flask_ask import Ask, statement, question

myArduino = serial.Serial("/dev/ttyUSB0", 9600)
app = Flask(__name__)
ask = Ask(app, "/")

log = logging.getLogger()
log.addHandler(logging.StreamHandler())
log.setLevel(logging.DEBUG)
logging.getLogger("flask_ask").setLevel(logging.DEBUG)

@ask.launch
def launch():
	return statement("Welcome to the request demo")

@ask.intent("SayHelloIntent")
def say_hello(firstname):
	return statement("Hello {}. Nice to meet you.".format(firstname))

@ask.intent("LedOnIntent")
def led_on():
	myArduino.write(bytes('turnLedOn', 'UTF-8'))
	return statement("I turned the led on")

@ask.intent("LedOffIntent")
def led_off():
	myArduino.write(bytes('turnLedOff', 'UTF-8'))
	return statement("I turned the led off")

@ask.intent("LedDimmIntent")
def led_dimm():
	myArduino.write(bytes('Dimm', 'UTF-8'))
	return statement("I dimmed the led")

@ask.intent("LedBlinkIntent")
def led_blink():
	myArduino.write(bytes('blink', 'UTF-8'))
	return statement("Blink the led")

@ask.intent("LedBinaryIntent")
def led_binary(prime):
	myArduino.write(bytes('binary:'+str(prime), 'UTF-8'))
	return statement("I am showing the number " + str(prime) + " in binary")

@ask.intent("RGBChangeColorIntent")
def rgb_color(color):
	myArduino.write(bytes(color, 'UTF-8'))
	return statement("I am showing the color {}".format(bytes(color, 'UTF-8')))

if __name__ == '__main__':
	app.run(debug=True)
