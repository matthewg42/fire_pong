#include <RelayReceiver.h>
#ifdef DESKTOP
#include <iostream>
#else
#include <Arduino.h>
#endif

void set_pin(int pin, bool state) {
#ifdef DESKTOP
    std::cerr << "Relay PIN " << pin << " : " << (state==RELAY_ON ? "ON" : "OFF") <<  std::endl;
#else
#ifdef DEBUG
    Serial.print(F("Relay PIN "));
    Serial.print(pin);
    Serial.print(F(" : "));
    Serial.println(state==RELAY_ON ? F("ON") : F("OFF"));
#endif
    digitalWrite(pin, state);
#endif
}

RelayReceiver::RelayReceiver(fp_id_t id, uint8_t pin) :
	EventReceiver(id),
	_pin(pin)
{
}

RelayReceiver::~RelayReceiver()
{
#ifndef DESKTOP
	digitalWrite(_pin, RELAY_OFF);
#endif
}

bool RelayReceiver::want(const FpEvent& e)
{
	return e.type() == FP_EVENT_RELAY;
}

void RelayReceiver::setup()
{
#ifndef DESKTOP
	pinMode(_pin, OUTPUT);
	digitalWrite(_pin, RELAY_OFF);
#endif
}

void RelayReceiver::handle(const FpEvent& e)
{
	if (e.data_length() != sizeof(uint16_t)) {
#ifdef DESKTOP
        std::cerr << "RelayReceiver::handle wrong data length: " << e.data_length() << std::endl;
#else
#ifdef DEBUG
		Serial.print(F("RelayReceiver::handle wrong data length: "));
		Serial.println(e.data_length());
#endif
#endif
	}
	uint16_t duration;
	duration = *(reinterpret_cast<const uint16_t*>(e.data()));
	_seq.reset();
	_seq.append(new EvtCallbackIntBool(0,        0, set_pin, _pin, RELAY_ON));
	_seq.append(new EvtCallbackIntBool(duration, 0, set_pin, _pin, RELAY_OFF));
#ifdef DESKTOP
    std::cerr << "RelayReceiver::handle starting duration=" << duration << std::endl;
#else
#ifdef DEBUG
	Serial.print(F("RelayReceiver::handle starting duration="));
	Serial.println(duration);
#endif
#endif
	_seq.start(1);
#ifndef DESKTOP
	digitalWrite(_pin, RELAY_ON);
#endif
}

void RelayReceiver::tick()
{
	_seq.tick();
}


