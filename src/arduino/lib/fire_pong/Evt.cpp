#include "Evt.h"
#ifndef DESKTOP
#include <Arduino.h>
#endif

Evt::Evt(unsigned long offset, int activations) : 
	_offset(offset),
	_activations(activations)
{
	if (_activations != 0)
		start(_activations);
}

Evt::~Evt()
{
}

void Evt::tick()
{
#ifndef DESKTOP
	if (_activations != 0) {
		if (millis() >= _millis) {
			fn();
			if (_activations > 0) {
				_activations--;
			}
			if (_activations != 0) {
				start(_activations);
			}
		}
	}
#endif
}

void Evt::start(int activations)
{
#ifndef DESKTOP
	_activations = activations;
	_millis = millis() + _offset;
#endif
}

void Evt::fn()
{
#ifndef DESKTOP
	Serial.print(F("Evt@"));
	Serial.print((unsigned long)this);
	Serial.print(F(" t="));
	Serial.print(_millis);
	Serial.print(F(" act="));
	Serial.println(_activations);
#endif
}

EvtCallback::EvtCallback(unsigned long offset, int activations, void (*callback)()) :
	Evt(offset, activations),
	_callback(callback)
{
}

EvtCallback::~EvtCallback()
{
}

void EvtCallback::fn()
{
	_callback();
}

EvtCallbackIntBool::EvtCallbackIntBool(unsigned long offset, int activations, void (*callback)(int,bool), int iarg, bool barg) :
	Evt(offset, activations),
	_callback(callback),
	_iarg(iarg),
	_barg(barg)
{
}

EvtCallbackIntBool::~EvtCallbackIntBool()
{
}

void EvtCallbackIntBool::fn()
{
	_callback(_iarg,_barg);
}


