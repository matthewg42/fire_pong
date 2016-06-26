#include <EventBuffer.h>
#include <Arduino.h>
#include <fp_event.h>
#include "RelayReceiver.h"

void handle_event(fp_event& e);

RelayReceiver *relay[8];
EventBuffer buf(handle_event);

void setup() {
	Serial.begin(115200);
    delay(500);
    uint32_t id = 0x1;
    for (int i=0; i<8; i++) {
        relay[i] = new RelayReceiver(id, 2+i);
        relay[i]->setup();
        id = id << 1;
    }
	Serial.println(F("setup complete"));
}

void loop () {
    buf.tick();
    for (int i=0; i<8; i++) {
        relay[i]->tick();
    }
}

void handle_event(fp_event& e)
{
    Serial.print("RECV: ");
    e.dump();
    for (int i=0; i<8; i++) {
        relay[i]->handle(e);
    }
}


