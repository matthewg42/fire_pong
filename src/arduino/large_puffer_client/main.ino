#include <Arduino.h>
#include <EventBuffer.h>
#include <FpEvent.h>
#include <PufferReceiver.h>
#include <Heartbeat.h>

#define HEARTBEAT_PIN    13

void handle_event(FpEvent& e);

Heartbeat heartbeat(HEARTBEAT_PIN);
PufferReceiver *puffer[2];
EventBuffer buf(handle_event, &heartbeat);

void setup() {
    uint32_t id = 0x1;
    Serial.begin(115200);

    heartbeat.setup();

    puffer[0] = new PufferReceiver(4096, 2);
    puffer[1] = new PufferReceiver(8192, 3);
    delay(500);
#ifdef DEBUG
	Serial.println(F("large puffer firmware setup complete"));
#endif
}

void loop () {
    buf.tick();
    for (uint8_t i=0; i<2; i++) {
        puffer[i]->tick();
    }
    heartbeat.tick();
}

void handle_event(FpEvent& e)
{
    for (uint8_t i=0; i<2; i++) {
        puffer[i]->process_event(e);
    }
}

