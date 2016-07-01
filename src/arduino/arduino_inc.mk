
# Set this to the boards.txt file installed by the Arduino IDE installer
BOARDS_TXT := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))boards.txt

# Set this for Arduino.mk from the repo https://github.com/sudar/Arduino-Makefile.git
include /opt/arduino-mk/Arduino.mk

