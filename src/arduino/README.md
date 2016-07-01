To use the Makefile instead of the Arduino GUI, clone into /opt/arduino-mk this git repo:

    https://github.com/sudar/Arduino-Makefile

Or put it somewhere else and set the path to the Arduino.mk file in *arduino_inc.mk* in this directory.

Also, copy the lib/fire_pong directory to your arduino libraries directory (or link it).

To build the program in one of the sub-directories, change into that directory and use the command *make*.  To upload to an Arduino, use *make upload*.
