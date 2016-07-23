#include <MatrixText.h>

/********************************************************
/****** 7 Segment LED driver board Basic Code 1 *********
/****** by Matt Little **********************************
/****** Date: 5/4/13 ************************************
/****** info@re-innovation.co.uk ************************
/****** www.re-innovation.co.uk *************************
/********************************************************

/* Adaped by Daniel Swann 26/08/2014 to test MatrixText *

This example uses the Serial Shift output to control a 7 segment LED display
Data is shifted out serially and only when all the shift registers are filled does the latch cause
the LED outputs to update.
The LED boards require 12V supply as they contain strings of 4 LEDs.
The wiring for each board is as follows (P1 and P2):

  Pin 1  ->  Serial LATCH -> A3 on Arduino (in this example)
  Pin 2  ->  Serial CLOCK -> A5 on Arduino (in this example)
  Pin 3  ->  Serial DATA  -> A4 on Arduino (in this example)  
  Pin 4  ->  GROUND       -> GND on Arduino
  Pin 5  ->  +5V          -> +5V on Arduino
  Pin 6  ->  GROUND       -> GND for LED supply
  Pin 7  ->  +12V         -> +12V for LED supply

Use a 0.1uF capacitor between Pin 1 (sLATCH) and Pin 4 (GND) to prevent flicker on the display.

see www.re-innovation.co.uk for more details
 
*/

// Our matrix display dimensions
const int DISPLAY_WIDTH     = 12;
const int DISPLAY_HEIGHT    = 8;

// Inputs and Outputs
const int SLATCH_PIN        = 2;    // Pin connected to ST_CP of 74HC595
const int SCLK_PIN          = 3;    // Pin connected to SH_CP of 74HC595
const int SDATA_PIN         = 4;    // Pin connected to DS of 74HC595
const int LED_PIN           = 13;   // LED of ProMini
const int MODE_BUTTON_PIN   = 5;    // Pin attached to mode selection button

// Number of modes (to be replaced with enum)
const int maxModes          = 3;

// Static display messages
const char text[]           = "Rule Zero*";
const char text1[]          = "More of a guideline, really";
const char text2[]          = "Setting Up - please do not disturb crew";

// Buffer for display data
uint8_t dataArray[DISPLAY_WIDTH];

// Object to generate display data (using D. Swann's library)
MatrixText *mt1;

int SWcounter               = 0;    // Debounce counter for the switch
int currentMode             = 0;    // This holds the mode we are in
bool lastPress              = HIGH; // This is to latch the button press

// Function declatations for Makefile build
void set_xy (uint16_t x, uint16_t y, byte val);

void setup()
{
    //set pins to output so you can control the shift register
    pinMode(SLATCH_PIN, OUTPUT);
    pinMode(SCLK_PIN, OUTPUT);
    pinMode(SDATA_PIN, OUTPUT);
    pinMode(LED_PIN, OUTPUT);   
    pinMode(MODE_BUTTON_PIN, INPUT_PULLUP); 

    mt1 = new MatrixText(set_xy);
    mt1->show_text(text, 0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT);
    mt1->set_scroll_speed(100); // Advance text position every 100ms

    memset(dataArray,0,sizeof(uint8_t)*DISPLAY_WIDTH);  // Set dataArray to clear it 
}

void loop()
{ 
    mt1->loop(); // do scrolling text
  
    // Write the dataArray to the LED matrix:
    digitalWrite(SLATCH_PIN, LOW);  
    for(int j=0;j<sizeof(dataArray);j++)
    {     
        shiftOut(SDATA_PIN, SCLK_PIN, LSBFIRST, dataArray[j]);  // Rotated text
    }
    digitalWrite(SLATCH_PIN, HIGH); 

    // Only want to do this if the switch has been pressed
    if(lastPress==HIGH)
    {  
        // Choose what to do depending upon the mode:
        // Mode are:
        // 0 = flash random colours
        // 1 = Write "Nottingham Hackspace"
        // 2 = Write "ERROR"
        switch(currentMode)
        {
            case 0:
                // Mode = 0   
                // Output text from text 1
                mt1->show_text(text, 0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT);
                break;
            case 1:
                // Mode = 1
                // In this case show text 2
                mt1->show_text(text1, 0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT);
                break;
            case 2:
                // Mode = 2
                // In this case show text 2
                mt1->show_text(text2, 0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT);
                break; 
            case 3:
                // Mode = 3
                // Just show a full ON screen
                for(int j=0;j<12;j++) {  
                    dataArray[j] = B11111111;
                }          
                break;   
            default:
                // Do this when not in a mode
                break;    
        }  
    }

    // Check the switch and change mode depending:
    if(digitalRead(MODE_BUTTON_PIN)==LOW&&lastPress==LOW) {
        // Button pressed so count up
        SWcounter++;
        if(SWcounter>=50)
        {
            currentMode++;
            if(currentMode>maxModes)
            {
                currentMode=0;
            }
            lastPress=HIGH;
        }
    }
    else if (digitalRead(MODE_BUTTON_PIN)==HIGH&&lastPress==HIGH)
    {
        // Button NOT pressed - reset everything
        SWcounter=0;
        lastPress=LOW;
    }

    // This is the main delay and slows everything down a bit.
    delay(10);

}

void set_xy (uint16_t x, uint16_t y, byte val)
{
    /// x is the column, y is the bit within the column (0 to 7)
    // The shift register is in the bit format 70123456, so we must move the last bit and push it into the first bit.
    byte actual_y;// = (y-1)%8; 

    if (y == 0) {
        actual_y = 7; 
    } else {
        actual_y = y - 1;
    }

    if (val) {
        dataArray[x] |= 1 << actual_y;    // Set bit
    } else {
        dataArray[x] &= ~(1 << actual_y); // Clear bit
    }
}


