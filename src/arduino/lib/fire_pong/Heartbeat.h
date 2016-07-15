#pragma once

#define ON_MS_WAITING		50
#define OFF_MS_WAITING		500
#define ON_MS_RECEIVING		25
#define OFF_MS_RECEIVING	25
#define ON_MS_HALTED		1000
#define OFF_MS_HALTED		150
#define ON_MS_ERROR			1000
#define OFF_MS_ERROR		1000

class Heartbeat {
public:
	enum Mode {
		Waiting=0,
		Receiving,
		Halted,
		Error
	};

	Heartbeat(int pin);
	~Heartbeat();

    void setup();
    Mode mode();
	void setMode(Mode mode);
	void tick();

private:
    void updatePin(bool on);

	Mode _mode;
	int _pin;
	bool _pinState;
	unsigned long _lastStateFlip;
	int _onTime;
	int _offTime;

};
