import logging
import serial
from flask import Flask
from flask_ask import Ask, statement, question
from tkinter import *
import subprocess

# Initializing Arduino on USB0
myArduino = serial.Serial("/dev/ttyUSB0", 9600, timeout=10)

# Initializing App for Alexa
app = Flask(__name__)
ask = Ask(app, "/")

# Setting logger
log = logging.getLogger()
log.addHandler(logging.StreamHandler())
log.setLevel(logging.DEBUG)
logging.getLogger("flask_ask").setLevel(logging.DEBUG)

# Opening needed Java Applications
javaProtocolPipe = subprocess.Popen(["java", "data.ProtocolMonitorMain"], stdin=subprocess.PIPE)

# this function checks which led number equals which room
def checkLedNbr(ledNbr):
    to_return = ""

    if ledNbr == 1:
        to_return = "im Wohnzimmer"
    elif ledNbr == 2:
        to_return = "in der Küche"
    elif ledNbr == 3:
        to_return = "im Bad"
    elif ledNbr == 4:
        to_return = "im Schlafzimmer"
    elif ledNbr == 5:
        to_return = "in der Garage"

    return to_return

def SendTextViaProtocolPipe(userText, alexaText):
    javaProtocolPipe.stdin.write(bytes("{};{}".format(userText, alexaText), "UTF-8"))
    javaProtocolPipe.stdin.flush()
    return

def WriteSerialLineToArduino(text):
    myArduino.write(bytes(text, "UTF-8"))
    myArduino.flush()
    myArduino.readline()

    return

@ask.launch
def launch():
    antwort = "Willkommen zu dem Arduino kontrollierten SmartHome der HTL Villach."
    SendTextViaProtocolPipe("Benutzer: ...", "Alexa: {}".format(antwort))

    return statement(antwort)

@ask.intent("SayHello_Intent")
def say_hello(firstname):
    antwort = "Hallo {}. Freut mich dich kennen zu lernen.".format(firstname)
    SendTextViaProtocolPipe("Benutzer: ...", "Alexa: {}".format(antwort))

    return statement(antwort)


@ask.intent("AllLEDsOn_Intent")
def allLeds_on():
    WriteSerialLineToArduino("allLeds_on")

    antwort = "Alle Lichter wurden eingeschaltet."
    SendTextViaProtocolPipe("Benutzer: ...", "Alexa: {}".format(antwort))

    return statement(antwort)

@ask.intent("AllLEDsOff_Intent")
def allLeds_off():
    WriteSerialLineToArduino("allLeds_off")

    antwort = "Alle Lichter wurden ausgeschaltet."
    SendTextViaProtocolPipe("Benutzer: ...", "Alexa: {}".format(antwort))

    return statement(antwort)

@ask.intent("AutoLEDDimm_Intent")
def autoLedDimm(ledNbr):
    WriteSerialLineToArduino("autoLedDimm:" + str(ledNbr))

    antwort = "Ich habe das licht {} automatisch gedimmt.".format(checkLedNbr(ledNbr))
    SendTextViaProtocolPipe("Benutzer: ...", "Alexa: {}".format(antwort))

    return statement("antwort")

@ask.intent("LEDDimm_Intent")
def led_dimm(ledNbr):
    WriteSerialLineToArduino("led_dimm:" + str(ledNbr))

    antwort = "Ich habe das licht " + checkLedNbr(ledNbr) + " entsprechend der Helligkeit gedimmt."
    SendTextViaProtocolPipe("Benutzer: ...", "Alexa: {}".format(antwort))

    return statement(antwort)

@ask.intent("TurnLEDXOn_Intent")
def led_x_on(ledNbr):
    WriteSerialLineToArduino("LEDON:" + str(ledNbr))

    antwort = "Ich habe das Licht " + checkLedNbr(ledNbr) + " eingeschaltet."
    SendTextViaProtocolPipe("Benutzer: ...", "Alexa: {}".format(antwort))

    return statement(antwort)

@ask.intent("TurnLEDXOff_Intent") 
def led_x_off(ledNbr):
    WriteSerialLineToArduino("LEDOFF:" + str(ledNbr))

    antwort = "Ich habe das Licht " + checkLedNbr(ledNbr) + " ausgeschaltet."
    SendTextViaProtocolPipe("Benutzer: ...", "Alexa: {}".format(antwort))

    return statement(antwort)

@ask.intent("RGB_LEDSetColor_Intent")
def rgb_color(color):
    WriteSerialLineToArduino(color.encode("UTF-8"))

    antwort = "Wie gewünscht siehst du jetzt die Farbe {}".format(color.encode("UTF-8").decode("UTF-8"))
    SendTextViaProtocolPipe("Benutzer: ...", "Alexa: {}".format(antwort))

    return statement(antwort)

@ask.intent("RGB_LEDOff_Intent")
def rgb_off():
    WriteSerialLineToArduino("rgb_off")

    antwort = "Ich habe die Farb-LED ausgeschaltet."
    SendTextViaProtocolPipe("Benutzer: ...", "Alexa: {}".format(antwort))

    return statement(antwort)

@ask.intent("ResetAllLEDs_Intent")
def reset_all_leds():
    WriteSerialLineToArduino("reset_all_leds")

    antwort = "Ich habe sämtliche Lichter und Lampen ausgeschaltet."
    SendTextViaProtocolPipe("Benutzer: ...", "Alexa: {}".format(antwort))

    return statement(antwort)

@ask.intent("ShowInBinary_Intent")
def led_binary(numberToDisplay):
    WriteSerialLineToArduino('binary:' + str(numberToDisplay))

    antwort = "Ich zeige nun die Zahl " + str(numberToDisplay) + " mittels den LEDs als Binärzahl."
    SendTextViaProtocolPipe("Benutzer: ...", "Alexa: {}".format(antwort))

    return statement(antwort)

@ask.intent("MeasureTemperatureCelsius_Intent")
def get_temp_cel():
    myArduino.write(bytes("measureTemperatureCelsius", "UTF-8"))
    myArduino.flush()
    s = myArduino.readline()	# arduino tells what alexa has to say

    antwort = "Zurzeit hat es {} Grad Celsius".format(s.decode("UTF-8"))
    SendTextViaProtocolPipe("Benutzer: ...", "Alexa: {}".format(antwort))

    return statement(antwort)

@ask.intent("MeasureTemperatureFahrenheit_Intent")
def get_temp_fahr():
    myArduino.write(bytes("measureTemperatureFahrenheit", "UTF-8"))
    myArduino.flush()
    s = myArduino.readline()	# arduino tells what alexa has to say

    antwort = "Zurzeit hat es {} Fahrenheit".format(s.decode("UTF-8"))
    SendTextViaProtocolPipe("Benutzer: ...", "Alexa: {}".format(antwort))

    return statement(antwort)

@ask.intent("LetLEDsWave_Intent")
def let_leds_wave():
    WriteSerialLineToArduino("ledLedsWave")
    myArduino.readline()

    antwort = "Die LEDs zeigen jetzt wie gewünscht eine Welle."
    SendTextViaProtocolPipe("Benutzer: ...", "Alexa: {}".format(antwort))

    return statement(antwort)

@ask.intent("TestAllFunctions_Intent")
def test_all_functions():
    WriteSerialLineToArduino("testAllFunctions")

    antwort = "Alle Funktionen werden getestet."
    SendTextViaProtocolPipe("Benutzer: ...", "Alexa: {}".format(antwort))

    return statement(antwort)

if __name__ == '__main__':
    app.run(debug=True)
