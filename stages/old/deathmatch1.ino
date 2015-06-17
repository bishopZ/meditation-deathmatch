#include <Adafruit_NeoPixel.h>

#define PIN 6
#define LEDCOUNT 150

String inputString = "";         // a string to hold incoming data
String currentString = "";         // a string to hold current state
boolean stringComplete = false;  // whether the string is complete
uint32_t led_state[LEDCOUNT];

Adafruit_NeoPixel strip = Adafruit_NeoPixel(LEDCOUNT, PIN, NEO_GRB + NEO_KHZ800);

void setup() {
  Serial.begin(9600);
  inputString.reserve(200);
  currentString.reserve(200);
  for (uint16_t i = 0; i < LEDCOUNT; i++) {
    led_state[i] = 0;
  }
  strip.begin();
  strip.show(); // Initialize all pixels to 'off'
  Serial.println("Ready");
}

void loop() {
  String r, g, b;
  if (stringComplete) {
    if (inputString.indexOf("a") != -1) {
      colorNow(strip.Color(255, 0, 0));
    }
    else if (inputString.indexOf("b") != -1) {
      colorNow(strip.Color(255, 192, 0));
    }
    else if (inputString.indexOf("c") != -1) {
      colorNow(strip.Color(0, 255, 0));
    }
    else if (inputString.indexOf("d") != -1) {
      colorNow(strip.Color(0, 255, 255));
    }
    else if (inputString.indexOf("e") != -1) {
      colorNow(strip.Color(128, 64, 192));
    }
    else if (inputString.indexOf("f") != -1) {
      colorNow(strip.Color(192, 0, 128));
    }
    else {
      r = inputString.substring(0, 3);
      g = inputString.substring(4, 7);
      b = inputString.substring(8, 11);
      colorNow(strip.Color(r.toInt(), g.toInt(), b.toInt()));
      Serial.println("\n" + r + "," + g + "," + b);
    }
    Serial.println("\nwat");
    inputString = "";
    stringComplete = false;
  }
}

void serialEvent() {
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    inputString += inChar;
    Serial.print(inChar);
    if (inChar == '\n' || inChar == '\r') {
      stringComplete = true;
    }
  } 
}


void colorNow(uint32_t c) {
  for (uint16_t i=0; i<strip.numPixels(); i++) {
    strip.setPixelColor(i, c);
  }
  strip.show();
}


// Fill the dots one after the other with a color
void colorWipe(uint32_t c, uint8_t wait) {
  for(uint16_t i=0; i<strip.numPixels(); i++) {
      strip.setPixelColor(i, c);
      strip.show();
      delay(wait);
  }
}

