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

#define DISPLAY_WIDTH   12
#define DISPLAY_HEIGHT  8

// Function declatations
void set_xy (uint16_t x, uint16_t y, byte val);

// This is for the serial shifted output data
const int sLatch =      2;   //Pin connected to ST_CP of 74HC595
const int sClk =        3;    //Pin connected to SH_CP of 74HC595
const int sData =       4;    //Pin connected to DS of 74HC595
const int led =         13;  //LED of Minimus
const int swInputA =    5;  // An input switch

const int maxModes =    3;  // Total number of switch modes

int number = 0;  // This will be the displayed data

uint8_t dataArray[DISPLAY_WIDTH];  // This holds the data to display 

MatrixText *mt1;  // MatrixText string

const char text[] = "Rule Zero*";
const char text1[] = "More of a guideline, really";
const char text2[] = "Setting Up - please do not disturb crew";

int SWcounter = 0;  // This is a debounce counter for the switch

int mode = 0;  // This holds the mode we are in

boolean lastPress= HIGH;  // This is to latch the button press

void setup()
{
  //set pins to output so you can control the shift register
  pinMode(sLatch, OUTPUT);
  pinMode(sClk, OUTPUT);
  pinMode(sData, OUTPUT);
  pinMode(led, OUTPUT);   
  pinMode(swInputA, INPUT_PULLUP); 
  
  mt1 = new MatrixText(set_xy);
  mt1->show_text(text, 0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT);
  mt1->set_scroll_speed(100); // Advance text position every 100ms

  memset(dataArray,0,sizeof(uint8_t)*DISPLAY_WIDTH);  // Set dataArray to clear it 
  
}

void loop()
{ 
  mt1->loop(); // do scrolling text
  
  // Write the dataArray to the LED matrix:
  digitalWrite(sLatch, LOW);  
  for(int j=0;j<sizeof(dataArray);j++)
  {     
    //shiftOut(sData, sClk, MSBFIRST, dataArray[j]);
    shiftOut(sData, sClk, LSBFIRST, dataArray[j]);  // Rotated text
  }
  digitalWrite(sLatch, HIGH); 


  // Only want to do this if the switch has been pressed
  if(lastPress==HIGH)
  {  
    // Choose what to do depending upon the mode:
    // Mode are:
    // 0 = flash random colours
    // 1 = Write "Nottingham Hackspace"
    // 2 = Write "ERROR"
    switch(mode)
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
        for(int j=0;j<12;j++)
        {  
          dataArray[j] = B11111111;
        }          
      break;   
      
      default:
      // Do this when not in a mode
         
      break;    
    }  
  }
   
  // Check the switch and change mode depending:
  if(digitalRead(swInputA)==LOW&&lastPress==LOW)
  {
    // Button pressed so count up
    SWcounter++;
    if(SWcounter>=50)
    {
      mode++;
      if(mode>maxModes)
      {
        mode=0;
      }
      lastPress=HIGH;
    }
  }
  else if (digitalRead(swInputA)==HIGH&&lastPress==HIGH)
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
  
  if (y == 0)
  {
   actual_y = 7; 
  }
  else
  {
    actual_y = y - 1;
  }
  
  if (val)
    dataArray[x] |= 1 << actual_y;    // Set bit
  else
    dataArray[x] &= ~(1 << actual_y); // Clear bit
}


