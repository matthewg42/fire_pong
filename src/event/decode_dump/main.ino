#include <Arduino.h>
#include <fp_event.h>

#define PACKET_TIMEOUT_MS 100
#define LED_PIN 13

static uint8_t buf[FP_SERIAL_BUF_LEN];
static fp_length_t ptr = 0;
static fp_length_t packet_length = 0;
static unsigned long last_packet_start;

void setup() {
	Serial.begin(115200);
	pinMode(LED_PIN, OUTPUT);
	digitalWrite(LED_PIN, LOW);
	Serial.println(F("setup complete"));
}

int wait_serial_clear() {
    int count = 0;
    int start = millis();
    while (millis()-start < 30) {
        if (Serial.available()) {
            Serial.read();
            count++;
            start = millis();
        }
    }
    return count;
}

void reset_buf(const __FlashStringHelper* m) {
    if (m) {
        wait_serial_clear();
        Serial.println(m);
    }
	ptr = 0;
    packet_length = 0;
}

void handle_packet()
{
    // wait for a break in transmission...
    int count = wait_serial_clear();
    if (count>0) {
        Serial.print(F("After packet end I received had another "));
        Serial.print(count);
        Serial.print(F(" bytes of data..."));
    }
    fp_event e(buf);
    if (e.is_valid()) {
        Serial.println("packet OK");
    } else {
        Serial.print("INVALID: ");
        e.dump();
    }

    
}

void loop () {
	if (Serial.available() > 0) {
		buf[ptr] = Serial.read();
		switch(ptr++) {
		case 0:
			if (buf[0] != 'f') {
				reset_buf(F("\r\nbad magic 1"));
			} else {
				last_packet_start = millis();
			}
			break;
		case 1:
			if (buf[1] != 'P') {
				reset_buf(F("\r\nbad magic 2"));
			}
			break;
        case FP_SERIAL_LENGTH_OFFSET+sizeof(fp_length_t)-1:
            packet_length = *(reinterpret_cast<fp_length_t*>(buf+FP_SERIAL_LENGTH_OFFSET));
            if (packet_length > FP_SERIAL_BUF_LEN || packet_length < FP_MINIMUM_PACKET_LEN) {
                reset_buf(F("Invalid packet length"));
            }
            break;
        default:
            if (ptr >= packet_length) {
                handle_packet();
                reset_buf(0);
            }
		}
	}
}

