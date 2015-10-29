#include <Adafruit_NeoPixel.h>

/*****************************************************************************/
// Debug 0 or 1
int debug = 1;

// Number of RGB LEDs in strand:
int nStages = 2;
int nNumStageBlock = 1;
int nLEDs = 150;

// Max String Size
int stringMax = 200;

String inputString = "";         // a string to hold incoming data
boolean stringComplete = false;  // whether the string is complete

int dataPins[2];
int clockPin = 3;

Adafruit_NeoPixel strip1 = Adafruit_NeoPixel((nLEDs * nNumStageBlock), 5, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel strip2 = Adafruit_NeoPixel((nLEDs * nNumStageBlock), 7, NEO_GRB + NEO_KHZ800);


void setup() {

  // Start up the LED strip
  strip1.begin();
  strip2.begin();
  
  // Update the strip, to start they are all 'off'
  strip1.show();
  strip2.show();
    
  Serial.begin(9600);
  inputString.reserve(stringMax);

  Serial.println("Ready");
  
}


void loop() {

  String r, g, b;
  
  serialEvent();
  
  if (stringComplete) {
    
    if (inputString.startsWith("1,")) {    
    
      if (inputString.indexOf("a") != -1) {
        colorNow1(strip1.Color(255, 0, 0));
      }
      else if (inputString.indexOf("b") != -1) {
        colorNow1(strip1.Color(255, 192, 0));
      }
      else if (inputString.indexOf("c") != -1) {
        colorNow1(strip1.Color(0, 255, 0));
      }
      else if (inputString.indexOf("d") != -1) {
        colorNow1(strip1.Color(0, 255, 255));
      }
      else if (inputString.indexOf("e") != -1) {
        colorNow1(strip1.Color(128, 64, 192));
      }
      else if (inputString.indexOf("f") != -1) {
        colorNow1(strip1.Color(192, 0, 128));
      }
      else {
  
        if (inputString.length() >= 15) { 
        
          inputString = "";
          
          if (debug) {
             
            Serial.println("RGB Buffer Overrun and Truncation");
            
          }
        
        } else {
        
          r = inputString.substring(2, 5);
          g = inputString.substring(6, 9);
          b = inputString.substring(10, 131);
          colorNow1(strip1.Color(r.toInt(), g.toInt(), b.toInt()));
          
          if (debug) {
            Serial.println("\n" + r + "," + g + "," + b);
          }
        
        }
        
      }
      
    } else {
      
      if (inputString.indexOf("a") != -1) {
        colorNow2(strip2.Color(255, 0, 0));
      }
      else if (inputString.indexOf("b") != -1) {
        colorNow2(strip2.Color(255, 192, 0));
      }
      else if (inputString.indexOf("c") != -1) {
        colorNow2(strip2.Color(0, 255, 0));
      }
      else if (inputString.indexOf("d") != -1) {
        colorNow2(strip2.Color(0, 255, 255));
      }
      else if (inputString.indexOf("e") != -1) {
        colorNow2(strip2.Color(128, 64, 192));
      }
      else if (inputString.indexOf("f") != -1) {
        colorNow2(strip2.Color(192, 0, 128));
      }
      else {
  
        if (inputString.length() >= 15) { 
        
          inputString = "";
          
          if (debug) {
             
            Serial.println("RGB Buffer Overrun and Truncation");
            
          }
        
        } else {
        
          r = inputString.substring(2, 5);
          g = inputString.substring(6, 9);
          b = inputString.substring(10, 131);
          colorNow2(strip2.Color(r.toInt(), g.toInt(), b.toInt()));
          
          if (debug) {
            Serial.println("\n" + r + "," + g + "," + b);
          }
        
        }
        
      }
      
    }
    
    inputString = "";
    stringComplete = false;
    
  }
  
}

void serialEvent() {
  while (Serial.available()) {
    char inChar = (char)Serial.read();

    if (inputString.length() >= stringMax) { 
    
      inputString = "";
      
      if (debug) {
         
        Serial.println("String Buffer Overrun and Truncation");
        
      }
    
    }

    inputString += inChar;
    
    if (debug) {
      Serial.print(inChar);  
    }
    
    if (inChar == '\n' || inChar == '\r') {
      stringComplete = true;
    }
  } 
}


void colorNow1(uint32_t c) {
  for (uint16_t i=0; i<strip1.numPixels(); i++) {
    strip1.setPixelColor(i, c);
  }
  strip1.show();
}

void colorNow2(uint32_t c) {
  for (uint16_t i=0; i<strip2.numPixels(); i++) {
    strip2.setPixelColor(i, c);
  }
  strip2.show();
}
