#include <DisplayReceiver.h>
#include <string.h>

DisplayReceiver::DisplayReceiver(fp_id_t id, display_callback callback) :
    EventReceiver(id)
{
    _callback = callback;
}

DisplayReceiver:: ~DisplayReceiver()
{
}

void DisplayReceiver::setup()
{
    clear();
}

void DisplayReceiver::clear()
{
    memset(_buf, 0, sizeof(char) * (FP_MAX_DATA_LEN+1));
}

bool DisplayReceiver::want(const FpEvent& e)
{
    return e.type() == FP_EVENT_DISPLAY;
}

void DisplayReceiver::handle(const FpEvent& e)
{
    switch (e.type()) {
    case FP_EVENT_DISPLAY:
        clear();
        for(int i=0; i<e.data_length(); i++) {
            _buf[i] = (char)(e.data()[i]);
        }
#ifdef DEBUG
#ifndef DESKTOP
        Serial.print(F("DisplayReceiver::handle got display: "));
        Serial.println(_buf);
#endif
#endif
        _callback(_buf);
        break;
    }
}

void DisplayReceiver::tick(void)
{
}

