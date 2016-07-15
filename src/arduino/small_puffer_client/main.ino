#include <EventBuffer.h>
#include <Arduino.h>
#include <FpEvent.h>
#include <SmallPufferReceiver.h>
#include <RelayReceiver.h>
#include <Heartbeat.h>

#define HEARTBEAT_PIN    13

void handle_event(FpEvent& e);

SmallPufferReceiver *puffer[4];
Heartbeat heartbeat(HEARTBEAT_PIN);
EventBuffer buf(handle_event, &heartbeat);

void setup() {
    uint32_t id = 0x1;
    Serial.begin(115200);

    heartbeat.setup();

    // Should define PUFFER_SEGMENT_NUMBER in CFLAGS
    for (uint8_t i=1; i<PUFFER_SEGMENT_NUMBER; i++) {
        id = id << 4;
    }

    for (uint8_t i=0; i<4; i++) {
        puffer[i] = new SmallPufferReceiver(id, (i*2)+3, (i*2)+2);
        puffer[i]->setup();
        id = id << 1;
    }

    delay(500);
#ifdef DEBUG
	Serial.print(F("small puffer firmware segment "));
	Serial.print(PUFFER_SEGMENT_NUMBER);
    Serial.println(F(" setup complete"));
#endif
}

void loop () {
    buf.tick();
    heartbeat.tick();
    for (uint8_t i=0; i<4; i++) {
        puffer[i]->tick();
    }
}

void handle_event(FpEvent& e)
{
    for (uint8_t i=0; i<4; i++) {
#ifdef DEBUG
        Serial.print(F("handle_event; puffer "));
        Serial.println(i);
#endif
        puffer[i]->process_event(e);
    }
}


