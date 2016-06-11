#include "Evt.h"
#include "Seq.h"

void switch_relay(int id, bool on) {
    Serial.print(F("Switching relay #"));
    Serial.print(id);
    Serial.println(on ? F(" on") : F(" off"));
}

Seq puff1;

void setup()
{
    Serial.begin(115200);
    puff1.append(new EvtCallbackIntBool(0,    0, switch_relay, 0, true));
    puff1.append(new EvtCallbackIntBool(100,  0, switch_relay, 1, true));
    puff1.append(new EvtCallbackIntBool(113,  0, switch_relay, 1, false));
    puff1.append(new EvtCallbackIntBool(313,  0, switch_relay, 1, true));
    puff1.append(new EvtCallbackIntBool(463,  0, switch_relay, 1, false));
    puff1.append(new EvtCallbackIntBool(763,  0, switch_relay, 0, false));
    puff1.start(1);
    Serial.println(F("setup end"));
}

void loop()
{
    puff1.tick();
}


