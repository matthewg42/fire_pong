#include <Arduino.h>
#include "crc8.h"
#include "fp_event.h"

static t_PufferEvent event;

void dump_event(t_PufferEvent *e)
{
	Serial.print(F("t_PufferEvent(id_set="));
	Serial.print(e->id_set);
	Serial.print(F(", type="));
	Serial.print(e->type);
	Serial.print(F(", duration="));
	Serial.print(e->duration);
	Serial.print(F(", checksum="));
	Serial.print(e->checksum);
	Serial.print(fp_event_validate(e) ? F(" [ok]") : F(" [INVALID]"));
	Serial.println(F(")"));
}

void setup() {
	Serial.begin(115200);
	Serial.println(F("setup complete"));
}

void loop () {
	event.id_set = 0x00100101;
	event.type = FP_EVENT_PUFF;
	event.duration = random(500);
	fp_event_set_checksum(&event);
	dump_event(&event);
	delay(1000);
}

