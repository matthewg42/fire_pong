#pragma once

#include <stdint.h>

// Set this to your WiiMote Bluetooth device ID 
// To find this (on Linux systems)
// 0. Install hciconfig and hcitool
// 1. Press the connection reset button in the battery compartment of your WiiMote
// 2. Run "hcitool --iac=liac"
static uint8_t WIIMOTE1_ADDR[6] = {0x00, 0x21, 0xbd, 0x02, 0x30, 0x9b};
static uint8_t WIIMOTE2_ADDR[6] = {0x00, 0x1e, 0x35, 0x27, 0x25, 0xa8};

// Use lsusb to find the VendorID and ProductID of your Bluetooth dongle
// Example line of output:
//
#define BT_USB_VENDOR_ID 0x0a12
#define BT_USB_PRODUCT_ID 0x0001


