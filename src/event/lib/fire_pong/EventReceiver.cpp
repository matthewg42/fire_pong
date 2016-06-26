#include <fp_event.h>
#include <Arduino.h>
#include <EventReceiver.h>

//extern uint8_t* fp_event_serial_buf;

EventReceiver::EventReceiver(fp_id_t id) :
	_id(id)
{
}

EventReceiver::~EventReceiver()
{
}

bool EventReceiver::want(const fp_event& e)
{
	return e.id_match(_id);
}

EchoReceiver::EchoReceiver(fp_id_t id) :
	EventReceiver(id)
{
	Serial.print(F("EchoReceiver() id=0x"));
	Serial.print(_id, HEX);
	Serial.print(F(" setup()"));
}

EchoReceiver::~EchoReceiver()
{
	Serial.print(F("~EchoReceiver() id=0x"));
	Serial.print(_id, HEX);
	Serial.print(F(" setup()"));
}

void EchoReceiver::handle(const fp_event& e)
{
	if (!want(e)) { return; }
	Serial.print(F("EchoReceiver id=0x"));
	Serial.print(_id, HEX);
	Serial.print(F(": "));
	e.dump();
}


