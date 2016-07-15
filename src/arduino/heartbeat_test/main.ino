#include <EventBuffer.h>
#include <Arduino.h>
#include <Heartbeat.h>

#define HEARTBEAT_PIN    13

Heartbeat heartbeat(HEARTBEAT_PIN);

void setup() {
    Serial.begin(115200);

    heartbeat.setup();

#ifdef DEBUG
	Serial.println(F("setup complete"));
#endif
}

void loop () {
    unsigned long m = millis() / 4000;

    switch (m%4) {
    case 0:
        if (heartbeat.mode()!=Heartbeat::Waiting) {
            Serial.println(F("Starting Heartbeat::Waiting"));
            heartbeat.setMode(Heartbeat::Waiting);
        }
        break;
    case 1:
        if (heartbeat.mode()!=Heartbeat::Receiving) {
            Serial.println(F("Starting Heartbeat::Receiving"));
            heartbeat.setMode(Heartbeat::Receiving);
        }
        break;
    case 2:
        if (heartbeat.mode()!=Heartbeat::Halted) {
            Serial.println(F("Starting Heartbeat::Halted"));
            heartbeat.setMode(Heartbeat::Halted);
        }
        break;
    case 3:
        if (heartbeat.mode()!=Heartbeat::Error) {
            Serial.println(F("Starting Heartbeat::Error"));
            heartbeat.setMode(Heartbeat::Error);
        }
        break;
    }
    heartbeat.tick();
}


