#include <Arduino.h>
#include <Evt.h>
#include <Seq.h>

#define RELAY_ON        LOW
#define RELAY_OFF       HIGH
#define BUTTON_PIN      11

Seq pufferSeqForward;
Seq pufferSeqReverse;
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

void start_forward() {
    Serial.println(F("start_forward()"));
    pufferSeqForward.start(1);
}

void start_reverse() {
    Serial.println(F("start_reverse()"));
    pufferSeqReverse.start(1);
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
        relaySeq[i].append(new EvtCallbackIntBool(413,  0, set_pin, PUFFER_PINS[i][1], RELAY_OFF));
        relaySeq[i].append(new EvtCallbackIntBool(513,  0, set_pin, PUFFER_PINS[i][0], RELAY_OFF));
    }

    // Add forward sequence
    pufferSeqForward.append(new EvtCallbackIntBool(0,    0, activate_puffer, 0, true));
    pufferSeqForward.append(new EvtCallbackIntBool(400,  0, activate_puffer, 1, true));
    pufferSeqForward.append(new EvtCallbackIntBool(800,  0, activate_puffer, 2, true));
    pufferSeqForward.append(new EvtCallbackIntBool(1200,  0, activate_puffer, 3, true));
    pufferSeqForward.append(new EvtCallback(1600, 0, start_reverse));

    // Add reverse sequence
    pufferSeqReverse.append(new EvtCallbackIntBool(0,    0, activate_puffer, 2, true));
    pufferSeqReverse.append(new EvtCallbackIntBool(400,  0, activate_puffer, 1, true));
    pufferSeqReverse.append(new EvtCallback(800, 0, start_forward));

    pinMode(BUTTON_PIN, INPUT_PULLUP);     
    while (1) {
        if (!digitalRead(BUTTON_PIN)) {
            bool pressed = true;
            for (int i=0; i<500; i+=10) {
                if (digitalRead(BUTTON_PIN))
                    pressed = false;
                delay(10);
            }
            if (pressed)
                break;
        }
    }

    start_forward();

    Serial.println(F("setup() done"));
}

void loop()
{
    // switch puffer relays as appropriate
    pufferSeqForward.tick();
    pufferSeqReverse.tick();
    for(unsigned char i=0; i<4; i++) {
        relaySeq[i].tick();
    }
}


