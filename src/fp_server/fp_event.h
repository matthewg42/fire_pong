/*
    This file is part of Fire Pong Firmware

    Fire Pong Firmware is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

*/

#pragma once

#include <stdint.h>

#define FP_EVENT_PUFF 1
   
typedef struct PufferEvent {
   uint32_t id_set;
   uint8_t  type;
   uint16_t duration;
   uint8_t checksum;
} t_PufferEvent;

void fp_event_set_checksum(t_PufferEvent* e);
int fp_event_validate(t_PufferEvent* e);

