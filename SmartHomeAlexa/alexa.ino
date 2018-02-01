#include <math.h>
#include <dht.h>

dht DHT;
int DHT11_PIN  = 8;       // the pin where you get the measuered humidity values back

String readSerialString;
byte dimmbrightness = 80;  // percentage of how bright the led should be dimmed
int MAX_WAVE_ROUNDS = 10;  // defines how often the led wave should appear
int led_Count = 4;         // specifies how much default leds can be used


// LEDpins from left to right; RGBpins Red Green Blue
int LEDpins[] = {3, 5, 6, 7}, RGBpins[] = {11, 10, 9};
boolean turnOnTheLights[] = {false, false, false, false};
int temperatureSensorPin = 0, photoresistorPin = 1;

// all the setup stuff is done in this function
void setup() {
  Serial.begin(9600);
  int i = 0;
  
  // Initialize pins by setting the pinmode to output
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
    if(readSerialString == "allLeds_on"){              // turn all leds on
      turnAllLedsOn();
      Serial.println("AllLEDsturnedOn");
    }
    else if(readSerialString == "allLeds_off"){          // turn all leds off
      turnAllLedsOff();
      Serial.println("AllLEDsturnedOff");
    }
    else if(readSerialString.startsWith("autoLedDimm")){    // auto dimm led by number
      int nbr = getValue(readSerialString, ':',1).toInt();
      dimmLedDependingOnBrightness(nbr-1);
      Serial.print("LED ");
      Serial.print(nbr);
      Serial.println(" automatically dimmed.");
    }
    else if(readSerialString == "led_dimm"){          // dimm led by number
      int nbr = getValue(readSerialString, ':',1).toInt();
      dimmLed(nbr-1);
      Serial.print("LED ");
      Serial.print(nbr);
      Serial.println(" dimmed to 80%");
    }
    else if(readSerialString.startsWith("LEDON")){     // turn led on by number
      int nbr = getValue(readSerialString, ':',1).toInt();
      turnLedOn(nbr-1);
      Serial.print("LED ");
      Serial.print(nbr);
      Serial.println(" is now turned on.");
    }
    else if(readSerialString.startsWith("LEDOFF")){    //turn led off by number
      int nbr = getValue(readSerialString, ':',1).toInt();
      turnLedOff(nbr-1);
      Serial.print("LED ");
      Serial.print(nbr);
      Serial.println(" is now turned off.");
    }
    // provisorische, aber keine dauerhafte loesung der Farbueberpruefung
    else if(readSerialString == "red"){          // change rgb led color to red
      setColorLedRed();
      Serial.println("The RGB LED is now red.");
    }
    // provisorische, aber keine dauerhafte loesung der Farbueberpruefung
    else if(readSerialString == "green"){        // change rgb led color to green
      setColorLedGreen();
      Serial.println("The RGB LED is now green.");
    }
    // provisorische, aber keine dauerhafte loesung der Farbueberpruefung
    else if(readSerialString == "blue"){        // change rgb led color to blue
      setColorLedBlue();
      Serial.println("The RGB LED is now blue.");
    }
    else if(readSerialString == "rgb_off"){      // turn rgb led off
      setColorLedOff();
      Serial.println("The RGB LED is now turned off.");
    }
    else if(readSerialString == "reset_all_leds"){      // reset/turn off ALL leds
      resetAllLeds();
      Serial.println("All LEDs are now turned off.");
    }
    else if(readSerialString.startsWith("binary")) {      // displays a number in binary using the default LEDs
      int nbrToDisplay = getValue(readSerialString, ':',1).toInt();
      Serial.print("The number ");
      Serial.print(nbrToDisplay);
      Serial.println(" is now shown in binary mode.");
      showBinary(nbrToDisplay);
    }
    else if(readSerialString == "measureTemperatureCelsius"){
      measureDegreesInCelsius();
    }
    else if(readSerialString == "measureTemperatureFahrenheit"){
      measureDegreesInFahrenheit();
    }
    else if(readSerialString == "ledLedsWave") {
      letDefaultLedsWave(true);
      Serial.println("You just saw a few rounds of waving leds.");
    }
    else if(readSerialString == "testAllFunctions") {
      testAllFunctions(); 
      Serial.println("All Functions have been tested.");
    }
    else if(readSerialString == "measureHumidity") {
      measureHumidity();
    }
  }
}








/////////////////// main functions - getting called in loop()
// this function turns the led specified by the paramters on
void turnLedOn(int nbr) {
  digitalWrite(LEDpins[nbr], HIGH);
}
// this function turns the led specified by the paramters off
void turnLedOff(int nbr) {
  digitalWrite(LEDpins[nbr], LOW);
}
// this function turns all default leds on
void turnAllLedsOn() {
  for(int i = 0; i < led_Count; i++) {
     digitalWrite(LEDpins[i], HIGH);
  } 
}
// this function turns all default leds off
void turnAllLedsOff() {
  for(int i = 0; i < led_Count; i++) {
     digitalWrite(LEDpins[i], LOW);
  } 
}
//this function dimms a led, specified by the parameters
void dimmLed(int nbr) {
      analogWrite(LEDpins[nbr], dimmbrightness);
}
// this function resets all leds
void resetAllLeds() {
      turnAllLedsOff();
      setColorLedOff();
}



// the following functions are changing the color of the rgb led
void setColorLedRed(){
      setRGBColor(255, 0, 0);
}
void setColorLedGreen(){
      setRGBColor(0, 255, 0);
}
void setColorLedBlue(){
      setRGBColor(0, 0, 255);
}

// this function switches the rgb led off
void setColorLedOff(){
      setRGBColor(0, 0, 0);
}



