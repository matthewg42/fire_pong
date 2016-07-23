#include <MatrixText.h>
#include <FpEvent.h>
#include <EventBuffer.h>
#include <Heartbeat.h>
#include <DisplayReceiver.h>
#include "MessageStore.h"

using namespace std;

/*
    FirePong Display Client

    2016-07-23  Mouse;        Adapted for FirePong
    2014-08-26  Daniel Swann; Adapted to test MatrixText 
    2013-04-04  Matt Little;  Original code; info@re-innovation.co.uk; www.re-innovation.co.uk

    see also http://www.instructables.com/files/orig/F8R/C5ME/I2P3NA7V/F8RC5MEI2P3NA7V.zip
    and http://www.instructables.com/id/Large-Scrolling-LED-display/?ALLSTEPS
*/

// Our matrix display dimensions
const int DISPLAY_WIDTH     = 12;
const int DISPLAY_HEIGHT    = 8;

// Default messages for this firmware
const char* MESSAGE1        = "Welcome to Nottingham Hackspace";
const char* MESSAGE2        = "www.nottinghack.org.uk";
const char* MESSAGE3        = "Ask me for a hackspace tour...";

// Firepong PID for display node
const uint32_t pid = 0x4000; 

// Inputs and Outputs
const int SLATCH_PIN        = 2;    // Pin connected to ST_CP of 74HC595
const int SCLK_PIN          = 3;    // Pin connected to SH_CP of 74HC595
const int SDATA_PIN         = 4;    // Pin connected to DS of 74HC595
const int LED_PIN           = 13;   // LED of ProMini
const int MODE_BUTTON_PIN   = 5;    // Pin attached to mode selection button

// This will hold our messages
MessageStore messageStore;
int currentMessage          = 0;    // Current message index

// Buffer for display data
uint8_t dataArray[DISPLAY_WIDTH];

// Object to generate display data (using D. Swann's library)
MatrixText *matrixText;

// So we can know what's happening by looking at the LED
Heartbeat heartbeat(LED_PIN);


int SWcounter               = 0;    // Debounce counter for the switch
int currentMode             = 0;    // This holds the mode we are in
bool lastPress              = HIGH; // This is to latch the button press

// Function declatations for Makefile build
void set_xy (uint16_t x, uint16_t y, byte val);
void handleEvent(FpEvent& e);
void displayText(const char* message);

// This object parses incoming FpEvent messages over serial
EventBuffer eventBuffer(handleEvent, &heartbeat);

DisplayReceiver displayReceiver(pid, displayText);

void setup()
{
#ifdef DEBUG
    Serial.begin(115200);
    delay(400);
    Serial.println(F("display client setup() BEGIN"));
#endif
    //set pins to output so you can control the shift register
    pinMode(SLATCH_PIN, OUTPUT);
    pinMode(SCLK_PIN, OUTPUT);
    pinMode(SDATA_PIN, OUTPUT);
    pinMode(MODE_BUTTON_PIN, INPUT_PULLUP); 

    heartbeat.setup();  // this will set the mode of LED_PIN

    messageStore.clear();
    messageStore.add(MESSAGE1);
    messageStore.add(MESSAGE2);
    messageStore.add(MESSAGE3);

    matrixText = new MatrixText(set_xy);
    matrixText->show_text(messageStore[currentMessage], 0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT);
    matrixText->set_scroll_speed(100); // Advance text position every 100ms

    memset(dataArray,0,sizeof(uint8_t)*DISPLAY_WIDTH);  // Set dataArray to clear it 

    // Blink rapidly for a period so we know setup() ran
    heartbeat.setMode(Heartbeat::Quick);
    for (unsigned long int wait=millis() + 400; millis()<wait;) {
        heartbeat.tick();
    }
    heartbeat.setMode(Heartbeat::Normal);

#ifdef DEBUG
    Serial.println(F("display client setup() END"));
#endif
}

void loop()
{ 
    // blinky blink
    heartbeat.tick();

    // handle incoming serial data
    eventBuffer.tick();

    // do scrolling text
    matrixText->loop();
  
    // Write the dataArray to the LED matrix:
    digitalWrite(SLATCH_PIN, LOW);  
    for(unsigned int j=0;j<sizeof(dataArray);j++) {     
        shiftOut(SDATA_PIN, SCLK_PIN, LSBFIRST, dataArray[j]);  // Rotated text
    }
    digitalWrite(SLATCH_PIN, HIGH); 

    // Only want to do this if the switch has been pressed
    if(lastPress==HIGH)
    {  
        currentMessage++;
        if (currentMessage == messageStore.size()-1) {
            // "after" the last message we will have an additional test mode
            // where we show every pixel ON
            for(int w=0;w<DISPLAY_WIDTH;w++) {  
                dataArray[w] = 0xff;
            }      
        } else {
            // wrap if necessary
            currentMessage = currentMessage % messageStore.size();
            matrixText->show_text(messageStore[currentMessage], 0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT);
        }
    }

    // Check the switch and change mode depending:
    if (digitalRead(MODE_BUTTON_PIN) == LOW && lastPress == LOW) {
        // Button pressed so count up
        SWcounter++;
        if(SWcounter>=50)
        {
            currentMode++;
            if(currentMode>MAX_MESSAGE_COUNT) {
                currentMode=0;
            }
            lastPress=HIGH;
        }
    }
    else if (digitalRead(MODE_BUTTON_PIN) == HIGH && lastPress == HIGH) {
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

void handleEvent(FpEvent& e)
{
#ifdef DEBUG
    Serial.print(F("Display received event: "));   
    e.dump();
#endif    
    displayReceiver.process_event(e);
}

void displayText(const char* message)
{
#ifdef DEBUG
    Serial.print(F("DISPLAY: "));   
    Serial.println(message);
#endif    
    messageStore.clear();
    messageStore.add(message);
    currentMessage = 0;
    matrixText->show_text(messageStore[currentMessage], 0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT);
}



