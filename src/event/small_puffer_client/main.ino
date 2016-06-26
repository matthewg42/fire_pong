#include <EventBuffer.h>
#include <Arduino.h>
#include <FpEvent.h>
#include <SmallPufferReceiver.h>
#include <RelayReceiver.h>

void handle_event(FpEvent& e);

SmallPufferReceiver *puffer[4];
EventBuffer buf(handle_event);

void setup() {
    uint32_t id = 0x1;
    Serial.begin(115200);

    // Should define PUFFER_SEGMENT_NUMBER in CFLAGS
    for (uint8_t i=1; i<PUFFER_SEGMENT_NUMBER; i++) {
        id << 4;
    }

    for (uint8_t i=0; i<4; i++) {
        puffer[i] = new SmallPufferReceiver(id, (i*2)+2, (i*2)+3);
        puffer[i]->setup();
        id = id << 1;
    }
    delay(500);
#ifdef DEBUG
	Serial.println(F("setup complete"));
#endif
}

void loop () {
    buf.tick();
    for (uint8_t i=0; i<4; i++) {
        puffer[i]->tick();
    }
}

void handle_event(FpEvent& e)
{
#ifdef DEBUG
    Serial.print("RECV: ");
#endif
    for (uint8_t i=0; i<4; i++) {
        puffer[i]->process_event(e);
    }
}


