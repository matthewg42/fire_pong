#include <SmallPufferReceiver.h>

void set_pin(int pin, bool state) {
    Serial.print(F("Relay PIN "));
    Serial.print(pin);
    Serial.print(F(" : "));
    Serial.println(state==RELAY_ON ? F("ON") : F("OFF"));
    digitalWrite(pin, state);
}

SmallPufferReceiver::SmallPufferReceiver(fp_id_t id, uint8_t sparker_pin, uint8_t solenoid_pin) :
	EventReceiver(id),
	_sparker_pin(sparker_pin),
	_solenoid_pin(solenoid_pin)
{
}

SmallPufferReceiver::~SmallPufferReceiver()
{
	digitalWrite(_sparker_pin, RELAY_OFF);
	digitalWrite(_solenoid_pin, RELAY_OFF);
}

bool SmallPufferReceiver::want(const FpEvent& e)
{
	return e.type() == FP_EVENT_PUFF;
}

void SmallPufferReceiver::setup()
{
	pinMode(_sparker_pin, OUTPUT);
	digitalWrite(_sparker_pin, RELAY_OFF);
	pinMode(_solenoid_pin, OUTPUT);
	digitalWrite(_solenoid_pin, RELAY_OFF);
}

void SmallPufferReceiver::handle(const FpEvent& e)
{
	if (e.data_length() != sizeof(uint16_t)) {
#ifdef DEBUG
		Serial.print(F("SmallPufferReceiver::handle wrong data length: "));
		Serial.println(e.data_length());
#endif
		return;
	}
	uint16_t duration;
	duration = *(reinterpret_cast<const uint16_t*>(e.data()));
	_seq.reset();
	uint16_t t = 0;
	_seq.append(new EvtCallbackIntBool(t, 0, set_pin, _sparker_pin,  RELAY_ON));   t += 70;
	_seq.append(new EvtCallbackIntBool(t, 0, set_pin, _solenoid_pin, RELAY_ON));   t += 13;
	_seq.append(new EvtCallbackIntBool(t, 0, set_pin, _solenoid_pin, RELAY_OFF));  t += 150;
	_seq.append(new EvtCallbackIntBool(t, 0, set_pin, _solenoid_pin, RELAY_ON));   t += duration;
	_seq.append(new EvtCallbackIntBool(t, 0, set_pin, _solenoid_pin, RELAY_OFF));  t += 100;
	_seq.append(new EvtCallbackIntBool(t, 0, set_pin, _sparker_pin,  RELAY_OFF));  
	_seq.start(1);
}

void SmallPufferReceiver::tick()
{
	_seq.tick();
}

