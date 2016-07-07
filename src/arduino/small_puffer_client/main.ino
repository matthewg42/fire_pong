#include <EventBuffer.h>
#include <Arduino.h>
#include <FpEvent.h>
#include <SmallPufferReceiver.h>
#include <RelayReceiver.h>

#define HEARTBEAT_PIN    13
#define HEARTBEAT_OFF_MS 500
#define HEARTBEAT_ON_MS  50

void handle_event(FpEvent& e);
void heartbeat_tick();

SmallPufferReceiver *puffer[4];
EventBuffer buf(handle_event);
unsigned long lastHeartbeat = 0;
bool heartbeatOn = true;

void setup() {
    uint32_t id = 0x1;
    Serial.begin(115200);

    pinMode(HEARTBEAT_PIN, OUTPUT);
    digitalWrite(HEARTBEAT_PIN, heartbeatOn);

    // Should define PUFFER_SEGMENT_NUMBER in CFLAGS
    for (uint8_t i=1; i<PUFFER_SEGMENT_NUMBER; i++) {
        id = id << 4;
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
    heartbeat_tick();
}

void heartbeat_tick()
{
    unsigned long now = millis();
    if (now - lastHeartbeat > (heartbeatOn ? HEARTBEAT_ON_MS : HEARTBEAT_OFF_MS)) {
        heartbeatOn = !heartbeatOn;
        digitalWrite(HEARTBEAT_PIN, heartbeatOn);
        lastHeartbeat = now;
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


