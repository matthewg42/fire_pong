#pragma once

#include "Evt.h"

#define MAX_SEQ_SIZE 10

class Seq {
public:
	Seq();
	~Seq();
	void append(Evt *e);
	void start(int activations);
	void tick();
	void reset();

private:
	Evt* _events[MAX_SEQ_SIZE];

};
