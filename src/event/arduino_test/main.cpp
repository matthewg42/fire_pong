#include <Arduino.h>
#include <crc8.h>
#include <fp_event.h>

void setup() {
	Serial.begin(115200);
	Serial.println(F("setup complete"));
}

void loop () {
	uint8_t buf[FP_SERIAL_BUF_LEN];
	memset(buf, 0, FP_SERIAL_BUF_LEN);
	fp_event e(0x1, FP_EVENT_SPARK, FP_STR("data"), 4);
	e.dump();
    // MMLIIIIT[D...]CMM
	buf[0] = 'f';
	buf[1] = 'P';
	buf[2] = 15;		// length
	buf[3] = 1;         // id byte 1
	buf[4] = 0;
	buf[5] = 0;
	buf[6] = 0;
	buf[7] = FP_EVENT_SPARK;
	buf[8] = 'd';
	buf[9] = 'a';
	buf[10] = 't';
	buf[11] = 'a';
	buf[12] = 0x8a;     // checksum
	buf[13] = 'f';
	buf[14] = 'P';

	fp_event e2(buf);
	e2.dump();
	
	buf[8] = 'D';
	fp_event e3(buf);
	e3.dump();
	delay(10000);
}

