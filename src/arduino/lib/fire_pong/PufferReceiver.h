#pragma once

#include <EventReceiver.h>
#include <Seq.h>

#ifdef DESKTOP
#define LOW             0
#define HIGH            1
#else
#include <Arduino.h>
#endif

#define RELAY_ON        LOW
#define RELAY_OFF       HIGH

//! Controls an individual puffer by solenoid valve (e.g. large puffer)
//! data : uint16_t duration in ms for main puff (100 is a typical value)
class PufferReceiver : public EventReceiver {
public:
    PufferReceiver(fp_id_t id, uint8_t solenoid_pin);
    ~PufferReceiver();

	virtual void setup();
    virtual void handle(const FpEvent& e);
	virtual void tick();
	virtual bool want(const FpEvent& e);

    static void set_pin(int pin, bool state);
protected:
	Seq _seq;

	uint8_t _solenoid_pin;

};

