#include <EventBuffer.h>
#ifdef DESKTOP
#include <iostream>
#else
#include <Arduino.h>
#endif
#include <FpEvent.h>

#ifdef DESKTOP
EventBuffer::EventBuffer(callback_function cb, Heartbeat* heartbeat)
{
}

int EventBuffer::wait_serial_clear() {
    return 0;
}

void EventBuffer::reset() {
    return;
}

void EventBuffer::tick () {
    return;
}

void EventBuffer::setHeartbeat(Heartbeat::Mode mode)
{
    return;
}

#else

EventBuffer::EventBuffer(callback_function cb, Heartbeat* heartbeat)
{
	_callback = cb;
    _heartbeat = heartbeat;
    _halted = false;
	this->reset();
}

int EventBuffer::wait_serial_clear() {
    int count = 0;
    int start = millis();
    while (millis()-start < SERIAL_CLEAR_MS) {
        if (Serial.available()) {
            Serial.read();
            count++;
            start = millis();
        }
    }
    return count;
}

void EventBuffer::reset() {
	_ptr = 0;
    _packet_length = 0;
    if (!_halted) {
        setHeartbeat(WAITING);
    }
}

void EventBuffer::tick () {
    if (millis() > _packet_timeout) {
        reset();
    }

	if (Serial.available() > 0) {
		_buf[_ptr] = Serial.read();
		switch(_ptr++) {
		case 0:
			if (_buf[0] != 'f') {
				reset();
			} else {
				_last_packet_start = millis();
                _packet_timeout = _last_packet_start + PACKET_TIMEOUT_MS;
			}
			break;
		case 1:
			if (_buf[1] != 'P') {
				reset();
			}
			break;
        case FP_SERIAL_LENGTH_OFFSET+sizeof(fp_length_t)-1:
            _packet_length = *(reinterpret_cast<fp_length_t*>(_buf+FP_SERIAL_LENGTH_OFFSET));
            if (_packet_length > FP_SERIAL_BUF_LEN || _packet_length < FP_MINIMUM_PACKET_LEN) {
                reset();
            }
            break;
        default:
            if (_ptr >= _packet_length) {
				FpEvent e(_buf);
                if (e.is_valid()) {
#ifdef DEBUG
                    Serial.print(F("Received VALID event:"));
                    e.dump();
#endif
                    if (_halted) {
                        // Only respond to RESET
                        if (e.type() == FP_EVENT_RESET) {
#ifdef DEBUG
                            Serial.println(F("HALTED -> RESET"));
#endif
                            _halted = false;
                            setHeartbeat(WAITING);
                        }
                        else {
#ifdef DEBUG
                            Serial.println(F("HALTED, not processing event"));
#endif
                        }
                    }
                    else if (e.type() == FP_EVENT_HALT) {
#ifdef DEBUG
                        Serial.println(F("Event was a HALT - HALTING"));
#endif
                        _halted = true;
                        setHeartbeat(HALTED);
                    }
                    else {
#ifdef DEBUG
                        Serial.print(F("Sending event to callback: "));
                        Serial.println((unsigned long)_callback, HEX);
#endif
                        _callback(e);
                    }
                }
                else {
#ifdef DEBUG
                    Serial.print(F("Invalid packet: "));
                    e.dump();
#endif
                }
                reset();
            }
		}
	}

    if (_ptr > 0 && !_halted) {
        setHeartbeat(RECEIVING);
    }
}

void EventBuffer::setHeartbeat(Heartbeat::Mode mode)
{
    if (_heartbeat) {
        _heartbeat->setMode(mode);
    }
}

#endif // DESKTOP

