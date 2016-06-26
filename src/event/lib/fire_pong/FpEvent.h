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

typedef uint16_t fp_magic_t;
typedef uint8_t fp_type_t;
typedef uint8_t fp_length_t;
typedef uint8_t fp_data_t;
typedef uint8_t fp_checksum_t;
typedef uint32_t fp_id_t;

#define FP_MAX_DATA_LEN   16
#define FP_EVENT_HALT     0
#define FP_EVENT_RESET    1
#define FP_EVENT_SPARK    2
#define FP_EVENT_SOLENOID 3
#define FP_EVENT_PUFF     4
#define FP_EVENT_DISPLAY  5
#define FP_EVENT_RELAY    6
#define FP_STR(x)         (reinterpret_cast<const fp_data_t*>(x))

// Magic is an unsigned short little endian, "fP", which when decoded turns
// out to be the value 0x5066.  We use a static not a #define so we can memcpy 
// from it...
static fp_magic_t FP_MAGIC=0x5066;

// Serialized packet structure:
//     000000000011111111112
//     012345678901234567890
//     MMLIIIIT[D...]CMM
// Where:
// MM    = magic
// L     = packet length in bytes (including magic)
// IIII  = id_set
// T     = type
// D     = zero or more data bytes
// C     = crc8 checksum of serialized data starting at beginning of packet upto the end of the data
// MM    = magic

#define FP_SERIAL_BUF_LEN (sizeof(fp_magic_t)+sizeof(fp_length_t)+sizeof(fp_id_t)+sizeof(fp_type_t)+(sizeof(fp_data_t)*FP_MAX_DATA_LEN)+sizeof(fp_checksum_t)+sizeof(fp_magic_t))
#define FP_MINIMUM_PACKET_LEN (sizeof(fp_magic_t)+sizeof(fp_length_t)+sizeof(fp_id_t)+sizeof(fp_type_t)+sizeof(fp_checksum_t)+sizeof(fp_magic_t))
#define FP_SERIAL_LENGTH_OFFSET (sizeof(fp_magic_t))
#define FP_SERIAL_ID_OFFSET (FP_SERIAL_LENGTH_OFFSET + sizeof(fl_length_t))
#define FP_SERIAL_TYPE_OFFSET (FP_SERIAL_ID_OFFSET + sizeof(fl_id_t))
#define FP_SERIAL_DATA_OFFSET (FP_SERIAL_TYPE_OFFSET + sizeof(fl_type_t))

class FpEvent {
public:
	// Create an empty FpEvent
	FpEvent();

	// Create an FpEvent with a specified id and type
	FpEvent(fp_id_t id_set, fp_type_t type, const fp_data_t* data=0, fp_length_t data_length=0);

	// Create an FpEvent from a buffer of serialized data 
	FpEvent(fp_data_t* buf);

	~FpEvent();

	void reset();

	// Set object up based on serialized buffer
	// Return false on error
	bool parse_serial_data(uint8_t* buf);

	// Return the checksum from a blob of serialized data
	void from_serial(uint8_t* buf);

	// Update just the payload (does not update checksum)
	// Returns true on success, else false
	bool set_payload(const fp_data_t* data, fp_length_t length);

	// Update the checksum based on the rest of the FpEvent
	fp_checksum_t calculate_checksum() const;

	// Check that the checksum which is set matches the rest of the FpEvent
	bool validate_checksum() const;

	// Check object has been set up corrctly and has a valid checksum
	bool is_valid() const;

	//! Get a serialized blob of data which encapsulates the FpEvent
	uint8_t* serialize() const;

	//! Dump to cout / Serial (depending on build)
	void dump() const;

	//! Is the event for this ID?
	bool id_match(fp_id_t id) const { return id & _id_set; }

	//! Get the type of the event
	const fp_type_t type() const { return _type; } 

	//! Get the data for the event
	const fp_data_t* data() const { return _data; }

	//! Get the data for the event
	const fp_length_t data_length() const { return _data_length; }

private:
	fp_id_t _id_set;
	fp_type_t  _type;
	fp_length_t  _data_length;
	fp_data_t  _data[FP_MAX_DATA_LEN];
	fp_checksum_t  _checksum;
	bool _complete;
};


