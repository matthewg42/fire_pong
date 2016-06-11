#include <Arduino.h>
#include "Evt.h"
#include "Seq.h"

#define RELAY_ON        LOW
#define RELAY_OFF       HIGH

Seq pufferSeq;
Seq relaySeq[4];

unsigned char PUFFER_PINS[4][2] = {  
   {2, 3} , // puffer 0
   {4, 5} , // puffer 1
   {6, 7} , // puffer 2
   {8, 9}   // puffer 3
};

void activate_puffer(int id, bool on) {
    Serial.print(F("PUFF:"));
    Serial.println(id);
    relaySeq[id].start(1);   
}

void set_pin(int pin, bool state) {
    Serial.print(F("Relay PIN "));
    Serial.print(pin);
    Serial.print(F(" : "));
    Serial.println(state==RELAY_ON ? F("ON") : F("OFF"));
    digitalWrite(pin, state);
}

void setup()
{
    Serial.begin(115200);

    // Set relay pins for output
    for(unsigned char i=0; i<4; i++) {
        pinMode(PUFFER_PINS[i][0], OUTPUT);     
        set_pin(PUFFER_PINS[i][0], RELAY_OFF);
        pinMode(PUFFER_PINS[i][1], OUTPUT);     
        set_pin(PUFFER_PINS[i][1], RELAY_OFF);
        relaySeq[i].append(new EvtCallbackIntBool(0,    0, set_pin, PUFFER_PINS[i][0], RELAY_ON));
        relaySeq[i].append(new EvtCallbackIntBool(100,  0, set_pin, PUFFER_PINS[i][1], RELAY_ON));
        relaySeq[i].append(new EvtCallbackIntBool(113,  0, set_pin, PUFFER_PINS[i][1], RELAY_OFF));
        relaySeq[i].append(new EvtCallbackIntBool(313,  0, set_pin, PUFFER_PINS[i][1], RELAY_ON));
        relaySeq[i].append(new EvtCallbackIntBool(463,  0, set_pin, PUFFER_PINS[i][1], RELAY_OFF));
        relaySeq[i].append(new EvtCallbackIntBool(763,  0, set_pin, PUFFER_PINS[i][0], RELAY_OFF));
    }

    // Add four puff enents - one for each puffer
    pufferSeq.append(new EvtCallbackIntBool(1000, 1, activate_puffer, 0, true));
    pufferSeq.append(new EvtCallbackIntBool(1500, 1, activate_puffer, 1, true));
    pufferSeq.append(new EvtCallbackIntBool(2000, 1, activate_puffer, 2, true));
    pufferSeq.append(new EvtCallbackIntBool(2500, 1, activate_puffer, 3, true));

    Serial.println(F("setup() done"));
}

void loop()
{
    // switch puffer relays as appropriate
    pufferSeq.tick();
    for(unsigned char i=0; i<4; i++) {
        relaySeq[i].tick();
    }
}


