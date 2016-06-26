#pragma once

#include <fp_event.h>

class EventReceiver {
public:
	EventReceiver(fp_id_t id);
	~EventReceiver();

	// called in setup to set pin modes and the like
	virtual void setup() {;}
	// must implement this for subclasses
	virtual void handle(const fp_event& e) = 0;
	// may over-ride this if you want your receiver to
	// do something periodically
	virtual void tick() {;}

	virtual bool want(const fp_event& e);
protected:
	fp_id_t _id;
	
};

//! A simple receiver object which decodes the incoming 
//! event packet and then writes a text version to the
//! Serial bus
class EchoReceiver : public EventReceiver {
public:
	EchoReceiver(fp_id_t id);
	~EchoReceiver();

	virtual void handle(const fp_event& e);

};

