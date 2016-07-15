#pragma once

#include <PufferReceiver.h>
#include <Seq.h>

//! Controls an individual small puffer (i.e. sparker and solenoid relays)
//! data : uint16_t duration in ms for main puff (100 is a typical value)
class SmallPufferReceiver : public PufferReceiver {
public:
    SmallPufferReceiver(fp_id_t id, uint8_t solenoid_pin, uint8_t sparker_pin);
    ~SmallPufferReceiver();

	virtual void setup();
    virtual void handle(const FpEvent& e);
	virtual void tick();
	virtual bool want(const FpEvent& e);

protected:
	uint8_t _sparker_pin;
};