// this function measures the temperature in celsius
void measureDegreesInCelsius() {
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
// this function measures the temperature in fahrenheit
void measureDegreesInFahrenheit() {
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

void measureHumidity() {
       int chk = DHT.read11(DHT11_PIN);
       //Serial.print("Temperature = ");
       //Serial.print(DHT.temperature);
       Serial.print("The humidity is ");
       Serial.print(DHT.humidity);
       Serial.println(" percent.");
}

// this function dimms the brightness of the first led (right one) depending on how dark it is
void dimmLedDependingOnBrightness(int ledToDimm) {
      double val = analogRead(photoresistorPin);
      int per = (val / 1024) * 100;
      
      analogWrite(LEDpins[ledToDimm], 1024 - val);
      
      if(per <= 25) {
        Serial.println("It is pretty dark. The room is brighter now");
      }
      else if(per <= 50) {
        Serial.println("The light is ok, but stil too dark. i will make some adjustments");
      }
      else if(per <= 90) {
        Serial.println("It is pretty bright. I'm dimming the lights.");
      }
      else {
        Serial.println("It is so bright! I'm turning off the lights.");
        digitalWrite(LEDpins[ledToDimm], LOW);
      }
}


// this function shows a binary number using the default leds
void showBinary (int n) {
  int remainder;
  turnLEDsFalse();

  int i = 0;
  while(n!=0) {
    remainder = n%2;

    Serial.print(remainder);
    if(remainder == 1) turnOnTheLights[i] = true;

    n /= 2;
    i++;
  }
  
  turnRightLEDsOn();
}

void turnRightLEDsOn() {
  for(int i = 0; i < led_Count; i++)
    if(turnOnTheLights[i] == true)
      digitalWrite(LEDpins[i], HIGH);
    else
      digitalWrite(LEDpins[i], LOW);
}

void turnLEDsFalse() {
  for(int i = 0; i < led_Count; i++)
    turnOnTheLights[i] = false;
}

// this function creates a smooth wave using the default leds
void letDefaultLedsWave(boolean fade) {
  if(!fade) {
    for(int i = 0; i < MAX_WAVE_ROUNDS; i++) {
      resetAllLeds();
      turnLedOn(0);
      delay(1000);
      turnLedOn(1);
      delay(1000);
      resetAllLeds();
      turnLedOn(1);
      turnLedOn(2);
      delay(1000);
      resetAllLeds();
      turnLedOn(2);
      turnLedOn(3);
      delay(1000);
      resetAllLeds();
      turnLedOn(3);
      delay(1000);
      resetAllLeds();
    }
  }
  else {
   for(int i = 0; i < MAX_WAVE_ROUNDS; i++) {
      resetAllLeds();
      analogWrite(LEDpins[0], 255);
      delay(100);
      analogWrite(LEDpins[0], 128);
      analogWrite(LEDpins[1], 255);
      delay(100);
      analogWrite(LEDpins[0], 64);
      analogWrite(LEDpins[1], 128);
      analogWrite(LEDpins[2], 255);
      delay(100);
      analogWrite(LEDpins[0], 32);
      analogWrite(LEDpins[1], 64);
      analogWrite(LEDpins[2], 128);
      analogWrite(LEDpins[3], 255);
      delay(100);
      analogWrite(LEDpins[0], 64);
      analogWrite(LEDpins[1], 128);
      analogWrite(LEDpins[2], 255);
      analogWrite(LEDpins[3], 128);
      delay(100);
      analogWrite(LEDpins[0], 128);
      analogWrite(LEDpins[1], 255);
      analogWrite(LEDpins[2], 128);
      analogWrite(LEDpins[3], 64);
      delay(100);
      analogWrite(LEDpins[0], 255);
      analogWrite(LEDpins[1], 128);
      analogWrite(LEDpins[2], 64);
      analogWrite(LEDpins[3], 32);
      delay(100);
      analogWrite(LEDpins[0], 128);
      analogWrite(LEDpins[1], 64);
      analogWrite(LEDpins[2], 32);
      analogWrite(LEDpins[3], 0);
      delay(100);
      analogWrite(LEDpins[0], 64);
      analogWrite(LEDpins[1], 32);
      analogWrite(LEDpins[2], 0);
      delay(100);
      resetAllLeds();
    }
  }
}



// this function tests all the other functions
void testAllFunctions() {
  // reset vor dem starten einer neuen funktion
  resetAllLeds();
  // countdown in binär
  showBinary(3);
  delay(1000);
  showBinary(2);
  delay(1000);
  showBinary(1);
  delay(1000);
  // reset vor dem starten einer neuen funktion
  resetAllLeds();
  // rgb led testen
  for(int i = 0; i < 3; i++) {
    setColorLedRed();
    delay(300);
    setColorLedOff();
    delay(100);
    setColorLedGreen();
    delay(300);
    setColorLedOff();
    delay(100);
    setColorLedBlue();
    delay(300);
    setColorLedOff();
    delay(100);
  }
  // reset vor dem starten einer neuen funktion
  resetAllLeds();
  // temperatursensor testen
  measureDegreesInCelsius();
  measureDegreesInFahrenheit();
  // reset vor dem starten einer neuen funktion
  resetAllLeds();
  // lichtsensor testen
  dimmLedDependingOnBrightness(1);
  // reset vor dem starten einer neuen funktion
  resetAllLeds();
  // wellenfunction der default leds testen
  letDefaultLedsWave(false);
  //letDefaultLedsWave(true);
}






//////////////// assisting arduino controlling functions
// this function changes the color of the rgb led
void setRGBColor(int red, int green, int blue) {
  analogWrite(RGBpins[0], red);
  analogWrite(RGBpins[1], green);
  analogWrite(RGBpins[2], blue);  
}
// this function gets the custom number of the user
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


