#include "Heartbeat.h"
#ifdef DESKTOP
#include <iostream>
#else
#include <Arduino.h>
#endif

Heartbeat::Heartbeat(int pin) :
    _mode(Heartbeat::Normal),
	_pin(pin),
    _pinState(true),
    _lastStateFlip(0),
    _onTime(0),
    _offTime(0)
{
}

Heartbeat::~Heartbeat()
{
}

void Heartbeat::setup()
{
#ifndef DESKTOP
    pinMode(_pin, OUTPUT);
#endif
	setMode(_mode);
}

Heartbeat::Mode Heartbeat::mode()
{
    return _mode;
}

void Heartbeat::setMode(Mode mode)
{
	_mode = mode;
	switch (_mode) {
	case Normal:
        _onTime = ON_MS_NORMAL;
        _offTime = OFF_MS_NORMAL;
		break;
	case Quick:
        _onTime = ON_MS_QUICK;
        _offTime = OFF_MS_QUICK;
		break;
	case Slow:
        _onTime = ON_MS_SLOW;
        _offTime = OFF_MS_SLOW;
		break;
	case Slower:
        _onTime = ON_MS_SLOWER;
        _offTime = OFF_MS_SLOWER;
		break;
	}
}

void Heartbeat::tick()
{
#ifdef DESKTOP
    return;
#else
    int wait = _pinState ? _onTime : _offTime;
    if (millis() - _lastStateFlip >= wait) {
        updatePin(!_pinState);
    }
#endif
}

void Heartbeat::updatePin(bool state)
{
#ifdef DESKTOP
    return;
#else
    _pinState = state;
    digitalWrite(_pin, _pinState);
    _lastStateFlip = millis();
#endif
}


