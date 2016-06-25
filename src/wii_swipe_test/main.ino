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

#define BUFLEN 100
#define SWIPE_THESHOLD 2.2
#define RESWIPE_MILLIS 500

WiiRemote wiiremote1;
WiiRemote wiiremote2;
static char buf[BUFLEN];
static float prev_yacc1 = 1.0;
static float prev_yacc2 = 1.0;
static unsigned long last_swipe1 = 0;
static unsigned long last_swipe2 = 0;

void myapp1(void);
void myapp2(void);

void setup() {
    Serial.begin(19200);

    // Wait a moment for BT devices to power up
    delay(500);
    wiiremote1.init();
    wiiremote1.setBDAddress(WIIMOTE1_ADDR, 6);
    wiiremote1.setBDAddressMode(BD_ADDR_FIXED);
    wiiremote2.init();
    wiiremote2.setBDAddress(WIIMOTE2_ADDR, 6);
    wiiremote2.setBDAddressMode(BD_ADDR_FIXED);
    Serial.println(F("Setup complete"));
}

void loop() {
    wiiremote1.task(&myapp1);
    wiiremote2.task(&myapp2);
}

int abar(char* ptr, float value)
{
    char* p = ptr;
    for (float i=-2; i<=2; i+=0.4) {
        if (value == 0) {
            *p = '|';
        } else {
            value > i ? *p = '#' : *p = '-';
        }
        p++;
    }
    return p - ptr;
}

void myapp1(void) {
    Serial.println("in myapp1");
    return;
}

// Call back which is executed by wiiremote.task() method
void myapp2(void) {
    int len = 0;
    float acc = abs(wiiremote1.Report.Accel.X) + abs(wiiremote1.Report.Accel.Y) + abs(wiiremote1.Report.Accel.Z);
    memset(buf, 0, BUFLEN);
    len += snprintf(buf+len, BUFLEN-len, "P2");
    len += snprintf(buf+len, BUFLEN-len, "x:");
    len += abar(buf+len, wiiremote1.Report.Accel.X);
    len += snprintf(buf+len, BUFLEN-len, " y:");
    len += abar(buf+len, wiiremote1.Report.Accel.Y);
    len += snprintf(buf+len, BUFLEN-len, " z:");
    len += abar(buf+len, wiiremote1.Report.Accel.Z);
    len += snprintf(buf+len, BUFLEN-len, " acc=");
    dtostrf(acc , 5, 1, buf+len);
    len += 5;
    if (prev_yacc1 > SWIPE_THESHOLD && prev_yacc1 > wiiremote1.Report.Accel.Y && millis() - last_swipe1 > RESWIPE_MILLIS) {
        len += snprintf(buf+len, BUFLEN-len, " SWIPE" );
        last_swipe1 = millis();
    }
    prev_yacc1 = wiiremote1.Report.Accel.Y;
    Serial.println(buf);
}

