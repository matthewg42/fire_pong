/**
 * Adapted from the WiiAccelerometer example from http://sudarmuthu.com/arduino/wiiremote
 * Requires the USB Host Shield Library to be installed in the arduino library directory
 * 
 */

/**
 * Copyright 2016  Mouse        (email : mousefad@gmail.com)
 * Copyright 2011  Sudar Muthu  (email : sudar@sudarmuthu.com)
 * ----------------------------------------------------------------------------
 * "THE BEER-WARE LICENSE" (Revision 42):
 * <sudar@sudarmuthu.com> wrote this file. As long as you retain this notice you
 * can do whatever you want with this stuff. If we meet some day, and you think
 * this stuff is worth it, you can buy me a beer or coffee in return - Sudar
 * ----------------------------------------------------------------------------
 * Seconded - Mouse <:3_)---
 */

#include <Usb.h>
#include <stdio.h>
#include <string.h>
#include "config.h"
#include "WiiRemote.h"

// Edit config.h to add your Bluetooth Dongle ID and WiiMote ID

#define BUFLEN 160
#define SWIPE_THESHOLD 2.5
#define RESWIPE_MILLIS 1500

WiiRemote wiiremote;
static char buf[BUFLEN];
static float prev_yacc = 1.0;
static unsigned long last_swipe = 0;

void myapp(void);

void setup() {
    Serial.begin(115200);

    // Wait a moment for BT devices to power up
    delay(500);
    wiiremote.init();
    wiiremote.setBDAddress(WIIMOTE_ADDR, 6);
    wiiremote.setBDAddressMode(BD_ADDR_FIXED);
    Serial.println(F("Setup complete"));
}

void loop() {
    wiiremote.task(&myapp);
}

int abar(char* ptr, float value)
{
    char* p = ptr;
    for (float i=-2; i<=2; i+=0.2) {
        value > i ? *p = '#' : *p = '-';
        p++;
    }
    return p - ptr;
}

// Call back which is executed by wiiremote.task() method
void myapp(void) {
    int len = 0;
    float acc = abs(wiiremote.Report.Accel.X) + abs(wiiremote.Report.Accel.Y) + abs(wiiremote.Report.Accel.Z);
    memset(buf, 0, BUFLEN);
    len += snprintf(buf+len, BUFLEN-len, "x:");
    len += abar(buf+len, wiiremote.Report.Accel.X);
    len += snprintf(buf+len, BUFLEN-len, " y:");
    len += abar(buf+len, wiiremote.Report.Accel.Y);
    len += snprintf(buf+len, BUFLEN-len, " z:");
    len += abar(buf+len, wiiremote.Report.Accel.Z);
    len += snprintf(buf+len, BUFLEN-len, " acc=");
    dtostrf(acc , 5, 1, buf+len);
    len += 5;
    if (prev_yacc > SWIPE_THESHOLD && prev_yacc > wiiremote.Report.Accel.Y && millis() - last_swipe > RESWIPE_MILLIS) {
        len += snprintf(buf+len, BUFLEN-len, " SWIPE" );
        last_swipe = millis();
    }
    prev_yacc = wiiremote.Report.Accel.Y;
    Serial.println(buf);
}

