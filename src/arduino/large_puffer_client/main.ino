#include <Arduino.h>
#include <EventBuffer.h>
#include <FpEvent.h>
#include <PufferReceiver.h>
#include <Heartbeat.h>
#include <avr/wdt.h>

#define HEARTBEAT_PIN       13
#define LARGE_PUFFER_1_PIN  2
#define LARGE_PUFFER_2_PIN  3

void handle_event(FpEvent& e);

Heartbeat heartbeat(HEARTBEAT_PIN);
PufferReceiver *puffer[2];
EventBuffer buf(handle_event, &heartbeat);

void setup() {
    uint32_t id = 0x1;
    Serial.begin(115200);

    // Set up the heartbeat and set it to flash rapidly during setup()
    heartbeat.setup();
    heartbeat.setMode(Heartbeat::Quick);

    puffer[0] = new PufferReceiver(4096, LARGE_PUFFER_1_PIN);
    puffer[1] = new PufferReceiver(8192, LARGE_PUFFER_2_PIN);
    puffer[0]->setup();
    puffer[1]->setup();

    // Let the serial line settle and let observers see rapid heartbeat indicating reset
    int wait = millis() + 400;
    while(millis() < wait) {
        heartbeat.tick();
    }

#ifdef DEBUG
	Serial.println(F("large puffer firmware setup complete"));
#endif

    // Enable watchdog timer (250 ms before reset)
    wdt_enable(WDTO_250MS);

    // Indicate ent of setup
    heartbeat.setMode(Heartbeat::Normal);
}

void loop () {
    buf.tick();
    heartbeat.tick();
    for (uint8_t i=0; i<2; i++) {
        puffer[i]->tick();
    }
    wdt_reset();
}

void handle_event(FpEvent& e)
{
    for (uint8_t i=0; i<2; i++) {
        puffer[i]->process_event(e);
    }
}

