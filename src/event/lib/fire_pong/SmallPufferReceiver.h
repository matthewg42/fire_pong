#pragma once

#include <Arduino.h>
#include <EventReceiver.h>
#include <Seq.h>

#define RELAY_ON        LOW
#define RELAY_OFF       HIGH

//! A simple receiver that controls a single relay. 
//! data : uint16_t duration in ms for relay to be activated
class SmallPufferReceiver : public EventReceiver {
public:
    SmallPufferReceiver(fp_id_t id, uint8_t sparker_pin, uint8_t solenoid_pin);
    ~SmallPufferReceiver();

	virtual void setup();
    virtual void handle(const FpEvent& e);
	virtual void tick();
	virtual bool want(const FpEvent& e);

private:
	uint8_t _sparker_pin;
	uint8_t _solenoid_pin;
	Seq _seq;
};

