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

//! A simple receiver that controls a single relay. 
//! data : uint16_t duration in ms for relay to be activated
class RelayReceiver : public EventReceiver {
public:
    RelayReceiver(fp_id_t id, uint8_t pin);
    ~RelayReceiver();

	virtual void setup();
    virtual void handle(const FpEvent& e);
	virtual void tick();
	virtual bool want(const FpEvent& e);

private:
	uint8_t _pin;
	Seq _seq;
};

