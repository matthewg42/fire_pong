# Specify which segment we're building here (1, 2 or 3)
SEGMENT=1

# Add -DDEBUG to have the program write debugging to serial
CPPFLAGS = -DPUFFER_SEGMENT_NUMBER=$(SEGMENT)
ARDUINO_LIBS = fire_pong
BOARD_TAG = pro5v328

include ../arduino_inc.mk

