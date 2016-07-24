#include <PufferReceiver.h>

#ifdef DESKTOP
#include <iostream>
#endif

PufferReceiver::PufferReceiver(fp_id_t id, uint8_t solenoid_pin) :
	EventReceiver(id),
	_solenoid_pin(solenoid_pin),
    _solenoid_timeout(0)
{
}

PufferReceiver::~PufferReceiver()
{
#ifndef DESKTOP
	digitalWrite(_solenoid_pin, RELAY_OFF);
#endif
}

bool PufferReceiver::want(const FpEvent& e)
{
	return e.type() == FP_EVENT_PUFF || e.type() == FP_EVENT_ALTPUFF || e.type() == FP_EVENT_SOLENOID;
}

void PufferReceiver::setup()
{
#ifndef DESKTOP
	pinMode(_solenoid_pin, OUTPUT);
	digitalWrite(_solenoid_pin, RELAY_OFF);
#endif
}

void PufferReceiver::handle(const FpEvent& e)
{
	uint16_t duration;
	uint16_t t = 0;
	uint8_t state;
	switch (e.type()) {
    case FP_EVENT_ALTPUFF:
	case FP_EVENT_PUFF:
		if (e.data_length() != sizeof(uint16_t)) {
#ifdef DESKTOP 
            std::cerr << "PufferReceiver::handle PUFF wrong data length: " << e.data_length() << std::endl;
#else
#ifdef DEBUG
			Serial.print(F("PufferReceiver::handle PUFF wrong data length: "));
			Serial.println(e.data_length());
#endif
#endif
			return;
		}
		duration = *(reinterpret_cast<const uint16_t*>(e.data()));
		_seq.reset();
		_seq.append(new EvtCallbackIntBool(t, 0, set_pin, _solenoid_pin, RELAY_ON));   
        t += duration;
		_seq.append(new EvtCallbackIntBool(t, 0, set_pin, _solenoid_pin, RELAY_OFF)); 
		_seq.start(1);
		break;
	case FP_EVENT_SOLENOID:
		if (e.data_length() != sizeof(uint8_t)) {
#ifdef DESKTOP 
            std::cerr << "PufferReceiver::handle SOLENOID wrong data length: " << e.data_length() << std::endl;
#else
#ifdef DEBUG
			Serial.print(F("PufferReceiver::handle SOLENOID wrong data length: "));
			Serial.println(e.data_length());
#endif
#endif
			return;
		}
		state = *(reinterpret_cast<const uint8_t*>(e.data()));
		set_pin(_solenoid_pin, state ? RELAY_ON : RELAY_OFF);
        _solenoid_timeout = state ? millis() + MAX_OPEN_MILLIS : 0;
		break;
	}
}

void PufferReceiver::tick()
{
#ifndef DESKTOP
    // Implement timeout - make sure solenoid is off
    if (_solenoid_timeout < millis() && _solenoid_timeout != 0) {
		set_pin(_solenoid_pin, RELAY_OFF);
        _solenoid_timeout = 0;
    }
#endif
	_seq.tick();
}

void PufferReceiver::set_pin(int pin, bool state) 
{
#ifdef DESKTOP
    std::cerr << "PufferReceiver::set_pin(pin=" << pin << ", state=" 
            << (state==RELAY_ON ? "ON" : "OFF") << ")" << std::endl;
#else
#ifdef DEBUG
    Serial.print(F("PufferReceiver::set_pin(pin="));
    Serial.print(pin);
    Serial.print(F(", "));
    Serial.print(state==RELAY_ON ? F("ON") : F("OFF"));
    Serial.println(F(")"));
#endif
    digitalWrite(pin, state);
#endif
}


