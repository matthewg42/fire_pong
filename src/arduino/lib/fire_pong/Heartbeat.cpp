#include "Heartbeat.h"
#include <Arduino.h>

Heartbeat::Heartbeat(int pin) :
    _mode(Heartbeat::Waiting),
	_pin(pin)
{
}

Heartbeat::~Heartbeat()
{
}

void Heartbeat::setup()
{
    pinMode(_pin, OUTPUT);
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
	case Waiting:
        _onTime = ON_MS_WAITING;
        _offTime = OFF_MS_WAITING;
		break;
	case Receiving:
        _onTime = ON_MS_RECEIVING;
        _offTime = OFF_MS_RECEIVING;
		break;
	case Halted:
        _onTime = ON_MS_HALTED;
        _offTime = OFF_MS_HALTED;
		break;
	case Error:
        _onTime = ON_MS_ERROR;
        _offTime = OFF_MS_ERROR;
		break;
	}
    updatePin(false);
}

void Heartbeat::tick()
{
    int wait = _pinState ? _onTime : _offTime;
    if (millis() - _lastStateFlip >= wait) {
        updatePin(!_pinState);
    }
}

void Heartbeat::updatePin(bool on)
{
    _pinState = on;
    digitalWrite(_pin, _pinState);
    _lastStateFlip = millis();
}


