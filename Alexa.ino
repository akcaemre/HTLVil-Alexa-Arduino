String readSerialString;
byte dimmbrightness = 80;
const int pinOFLED = 3;
bool blink = false;
int LEDpins[] = {3};
int redPin = 11;
int greenPin = 9;
int bluePin = 10;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(pinOFLED, OUTPUT);
  pinMode(redPin, OUTPUT); 
  pinMode(greenPin, OUTPUT); 
  pinMode(bluePin, OUTPUT); 
  // set the data rate for the SoftwareSerial port
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available() > 0) {
    // read the incoming byte:
    readSerialString = Serial.readString();
    int splitIndex = readSerialString.indexOf(':');
    if(readSerialString == "turnLedOn"){
      digitalWrite(LEDpins[0], HIGH);
      Serial.println("LEDturnedOn");
      blink = false;
    }
    else if(readSerialString == "turnLedOff"){
      digitalWrite(LEDpins[0], LOW);
      Serial.println("LEDturnedOFF");
      blink = false;
    }
    else if(readSerialString == "dimm"){
      analogWrite(LEDpins[0],dimmbrightness);
      Serial.println("Dimmend");
      blink = false;
    }
    else if(readSerialString == "blink"){
      blink = true;
    }
    else if(readSerialString == "stopBlink"){
      blink = false;
    }
    else if(readSerialString == "reset"){
      int i = 0;
      for(i=0;i<(sizeof(LEDpins)/sizeof(int));i++){
        digitalWrite(LEDpins[i], LOW);
        Serial.println("RESETED");
      }
      setColor(0, 0, 0);
      
    }
    else if(readSerialString == "red"){
      setColor(255, 0, 0);
      Serial.println("red");
    }
    else if(readSerialString == "green"){
      setColor(0, 255, 0);
      Serial.println("green");
    }
    else if(readSerialString == "blue"){
      setColor(0, 0, 255);
      Serial.println("blue");
    }
    else if(readSerialString == "rgboff"){
      setColor(0, 0, 0);
      Serial.println("RGB Off");
    }
  }
  if(blink){
    digitalWrite(LEDpins[0], HIGH);
    delay(1000);
    digitalWrite(LEDpins[0], LOW);
    delay(1000);
  }
}

void setColor(int red, int green, int blue)
{
  analogWrite(redPin, red);
  analogWrite(greenPin, green);
  analogWrite(bluePin, blue);  
}
