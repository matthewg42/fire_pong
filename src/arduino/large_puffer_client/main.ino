#include <EventBuffer.h>
#include <Arduino.h>
#include <FpEvent.h>
#include <LargePufferReceiver.h>
#include <RelayReceiver.h>

void handle_event(FpEvent& e);

LargePufferReceiver *puffer[2];
EventBuffer buf(handle_event);

void setup() {
    uint32_t id = 0x1;
    Serial.begin(115200);

    puffer[0] = new LargePufferReceiver(4096, 2);
    puffer[1] = new LargePufferReceiver(8192, 3);
    delay(500);
#ifdef DEBUG
	Serial.println(F("setup complete"));
#endif
}

void loop () {
    buf.tick();
    for (uint8_t i=0; i<2; i++) {
        puffer[i]->tick();
    }
}

void handle_event(FpEvent& e)
{
#ifdef DEBUG
    Serial.print("RECV: ");
#endif
    for (uint8_t i=0; i<2; i++) {
        puffer[i]->process_event(e);
    }
}

