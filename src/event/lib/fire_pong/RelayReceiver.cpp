#include <RelayReceiver.h>

void set_pin(int pin, bool state) {
    Serial.print(F("Relay PIN "));
    Serial.print(pin);
    Serial.print(F(" : "));
    Serial.println(state==RELAY_ON ? F("ON") : F("OFF"));
    digitalWrite(pin, state);
}

RelayReceiver::RelayReceiver(fp_id_t id, uint8_t pin) :
	EventReceiver(id),
	_pin(pin)
{
}

RelayReceiver::~RelayReceiver()
{
	digitalWrite(_pin, RELAY_OFF);
}

bool RelayReceiver::want(const fp_event& e)
{
	return e.type() == FP_EVENT_RELAY;
}

void RelayReceiver::setup()
{
	pinMode(_pin, OUTPUT);
	digitalWrite(_pin, RELAY_OFF);
}

void RelayReceiver::handle(const fp_event& e)
{
	if (e.data_length() != sizeof(uint16_t)) {
		Serial.print(F("RelayReceiver::handle wrong data length: "));
		Serial.println(e.data_length());
	}
	uint16_t duration;
	duration = *(reinterpret_cast<const uint16_t*>(e.data()));
	_seq.reset();
	_seq.append(new EvtCallbackIntBool(0,        0, set_pin, _pin, RELAY_ON));
	_seq.append(new EvtCallbackIntBool(duration, 0, set_pin, _pin, RELAY_OFF));
	Serial.print(F("RelayReceiver::handle starting duration="));
	Serial.println(duration);
	_seq.start(1);
	digitalWrite(_pin, RELAY_ON);
}

void RelayReceiver::tick()
{
	_seq.tick();
}


