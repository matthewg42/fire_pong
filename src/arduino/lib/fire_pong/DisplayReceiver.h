#pragma once

#include <EventReceiver.h>
#include <FpEvent.h>

#ifdef DESKTOP
#include <iostream>
#else
#include <Arduino.h>
#endif

typedef void (*display_callback)(const char* message);

class DisplayReceiver : public EventReceiver {
public:

    DisplayReceiver(fp_id_t id, display_callback callback);
    ~DisplayReceiver();

	virtual void setup();
    virtual void handle(const FpEvent& e);
	virtual void tick();
	virtual bool want(const FpEvent& e);

    void clear();
    
private:
    display_callback _callback;
    char _buf[FP_MAX_DATA_LEN+1];

};

