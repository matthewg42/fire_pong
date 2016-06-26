#include <EventBuffer.h>
#include <Arduino.h>
#include <fp_event.h>

EventBuffer::EventBuffer(callback_function cb)
{
	_callback = cb;
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
}

void EventBuffer::tick () {
	if (Serial.available() > 0) {
		_buf[_ptr] = Serial.read();
		switch(_ptr++) {
		case 0:
			if (_buf[0] != 'f') {
				reset();
			} else {
				_last_packet_start = millis();
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
				fp_event e(_buf);
				_callback(e);
                reset();
            }
		}
	}
}

