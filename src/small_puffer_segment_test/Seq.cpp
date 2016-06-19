#include "Seq.h"
#include <Arduino.h>

Seq::Seq()
{
	for (int i=0; i<MAX_SEQ_SIZE; i++) {
		_events[i] = NULL;
	}
}

Seq::~Seq()
{
}

void Seq::append(Evt *e) {
	for (int i=0; i<MAX_SEQ_SIZE; i++) {
		if (_events[i] == NULL) {
			_events[i] = e;
			return;
		}
	}
}

void Seq::start(int activations)
{
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

