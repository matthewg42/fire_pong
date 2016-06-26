#pragma once

#include <fp_event.h>

class EventReceiver {
public:
	EventReceiver(fp_id_t id);
	~EventReceiver();

	// must implement this for subclasses - it is called from process_event
	virtual void handle(const fp_event& e) = 0;
	// Used to determine what events will be passed to handle()
	virtual bool want(const fp_event& e) {return true;}

	// called in setup to set pin modes and the like
	virtual void setup() {;}
	// This should be called in client code when an event is read
	virtual void process_event(const fp_event& e);
	// may over-ride this if you want your receiver to
	// do something periodically
	virtual void tick() {;}
protected:
	fp_id_t _id;
	bool _halted;
	
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

