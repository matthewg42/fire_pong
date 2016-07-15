#pragma once

#include <FpEvent.h>
#include <Heartbeat.h>

#define SERIAL_CLEAR_MS     30
#define PACKET_TIMEOUT_MS   500

#define WAITING             Heartbeat::Normal
#define RECEIVING           Heartbeat::Quick
#define HALTED              Heartbeat::Slow
#define UNKNOWN             Heartbeat::Slower

typedef void (*callback_function)(FpEvent& e); 

class EventBuffer {
public:
	EventBuffer(callback_function cb, Heartbeat* heartbeat);
	
	int wait_serial_clear();
	void reset();
	void tick();

    void setHeartbeat(Heartbeat::Mode mode);

private:
	uint8_t _buf[FP_SERIAL_BUF_LEN];
	fp_length_t _ptr;
	fp_length_t _packet_length;
	unsigned long _last_packet_start;
	callback_function _callback;
    unsigned long _packet_timeout;
    bool _halted;
    Heartbeat* _heartbeat;

};

