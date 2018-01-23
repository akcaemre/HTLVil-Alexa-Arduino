import logging
from tkinter import *
import subprocess
from flask import Flask
from flask_ask import Ask, statement, question

# Initializing App for Alexa
app = Flask(__name__)
ask = Ask(app, "/")

# Setting logger
log = logging.getLogger()
log.addHandler(logging.StreamHandler())
log.setLevel(logging.DEBUG)
logging.getLogger("flask_ask").setLevel(logging.DEBUG)

# Opening needed Java Applications
JAVA_PIPE_HOUSE_SIMULATION = subprocess.Popen(["java", "data.Main"], stdin=subprocess.PIPE)
javaProtocolPipe = subprocess.Popen(["java", "data.ProtocolMonitorMain"], stdin=subprocess.PIPE)


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

def SendTextViaProtocolPipe(userText, alexaText):
    javaProtocolPipe.stdin.write(bytes("{};{}\n".format(userText, alexaText), "UTF-8"))
    javaProtocolPipe.stdin.flush()
    return

def SendTextViaHouseSimulationPipe(text):
    JAVA_PIPE_HOUSE_SIMULATION.stdin.write(bytes(text, "UTF-8"))
    JAVA_PIPE_HOUSE_SIMULATION.stdin.flush()
    return

@ask.launch
def launch():
    antwort = "Willkommen zu der SmartHome Simulation der HTL Villach."
    SendTextViaProtocolPipe("Benutzer: ...", "Alexa: {}".format(antwort))

    return statement(antwort)

@ask.intent("SayHello_Intent")
def say_hello(firstname):
    antwort = "Hallo {}. Freut mich dich kennen zu lernen!".format(firstname)
    SendTextViaProtocolPipe("Benutzer: ...", "Alexa: {}".format(antwort))

    return statement(antwort)

@ask.intent("AllLEDsOn_Intent")
def allLeds_on():
    antwort = "Alle Lichter wurden eingeschaltet."

    SendTextViaProtocolPipe("Benutzer: ...", "Alexa: {}".format(antwort))
    SendTextViaHouseSimulationPipe("TurnOnAll\n")

    return statement(antwort)

@ask.intent("AllLEDsOff_Intent")
def allLeds_off():
    antwort = "Alle Lichter wurden ausgeschaltet."

    SendTextViaProtocolPipe("Benutzer: ...", "Alexa: {}".format(antwort))
    SendTextViaHouseSimulationPipe("TurnOffAll\n")

    return statement(antwort)

@ask.intent("TurnLEDXOn_Intent")
def led_x_on(Raum):
    antwort = "Ich habe das Licht {} eingeschaltet.".format(getCorrectPhrase(Raum))

    SendTextViaProtocolPipe("Benutzer: ...", "Alexa: {}".format(antwort))
    SendTextViaHouseSimulationPipe("TurnOn:{}\n".format(Raum))

    return statement(antwort)

@ask.intent("TurnLEDXOff_Intent") 
def led_x_off(Raum):
    antwort = "Ich habe das Licht {} ausgeschaltet.".format(getCorrectPhrase(Raum))

    SendTextViaProtocolPipe("Benutzer: ...", "Alexa: {}".format(antwort))
    SendTextViaHouseSimulationPipe("TurnOff:{}\n".format(Raum))

    return statement(antwort)

if __name__ == '__main__':
    app.run(debug=True)
