import logging
import serial
from flask import Flask
from flask_ask import Ask, statement, question
from tkinter import *
import subprocess

myArduino = serial.Serial("/dev/ttyUSB0", 9600, timeout=10)
app = Flask(__name__)
ask = Ask(app, "/")

log = logging.getLogger()
log.addHandler(logging.StreamHandler())
log.setLevel(logging.DEBUG)
logging.getLogger("flask_ask").setLevel(logging.DEBUG)

# PROTOCOL GUI VARIABLES
alexaScreen = Tk() # Fenster erstellen
alexaScreen.wm_title("Raspberry Pi GUI") # Fenster Titel
alexaScreen.config(background = "#FEFEFE") # Hintergrundfarbe des Fensters
lab = Label(alexaScreen)
lab.pack()

javaPipe = subprocess.Popen(["java", "data.main"], stdin=subprocess.PIPE)	# opens java application

# displays what alexa said on the protocol screen
def alexaSaid(sentence):
    lab.set("Alexa:\t" + sentence)
    alexaScreen.update_idletasks()
    return
# displays what the user said on the protocol screen
def userSaid(sentence):
    lab.set("User:\t" + sentence)
    alexaScreen.update_idletasks()
    return

alexaScreen.mainloop() # GUI wird upgedated. Danach keine Elemente setzen


# this function checks which led number equals which room
def checkLedNbr(ledNbr):
	location = "error"
	if ledNbr == 0
		location = "in der Küche"
	else if ledNbr == 1
		location = "in der Garage"
	else if ledNbr == 2
		location = "im Badezimmer"
	else if ledNbr == 3
		location = "im Wohnzimmer"
	else if ledNbr == 4
		location = "im Schlafzimmer"
	return location

def getRoomName(ledNbr):
	location = "error"
	if ledNbr == 0
		location = "Küche"
	else if ledNbr == 1
		location = "Garage"
	else if ledNbr == 2
		location = "Bad"
	else if ledNbr == 3
		location = "Wohnzimmer"
	else if ledNbr == 4
		location = "Schlafzimmer"
	return location

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
	antwort = "Alle Lichter wurden eingeschaltet."
	alexaSaid(antwort)
	javaPipe.stdin.write("TurnOnAll\r\n")
	return statement(antwort)

@ask.intent("AllLEDsOff_Intent")
def allLeds_off():
	myArduino.write(bytes("allLeds_off", "UTF-8"))
	myArduino.flush()
	myArduino.readline()
	antwort = "Alle Lichter wurden ausgeschaltet."
	alexaSaid(antwort)
	javaPipe.stdin.write("TurnOffAll\r\n")
	return statement(antwort)

@ask.intent("AutoLEDDimm_Intent")
def autoLedDimm(ledNbr):
	myArduino.write(bytes("autoLedDimm:"+str(ledNbr), "UTF-8"))
	myArduino.flush()
	myArduino.readline()

	antwort = "Ich habe das licht " + checkLedNbr(ledNbr) + " automatisch gedimmt."
	alexaSaid(antwort)
	return statement(antwort)

@ask.intent("LEDDimm_Intent")
def led_dimm(ledNbr):
	myArduino.write(bytes("led_dimm:"+str(ledNbr), "UTF-8"))
	myArduino.flush()
	myArduino.readline()

	antwort = "Ich habe das licht " + checkLedNbr(ledNbr) + " entsprechend der Helligkeit gedimmt."
	alexaSaid(antwort)
	return statement(antwort)

@ask.intent("TurnLedXOn_Intent")
def led_x_on(ledNbr):
	myArduino.write(bytes("LEDON:" + str(ledNbr), "UTF-8"))
	myArduino.flush()
	myArduino.readline()

	antwort = "Ich habe das Licht " + checkLedNbr(ledNbr) + " eingeschaltet."
	alexaSaid(antwort)
	javaPipe.stdin.write("TurnOn" + getRoomName(ledNbr) + "\r\n")
	return statement(antwort)

@ask.intent("TurnLEDXOff_Intent") 
def led_x_off(ledNbr):
	myArduino.write(bytes("LEDOFF:" + str(ledNbr), "UTF-8"))
	myArduino.flush()
	myArduino.readline()

	antwort = "Ich habe das Licht " + checkLedNbr(ledNbr) + " ausgeschaltet."
	alexaSaid(antwort)
	javaPipe.stdin.write("TurnOff" + getRoomName(ledNbr) + "\r\n")
	return statement(antwort)

@ask.intent("RGB_LEDSetColor_Intent")
def rgb_color(color):
	myArduino.write(color.encode("UTF-8"))
	myArduino.flush()
	myArduino.readline()

	antwort = "Wie gewünscht siehst du jetzt die Farbe {}".format(color.encode("UTF-8").decode("UTF-8"))
	alexaSaid(antwort)
	return statement(antwort)

@ask.intent("RGB_LEDOff_Intent")
def rgb_off():
	myArduino.write(bytes("rgb_off", "UTF-8"))
	myArduino.flush()
	myArduino.readline()

	antwort = "Ich habe die Farb-LED ausgeschaltet."
	alexaSaid(antwort)
	return statement(antwort)

@ask.intent("ResetAllLEDs_Intent")
def reset_all_leds():
	myArduino.write(bytes("reset_all_leds", "UTF-8"))
	myArduino.flush()
	myArduino.readline()

	antwort = "Ich habe sämtliche Lichter und Lampen ausgeschaltet."
	alexaSaid(antwort)
	return statement(antwort)

@ask.intent("ShowInBinary_Intent")
def led_binary(numberToDisplay):
	myArduino.write(bytes('binary:'+str(numberToDisplay), 'UTF-8'))
	myArduino.flush()
	myArduino.readline()

	antwort = "Ich zeige nun die Zahl " + str(prime) + " mittels den LEDs als Binärzahl."
	alexaSaid(antwort)
	return statement(antwort)

@ask.intent("MeasureTemperatureCelsius_Intent")
def get_temp_cel():
	myArduino.write(bytes("measureTemperatureCelsius", "UTF-8"))
	myArduino.flush()
	s = myArduino.readline()	# arduino tells what alexa has to say
	alexaSaid(s.decode("UTF-8"))
	return statement(s.decode("UTF-8"))

@ask.intent("MeasureTemperatureFahrenheit_Intent")
def get_temp_fahr():
	myArduino.write(bytes("measureTemperatureFahrenheit", "UTF-8"))
	myArduino.flush()
	s = myArduino.readline()	# arduino tells what alexa has to say
	alexaSaid(s.decode("UTF-8"))
	return statement(s.decode("UTF-8"))

@ask.intent("LetLEDsWave_Intent")
def let_leds_wave():
	myArduino.write(bytes("ledLedsWave", "UTF-8"))
	myArduino.flush()
	myArduino.readline()

	antwort = "Die LEDs zeigen jetzt wie gewünscht eine Welle."
	alexaSaid(antwort)
	return statement(antwort)

@ask.intent("TestAllFunctions_Intent")
def test_all_functions():
	myArduino.write(bytes("testAllFunctions", "UTF-8"))
	myArduino.flush()
	myArduino.readline()

	antwort = "Everything is getting tested."
	alexaSaid(antwort)
	return statement(antwort)

if __name__ == '__main__':
	app.run(debug=True)
