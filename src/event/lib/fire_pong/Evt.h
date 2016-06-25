#pragma once

#define RECURRING_EVT -1

class Evt {
public:
	//! Create an Evt. 
	//! @offset in ms from start time
	//! @activations: 0=inactive; +ve=number of activations or RECURRING_EVT for no end
	Evt(unsigned long offset, int activations);
	~Evt();

	//! called periodically in loop() to test to see if Evt is due, and call it if necessary
	virtual void tick();

	//! call this to activate the Evt and start the event timer
	virtual void start(int activations);

protected:
	//! the thing you want to happen
	virtual void fn();
	unsigned long _offset;
	int _activations;
	unsigned long _millis;

};

class EvtCallback : public Evt {
public:
	EvtCallback(unsigned long offset, int activations, void (*callback)());
	~EvtCallback();

protected:
	virtual void fn();
	void (*_callback)();

};

class EvtCallbackIntBool : public Evt {
public:
	EvtCallbackIntBool(unsigned long offset, int activations, void (*callback)(int,bool), int iarg, bool barg);
	~EvtCallbackIntBool();

protected:
	virtual void fn();
	void (*_callback)(int,bool);
	int _iarg;
	bool _barg;

};
