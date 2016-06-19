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

#include "fp_event.h"
#include "crc8.h"
#include "string.h"

static uint8_t fp_crc_buf[8];

// buf must be at least 7 bytes, pre-allocated...
void fp_prepare_buf(t_PufferEvent* e)
{
	memcpy(&fp_crc_buf[0], &(e->id_set), 4);
	memcpy(&fp_crc_buf[4], &(e->type),   1);
	memcpy(&fp_crc_buf[5], &(e->type),   2);
}
   
void fp_event_set_checksum(t_PufferEvent* e)
{
	fp_prepare_buf(e);
	e->checksum = crc8(fp_crc_buf, 7);
}

int fp_event_validate(t_PufferEvent* e)
{
	fp_prepare_buf(e);
	uint8_t ck = crc8(fp_crc_buf, 7);
	return ck == e->checksum;
}

