#include <iostream>
#include <fp_event.h>
#include <string.h>
#include <stdint.h>

using namespace std;

int main(int argc, char** argv)
{
	uint16_t duration = 1234;
	fp_event e0(1, FP_EVENT_HALT);
	e0.dump();
	fp_event e1(0x87654321, FP_EVENT_PUFF, reinterpret_cast<uint8_t*>(&duration), sizeof(uint16_t));
	e1.dump();
	uint8_t buf[FP_SERIAL_BUF_LEN];
	memset(buf, 0, FP_SERIAL_BUF_LEN);

	fp_event e2(0x1, FP_EVENT_SPARK, FP_STR("data"), 4);
	e2.dump();

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

	fp_event e3(buf);
	e3.dump();
	
	buf[8] = 'D';
	fp_event e4(buf);
	e4.dump();
	return 0;
}
