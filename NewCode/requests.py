import logging
import serial
from flask import Flask
from flask_ask import Ask, statement, question

myArduino = serial.Serial("/dev/ttyUSB0", 9600, timeout=10)
app = Flask(__name__)
ask = Ask(app, "/")

log = logging.getLogger()
log.addHandler(logging.StreamHandler())
log.setLevel(logging.DEBUG)
logging.getLogger("flask_ask").setLevel(logging.DEBUG)

@ask.launch
def launch():
	return statement("Welcome to the arduino control.")

@ask.intent("SayHello_Intent")
def say_hello(firstname):
	return statement("Hello {}. Nice to meet you.".format(firstname))



@ask.intent("AllLEDsOn_Intent")
def allLeds_on():
	myArduino.write(bytes("allLeds_on", "UTF-8"))
	myArduino.flush()
	myArduino.readline()
	return statement("All LEDs are on now.")

@ask.intent("AllLEDsOff_Intent")
def allLeds_off():
	myArduino.write(bytes("allLeds_off", "UTF-8"))
	myArduino.flush()
	myArduino.readline()
	return statement("All LEDs are off now.")

@ask.intent("AutoLEDDimm_Intent")
def autoLedDimm(ledNbr):
	myArduino.write(bytes("autoLedDimm:"+str(ledNbr), "UTF-8"))
	myArduino.flush()
	myArduino.readline()
	return statement("I dimmed led " + str(ledNbr) + ".")

@ask.intent("LEDDimm_Intent")
def led_dimm(ledNbr):
	myArduino.write(bytes("led_dimm:"+str(ledNbr), "UTF-8"))
	myArduino.flush()
	myArduino.readline()
	return statement("I dimmed led " + str(ledNbr) + ".")

@ask.intent("TurnLedXOn_Intent")
def led_x_on(ledNbr):
	myArduino.write(bytes("LEDON:" + str(ledNbr), "UTF-8"))
	myArduino.flush()
	myArduino.readline()
	return statement("I turned led " + str(ledNbr) + " on.")

@ask.intent("TurnLEDXOff_Intent") 
def led_x_off(ledNbr):
	myArduino.write(bytes("LEDOFF:" + str(ledNbr), "UTF-8"))
	myArduino.flush()
	myArduino.readline()
	return statement("I turned led " + str(ledNbr) + " off.")

@ask.intent("RGB_LEDSetColor_Intent")
def rgb_color(color):
	myArduino.write(color.encode("UTF-8"))
	myArduino.flush()
	myArduino.readline()
	return statement("I am showing the color {}".format(color.encode("UTF-8").decode("UTF-8")))

@ask.intent("RGB_LEDOff_Intent")
def rgb_off():
	myArduino.write(bytes("rgb_off", "UTF-8"))
	myArduino.flush()
	myArduino.readline()
	return statement("I turned the RGB LED off.")

@ask.intent("ResetAllLEDs_Intent")
def reset_all_leds():
	myArduino.write(bytes("reset_all_leds", "UTF-8"))
	myArduino.flush()
	myArduino.readline()
	return statement("I turned the lights off.")

@ask.intent("ShowInBinary_Intent")
def led_binary(numberToDisplay):
	myArduino.write(bytes('binary:'+str(numberToDisplay), 'UTF-8'))
	myArduino.flush()
	myArduino.readline()
	return statement("I am showing the number " + str(prime) + " in binary")

@ask.intent("MeasureTemperatureCelsius_Intent")
def get_temp_cel():
	myArduino.write(bytes("measureTemperatureCelsius", "UTF-8"))
	myArduino.flush()
	s = myArduino.readline()
	return statement(s.decode("UTF-8"))

@ask.intent("MeasureTemperatureFahrenheit_Intent")
def get_temp_fahr():
	myArduino.write(bytes("measureTemperatureFahrenheit", "UTF-8"))
	myArduino.flush()
	s = myArduino.readline()
	return statement(s.decode("UTF-8"))

@ask.intent("LetLEDsWave_Intent")
def let_leds_wave():
	myArduino.write(bytes("ledLedsWave", "UTF-8"))
	myArduino.flush()
	myArduino.readline()
	return statement("The Leds are now waving.")

@ask.intent("TestAllFunctions_Intent")
def test_all_functions():
	myArduino.write(bytes("testAllFunctions", "UTF-8"))
	myArduino.flush()
	myArduino.readline()
	return statement("Everything is getting tested.")

if __name__ == '__main__':
	app.run(debug=True)
