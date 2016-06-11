#include "Seq.h"
#include <Arduino.h>

Seq::Seq()
{
	for (int i=0; i<MAX_SEQ_SIZE; i++) {
		_events[i] = NULL;
	}
	Serial.println(F("Seq::Seq()"));
}

Seq::~Seq()
{
	Serial.println(F("Seq::~Seq GNDN"));
}

void Seq::append(Evt *e) {
	for (int i=0; i<MAX_SEQ_SIZE; i++) {
		if (_events[i] == NULL) {
			Serial.println(F("Seq::appended"));
			_events[i] = e;
			return;
		}
	}
	Serial.println(F("Seq::append no room"));
}

void Seq::start(int activations)
{
	Serial.println(F("Seq::Seq()"));
	for (int i=0; i<MAX_SEQ_SIZE; i++) {
		if (_events[i] != NULL) {
			_events[i]->start(activations);
		}
	}
}

void Seq::tick()
{
	for (int i=0; i<MAX_SEQ_SIZE; i++) {
		if (_events[i] != NULL) {
			_events[i]->tick();
		}
	}
}

