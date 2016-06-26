#include <FpEvent.h>
#include <Arduino.h>
#include <EventReceiver.h>

//extern uint8_t* fp_event_serial_buf;

EventReceiver::EventReceiver(fp_id_t id) :
	_id(id),
	_halted(false)
{
}

EventReceiver::~EventReceiver()
{
}

void EventReceiver::process_event(const FpEvent& e)
{
	if (e.id_match(_id)) {
		if (_halted) {
			if (e.type() == FP_EVENT_RESET) {
				_halted = false;
			}
			return;
		} else if (e.type() == FP_EVENT_HALT) {
			_halted = true;
			return;
		} else if (want(e)) {
			handle(e);
		}
	}
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
	Serial.print(F(" deconstruct"));
}

void EchoReceiver::handle(const FpEvent& e)
{
	if (!want(e)) { return; }
	Serial.print(F("EchoReceiver id=0x"));
	Serial.print(_id, HEX);
	Serial.print(F(": "));
	e.dump();
}


