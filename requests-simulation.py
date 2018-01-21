import logging
from tkinter import *
import subprocess
from flask import Flask
from flask_ask import Ask, statement, question

app = Flask(__name__)
ask = Ask(app, "/")

log = logging.getLogger()
log.addHandler(logging.StreamHandler())
log.setLevel(logging.DEBUG)
logging.getLogger("flask_ask").setLevel(logging.DEBUG)

javaPipe = subprocess.Popen(["java", "data.Main"], stdin=subprocess.PIPE)	# opens java application

def getCorrectPhrase(Raum):
    to_return = ""

    if Raum == "wohnzimmer":
        to_return = "im Wohnzimmer"
    elif Raum == "küche":
        to_return = "in der Küche"
    elif Raum == "bad":
        to_return = "im Bad"
    elif Raum == "schlafzimmer":
        to_return = "im Schlafzimmer"
    elif Raum == "garage":
        to_return = "in der Garage"

    return to_return

@ask.launch
def launch():
    return statement("Willkommen zu der SmartHome Simulation der HTL Villach.")

@ask.intent("SayHello_Intent")
def say_hello(firstname):
    return statement("Hallo {}. Freut mich dich kennen zu lernen!".format(firstname))

@ask.intent("AllLEDsOn_Intent")
def allLeds_on():
    antwort = "Alle Lichter wurden eingeschaltet."

	#userSaid(request)
    #gui.alexa_said(antwort)
    javaPipe.stdin.write(bytes("TurnOnAll\n", "UTF-8"))
    javaPipe.stdin.flush()

    return statement(antwort)

@ask.intent("AllLEDsOff_Intent")
def allLeds_off():
    antwort = "Alle Lichter wurden ausgeschaltet."

	#userSaid(request)
    #gui.alexa_said(antwort)
    javaPipe.stdin.write(bytes("TurnOffAll\n", "UTF-8"))
    javaPipe.stdin.flush()

    return statement(antwort)

@ask.intent("TurnLEDXOn_Intent")
def led_x_on(Raum):
    antwort = "Ich habe das Licht {} eingeschaltet.".format(getCorrectPhrase(Raum))

    #userSaid(request)
    #gui.alexa_said(antwort)
    javaPipe.stdin.write(bytes("TurnOn:{}\n".format(Raum), "UTF-8"))
    javaPipe.stdin.flush()

    return statement(antwort)

@ask.intent("TurnLEDXOff_Intent") 
def led_x_off(Raum):
    antwort = "Ich habe das Licht {} ausgeschaltet.".format(getCorrectPhrase(Raum))

	#userSaid(request)
    #gui.alexa_said(antwort)
    javaPipe.stdin.write(bytes("TurnOff:{}\n".format(Raum), "UTF-8"))
    javaPipe.stdin.flush()

    return statement(antwort)

if __name__ == '__main__':
    app.run(debug=True)
