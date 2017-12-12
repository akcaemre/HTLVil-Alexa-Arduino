import logging
import serial
from flask import Flask
from flask_ask import Ask, statement, question

myArduino = serial.Serial("/dev/ttyUSB0", 9600, timeout=1)
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
	myArduino.write(color.encode("UTF-8"))
	return statement("I am showing the color {}".format(color.encode("UTF-8").decode("UTF-8")))

@ask.intent("GetTemperatureIntent")
def get_temp():
	myArduino.write(bytes("measureTemperatureCelsius", "UTF-8"))
	s = myArduino.readline()
	return statement(s.decode("UTF-8"))

@ask.intent("RGBOffIntent")
def rgb_off():
	myArduino.write(bytes("rgboff", "UTF-8"))
	return statement("I turned the color off.")

@ask.intent("ResetPinsIntent")
def reset_pins():
	myArduino.write(bytes("reset", "UTF-8"))
	return statement("I turned the lights out.")

@ask.intent("TurnLedXOn")
def led_x(prime):
	myArduino.write(bytes("LEDON:" + str(prime), "UTF-8"))
	return statement("I turned led " + str(prime) + " on.")

@ask.intent("LedDimmAutoIntent")
def dimm_auto():
	myArduino.write(bytes("dimmauto", "UTF-8"))
	return statement("The lights are automatically dimmed")

if __name__ == '__main__':
	app.run(debug=True)
