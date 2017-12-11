#include <math.h>

String readSerialString;
byte dimmbrightness = 80;
boolean blink = false;

// LEDpins from left to right; RGBpins Red Green Blue
int LEDpins[] = {3, 5, 6, 7}, RGBpins[] = {11, 10, 9};
boolean turnOnTheLights[] = {false, false, false, false};
int i = 0;
int temperatureSensorPin = 0, photoresistorPin = 1;
int LEDCount = 4;

void setup() {
  Serial.begin(9600);
  
  // Initialize pins
  for (i = 0; i < 4; i++)
    pinMode(LEDpins[i], OUTPUT);

  for (i = 0; i < 3; i++)
    pinMode(RGBpins[i], OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    // Read the incoming String:
    readSerialString = Serial.readString();

    // Handle the readSerialString
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
      blink != blink;
    }
    else if(readSerialString == "reset"){
      turnLEDsOff();
      setColor(0, 0, 0);
      
      Serial.println("RESETED");
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
    else if(readSerialString.startsWith("binary")) {
      showBinary(getValue(readSerialString, ':',1).toInt());
    }
    else if(readSerialString.startsWith("LEDON")) {
      int ledOnNum = getValue(readSerialString,':', 1).toInt() - 1;

      if(ledOnNum >= 0 && ledOnNum < LEDCount) {
        turnLEDsFalse();
        
        turnOnTheLights[ledOnNum] = true;
        
        turnRightLEDsOn();
        
        Serial.print("LED ");
        Serial.print(ledOnNum+1);
        Serial.println(" turned ON");
      } 
    }
    else if(readSerialString == "measureTemperatureCelsius"){
      int val = analogRead(temperatureSensorPin);   
    
      // Tutorial from computers.tutsplus.com --> "How to Read Temperatures With Arduino"
      double temp = log(((10240000/val) - 10000));
      // Kelvin
      temp = 1 / (0.001129148 + (0.000234125 + (0.0000000876741 * temp * temp)) * temp);
      // Celsius
      temp = temp - 273.15;   
      
      Serial.print("The current temperature is ");
      Serial.print(temp);
      Serial.println(" celsius degrees.");    
    }
    else if(readSerialString == "measureTemperatureFahrenheit"){
      int val = analogRead(temperatureSensorPin);   
    
      // Tutorial from computers.tutsplus.com --> "How to Read Temperatures With Arduino"
      double temp = log(((10240000/val) - 10000));
      // Kelvin
      temp = 1 / (0.001129148 + (0.000234125 + (0.0000000876741 * temp * temp)) * temp);
      // Celsius
      temp = temp - 273.15;    
      // Fahrenheit
      temp = (temp * 9) / 5 + 32;
      
      Serial.print("The current temperature is ");
      Serial.print(temp);
      Serial.println(" fahrenheit.");    
    }
    else if(readSerialString == "dimmauto") {
      double val = analogRead(photoresistorPin);
      int per = (val / 1024) * 100;
      
      analogWrite(LEDpins[0], 1024 - val);    
      blink = false;
      
      if(per <= 25) {
        Serial.println("It is pretty dark. The room is brighter now");
      }
      else if(per <= 50) {
        Serial.println("The light is ok, but stil too dark. i will make some adjustments");
      }
      else if(per <= 75) {
        Serial.println("It is pretty bright. I'm dimming the lights.");
      }
      else {
        Serial.println("It is so bright! I'm turning off the lights.");
        digitalWrite(LEDpins[0], LOW);
      }
    }
  }
  if(blink){
    digitalWrite(LEDpins[0], HIGH);
    delay(1000);
    digitalWrite(LEDpins[0], LOW);
    delay(1000);
  }
}

void turnLEDsOff() {
      turnLEDsFalse();
      turnRightLEDsOn();
}
void turnLEDsFalse() {
  for(i = 0; i < LEDCount; i++)
    turnOnTheLights[i] = false;
}
void turnRightLEDsOn() {
  for(i = 0; i < LEDCount; i++)
    if(turnOnTheLights[i] == true)
      digitalWrite(LEDpins[i], HIGH);
    else
      digitalWrite(LEDpins[i], LOW);
}

void setColor(int red, int green, int blue)
{
  analogWrite(RGBpins[0], red);
  analogWrite(RGBpins[1], green);
  analogWrite(RGBpins[2], blue);  
}

String getValue(String data, char separator, int index) {
  int found = 0;
  int strIndex[] = {
    0, -1  };
  int maxIndex = data.length()-1;

  for (int i = 0; i <= maxIndex && found <= index; i++) {
    if(data.charAt(i)==separator || i == maxIndex) {
      found++;
      strIndex[0] = strIndex[1]+1;
      strIndex[1] = (i == maxIndex) ? i+1 : i; 
    }
  }

  return found > index ? data.substring(strIndex[0], strIndex[1]) : "";
}
void showBinary (int n) {
  int remainder;
  turnLEDsFalse();

  i = 0;
  while(n!=0) {
    remainder = n%2;

    Serial.print(remainder);
    if(remainder == 1) turnOnTheLights[i] = true;

    n /= 2;
    i++;
  }
  
  turnRightLEDsOn();
}

