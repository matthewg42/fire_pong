#include <EventBuffer.h>
#include <Arduino.h>
#include <fp_event.h>
#include "RelayReceiver.h"

void handle_event(fp_event& e);

RelayReceiver relay(0x01, 2);
EventBuffer buf(handle_event);

void setup() {
	Serial.begin(115200);
    delay(500);
    relay.setup();
	Serial.println(F("setup complete"));
}

void loop () {
    buf.tick();
    relay.tick();
}

void handle_event(fp_event& e)
{
    Serial.print("RECV: ");
    e.dump();
    relay.handle(e);
}


