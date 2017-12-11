String readSerialString;
byte dimmbrightness = 80;
boolean blink = false;

// LEDpins from left to right; RGBpins Red Green Blue
int LEDpins[] = {4, 5, 6, 7}, RGBpins[] = {11, 10, 9};
boolean turnOnTheLights[] = {false, false, false, false};
int i = 0;
int tempartureSensorPin = 0; //Muss auf den PIN des Senosrs noch geändert werden
int LEDCount = 4;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  for (i = 0; i < 4; i++)
    pinMode(LEDpins[i], OUTPUT);
  
  for (i = 0; i < 3; i++)
    pinMode(RGBpins[i], OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available() > 0) {
    // read the incoming byte:
    readSerialString = Serial.readString();
    
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
      blink = blink ? false : true;
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
    else if(readSerialString.startsWith("binary")) {
      showBinary(getValue(readSerialString, ':',1).toInt());
      for(i = 0; i < 4; i++){
        if(turnOnTheLights[i] == true)
          digitalWrite(LEDpins[i], HIGH);
        else
          digitalWrite(LEDpins[i], LOW);
      }
    }
    else if(readSerialString.startsWith("LEDON")) {
      int ledOnNum = getValue(readSerialString,':', 1).toInt() - 1;
      
      if(ledOnNum >= 0 && ledOnNum < LEDCount) {
        for(i = 0; i < LEDCount; i++) {
          turnOnTheLights[i] = false;
        }
        
        turnOnTheLights[ledOnNum] = true;
        
        for(i = 0; i < LEDCount; i++) {
          if(turnOnTheLights[i] == true)
            digitalWrite(LEDpins[i], HIGH);
          else
            digitalWrite(LEDpins[i], LOW);
        }
        
      Serial.println("LED " + (ledOnNum + 1) + " turned ON");
      } else {
        Serial.println("LED could not be turned on.");
      }
    }
    else if(readSerialString == "measureTemperature"){
        int val;                
        val=analogRead();      
        Serial.println("Temperatur:"+val);    
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
  analogWrite(RGBpins[0], red);
  analogWrite(RGBpins[1], green);
  analogWrite(RGBpins[2], blue);  
}

String getValue(String data, char separator, int index) {
 int found = 0;
 int strIndex[] = {0, -1};
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
  
  for(i = 0; i < 4; i++)
     turnOnTheLights[i] = false;
  
  i = 0;
  while(n!=0) {
    remainder = n%2;
    
    Serial.print(remainder);
    if(remainder == 1) turnOnTheLights[i] = true;
    
    n /= 2;
    i++;
  }
}
