#pragma once

#include <Arduino.h>
#include <EventReceiver.h>
#include <Seq.h>

#define RELAY_ON        LOW
#define RELAY_OFF       HIGH

//! Large puffer controller - controls a single large puffer
//! data : uint16_t duration in ms for relay to be activated
class LargePufferReceiver : public EventReceiver {
public:
    LargePufferReceiver(fp_id_t id, uint8_t solenoid_pin);
    ~LargePufferReceiver();

	virtual void setup();
    virtual void handle(const FpEvent& e);
	virtual void tick();
	virtual bool want(const FpEvent& e);

private:
	uint8_t _solenoid_pin;
	Seq _seq;
};

