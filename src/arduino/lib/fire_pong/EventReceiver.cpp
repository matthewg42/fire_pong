#include <FpEvent.h>

#ifdef DESKTOP
#include <iostream>
#else
#include <Arduino.h>
#endif
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
#ifdef DESKTOP
                std::cerr << "EventReceiver() id=0x" << std::hex << _id << " RESET" << std::endl;
#else
#ifdef DEBUG
                Serial.print(F("EventReceiver() id=0x"));
                Serial.print(_id, HEX);
                Serial.println(F(" RESET"));
#endif
#endif
				_halted = false;
			}
			return;
		} else if (e.type() == FP_EVENT_HALT) {
#ifdef DESKTOP
            std::cerr << "EventReceiver() id=0x" << std::hex << _id << " HALT" << std::endl;
#else
#ifdef DEBUG
            Serial.print(F("EventReceiver() id=0x"));
            Serial.print(_id, HEX);
            Serial.println(F(" HALT"));
#endif
#endif
			_halted = true;
			return;
		} else if (want(e)) {
#ifdef DESKTOP
            std::cerr << "EventReceiver() id=0x" << std::hex << _id << " handle()" << std::endl;
#else
#ifdef DEBUG
            Serial.print(F("EventReceiver() id=0x"));
            Serial.print(_id, HEX);
            Serial.println(F(" handle()"));
#endif
#endif
			handle(e);
		}
	}
}

EchoReceiver::EchoReceiver(fp_id_t id) :
	EventReceiver(id)
{
#ifdef DESKTOP
    std::cerr << "EchoReceiver() id=0x" << std::hex << _id << " setup()" << std::endl;
#else
#ifdef DEBUG
	Serial.print(F("EchoReceiver() id=0x"));
	Serial.print(_id, HEX);
	Serial.print(F(" setup()"));
#endif
#endif
}

EchoReceiver::~EchoReceiver()
{
#ifdef DESKTOP
    std::cerr << "~EchoReceiver() id=0x" << std::hex << _id << " deconstruct" << std::endl;
#else
#ifdef DEBUG
	Serial.print(F("~EchoReceiver() id=0x"));
	Serial.print(_id, HEX);
	Serial.print(F(" deconstruct"));
#endif
#endif
}

void EchoReceiver::handle(const FpEvent& e)
{
	if (!want(e)) { return; }
#ifdef DESKTOP
    std::cerr << "EchoReceiver() id=0x" << std::hex << _id << ": " << std::endl;
	e.dump();
#else
#ifdef DEBUG
	Serial.print(F("EchoReceiver id=0x"));
	Serial.print(_id, HEX);
	Serial.print(F(": "));
	e.dump();
#endif
#endif
}


