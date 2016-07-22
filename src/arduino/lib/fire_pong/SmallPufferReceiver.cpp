#include <SmallPufferReceiver.h>

#ifdef DESKTOP
#include <iostream>
#endif

SmallPufferReceiver::SmallPufferReceiver(fp_id_t id, uint8_t solenoid_pin, uint8_t sparker_pin) :
    PufferReceiver(id, solenoid_pin),
	_sparker_pin(sparker_pin),
    _sparker_timeout(0)
{
}

SmallPufferReceiver::~SmallPufferReceiver()
{
#ifndef DESKTOP
	digitalWrite(_sparker_pin, RELAY_OFF);
#endif
}

bool SmallPufferReceiver::want(const FpEvent& e)
{
	return e.type() == FP_EVENT_PUFF || e.type() == FP_EVENT_ALTPUFF || e.type() == FP_EVENT_SPARK || e.type() == FP_EVENT_SOLENOID;
}

void SmallPufferReceiver::setup()
{
    PufferReceiver::setup();
#ifndef DESKTOP
	pinMode(_sparker_pin, OUTPUT);
	digitalWrite(_sparker_pin, RELAY_OFF);
#endif
}

void SmallPufferReceiver::handle(const FpEvent& e)
{
	uint16_t duration;
	uint16_t t = 0;
	uint8_t state;
    
#ifdef DESKTOP 
    std::cerr << "SmallPufferReceiver::handle: ";
    e.dump();
#else
#ifdef DEBUG
    Serial.print(F("SmallPufferReceiver::handle: "));
    e.dump();
#endif
#endif

	switch (e.type()) {
	case FP_EVENT_PUFF:
		if (e.data_length() != sizeof(uint16_t)) {
#ifdef DESKTOP 
            std::cerr << "SmallPufferReceiver::handle PUFF wrong data length: " << e.data_length() << std::endl;
#else
#ifdef DEBUG
			Serial.print(F("SmallPufferReceiver::handle PUFF wrong data length: "));
			Serial.println(e.data_length());
#endif
#endif
			return;
		}
		duration = *(reinterpret_cast<const uint16_t*>(e.data()));
		_seq.reset();
		_seq.append(new EvtCallbackIntBool(t, 0, set_pin, _sparker_pin,  RELAY_ON));   t += 100;
		_seq.append(new EvtCallbackIntBool(t, 0, set_pin, _solenoid_pin, RELAY_ON));   t += 13;
		_seq.append(new EvtCallbackIntBool(t, 0, set_pin, _solenoid_pin, RELAY_OFF));  t += 200;
		_seq.append(new EvtCallbackIntBool(t, 0, set_pin, _solenoid_pin, RELAY_ON));   t += duration;
		_seq.append(new EvtCallbackIntBool(t, 0, set_pin, _solenoid_pin, RELAY_OFF));  t += 100;
		_seq.append(new EvtCallbackIntBool(t, 0, set_pin, _sparker_pin,  RELAY_OFF));  
		_seq.start(1);
		break;
	case FP_EVENT_ALTPUFF:
		if (e.data_length() != sizeof(uint16_t)) {
#ifdef DESKTOP 
            std::cerr << "SmallPufferReceiver::handle ALTPUFF wrong data length: " << e.data_length() << std::endl;
#else
#ifdef DEBUG
			Serial.print(F("SmallPufferReceiver::handle ALTPUFF wrong data length: "));
			Serial.println(e.data_length());
#endif
#endif
			return;
		}
		duration = *(reinterpret_cast<const uint16_t*>(e.data()));
		_seq.reset();
		_seq.append(new EvtCallbackIntBool(t, 0, set_pin, _sparker_pin,  RELAY_ON));   t += 100;
		_seq.append(new EvtCallbackIntBool(t, 0, set_pin, _solenoid_pin, RELAY_ON));   t += duration;
		_seq.append(new EvtCallbackIntBool(t, 0, set_pin, _solenoid_pin, RELAY_OFF));  t += 100;
		_seq.append(new EvtCallbackIntBool(t, 0, set_pin, _sparker_pin,  RELAY_OFF));  
		_seq.start(1);
		break;
	case FP_EVENT_SOLENOID:
		if (e.data_length() != sizeof(uint8_t)) {
#ifdef DESKTOP 
            std::cerr << "SmallPufferReceiver::handle SOLENOID wrong data length: " << e.data_length() << std::endl;
#else
#ifdef DEBUG
			Serial.print(F("SmallPufferReceiver::handle SOLENOID wrong data length: "));
			Serial.println(e.data_length());
#endif
#endif
			return;
		}
		state = *(reinterpret_cast<const uint8_t*>(e.data()));
		set_pin(_solenoid_pin, state ? RELAY_ON : RELAY_OFF);
        _solenoid_timeout = state ? millis() + MAX_OPEN_MILLIS : 0;
		break;
	case FP_EVENT_SPARK:
		if (e.data_length() != sizeof(uint8_t)) {
#ifdef DESKTOP 
            std::cerr << "SmallPufferReceiver::handle SPARK wrong data length: " << e.data_length() << std::endl;
#else
#ifdef DEBUG
			Serial.print(F("SmallPufferReceiver::handle SPARK wrong data length: "));
			Serial.println(e.data_length());
#endif
#endif
			return;
		}
		state = *(reinterpret_cast<const uint8_t*>(e.data()));
		set_pin(_sparker_pin, state ? RELAY_ON : RELAY_OFF);
        _sparker_timeout = state ? millis() + MAX_SPARK_MILLIS : 0;
		break;
	}
}

void SmallPufferReceiver::tick()
{
    // Implement timeout - make sure solenoid is off
    if (_solenoid_timeout < millis() && _solenoid_timeout != 0) {
		set_pin(_solenoid_pin, RELAY_OFF);
        _solenoid_timeout = 0;
    }
    
    // Implement timeout - make sure spark is off
    if (_sparker_timeout < millis() && _sparker_timeout != 0) {
		set_pin(_sparker_pin, RELAY_OFF);
        _sparker_timeout = 0;
    }
    
	_seq.tick();
}


