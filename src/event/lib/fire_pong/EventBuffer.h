#pragma once

#include <FpEvent.h>

#define SERIAL_CLEAR_MS 30

typedef void (*callback_function)(FpEvent& e); 

class EventBuffer {
public:
	EventBuffer(callback_function cb);
	
	int wait_serial_clear();
	void reset();
	void tick();

private:
	uint8_t _buf[FP_SERIAL_BUF_LEN];
	fp_length_t _ptr;
	fp_length_t _packet_length;
	unsigned long _last_packet_start;
	callback_function _callback;

};

