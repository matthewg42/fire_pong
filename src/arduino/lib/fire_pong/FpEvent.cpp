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

#include <FpEvent.h>
#include <crc8.h>
#ifdef DESKTOP
#include <iostream>
using namespace std;
#else
#include <Arduino.h>
#endif
#include "string.h"

// Magic is an unsigned short little endian, "fP", which when decoded turns
// out to be the value 0x5066.  We use a static not a #define so we can memcpy 
// from it...
static fp_magic_t FP_MAGIC=0x5066;

static uint8_t fp_event_serial_buf[FP_SERIAL_BUF_LEN];

FpEvent::FpEvent() :
	_type(0xff),
	_checksum(0),
	_complete(false)
{
}
   
FpEvent::FpEvent(fp_id_t id_set, fp_type_t type, const fp_data_t* data, fp_length_t data_length) :
	_id_set(id_set),
	_type(type),
	_data_length(data_length),
	_checksum(0),
	_complete(false)
{
	if (set_payload(data, data_length)) {
		_complete = true;
	}
}

	// Create an FpEvent from a blob of serialized data 
FpEvent::FpEvent(uint8_t* buf)
{
	if (parse_serial_data(buf)) {
		_complete = true;
	} else {
		_complete = false;
	}
}

FpEvent::~FpEvent()
{
}

void FpEvent::reset() {
	_id_set = 0;
	_type = 0xff;
	_data_length = 0;
	_checksum = 0;
	memset(_data, 0, FP_MAX_DATA_LEN);
	_complete = false;
}

// Update all fields from a blob of serialized data
// Truen true if parsed OK
bool FpEvent::parse_serial_data(uint8_t* buf)
{
	uint8_t* ptr = buf;
	// Check magic
	if (*(reinterpret_cast<fp_magic_t*>(ptr)) != FP_MAGIC) { return false; }
	ptr += sizeof(fp_magic_t);

	// Get and check the length of packet
	fp_length_t packet_length = *(reinterpret_cast<fp_length_t*>(ptr));
	ptr += sizeof(fp_length_t);
	if ( packet_length > FP_SERIAL_BUF_LEN || packet_length < FP_MINIMUM_PACKET_LEN) { return false; }
	_data_length = packet_length - FP_MINIMUM_PACKET_LEN;
	if (_data_length > FP_MAX_DATA_LEN) { return false; }
	
	// Get the fixed length items
	_id_set = *(reinterpret_cast<fp_id_t*>(ptr));
	ptr += sizeof(fp_id_t);

	_type = *(reinterpret_cast<fp_type_t*>(ptr));
	ptr += sizeof(fp_type_t);

	// Populate data, zero unused items
	for(fp_length_t i=0; i<=FP_MAX_DATA_LEN; i++) {
		if (i<_data_length) {
			_data[i] = *(reinterpret_cast<fp_data_t*>(ptr));
			ptr += sizeof(fp_data_t);
		} else {
			_data[i] = 0;
		}
	}

	_checksum = *(reinterpret_cast<fp_checksum_t*>(ptr));
	ptr += sizeof(fp_checksum_t);

	// Finally, check we have the end magic
	if (*(reinterpret_cast<fp_magic_t*>(ptr)) != FP_MAGIC) { return false; }
	return true;
}

// Update the payload (and length). Also updates checksum
bool FpEvent::set_payload(const fp_data_t* data, fp_length_t length)
{
	if (length>FP_MAX_DATA_LEN) { return false; }

	for(fp_length_t i=0; i<FP_MAX_DATA_LEN; i++) {
		if (i<length) {
			_data[i] = data[i];
		} else {
			_data[i] = 0;
		}
	}
	_data_length = length;
	_checksum = this->calculate_checksum();
	return true;
}

// Update the checksum based on the rest of the FpEvent
fp_checksum_t FpEvent::calculate_checksum() const
{
	uint8_t* buf = serialize();
	fp_length_t len = *(reinterpret_cast<fp_length_t*>(buf+sizeof(fp_magic_t)));
	if (len>FP_SERIAL_BUF_LEN) { len=FP_SERIAL_BUF_LEN; }
	return crc8(buf, len-sizeof(fp_checksum_t)-sizeof(fp_magic_t));
}

// Check that the checksum which is set matches the rest of the FpEvent
bool FpEvent::validate_checksum() const
{
	return _checksum == calculate_checksum();
}

bool FpEvent::is_valid() const
{
	return validate_checksum() && _complete;
}

//! Get a serialized blob of data which encapsulates the FpEvent
uint8_t* FpEvent::serialize() const
{
	uint8_t* ptr = fp_event_serial_buf;
	fp_length_t* len_ptr;
	fp_length_t data_len = _data_length;
	memcpy(ptr, reinterpret_cast<uint8_t*>(&FP_MAGIC), sizeof(fp_magic_t));
	ptr += sizeof(fp_magic_t);
	len_ptr = reinterpret_cast<fp_length_t*>(ptr);
	ptr += sizeof(fp_length_t);
	memcpy(ptr, reinterpret_cast<const uint8_t*>(&_id_set), sizeof(fp_id_t));
	ptr += sizeof(fp_id_t);
	memcpy(ptr, reinterpret_cast<const uint8_t*>(&_type), sizeof(fp_type_t));
	ptr += sizeof(fp_type_t);
	if (data_len > FP_MAX_DATA_LEN) { data_len = FP_MAX_DATA_LEN; }
	memcpy(ptr, reinterpret_cast<const uint8_t*>(&_data), sizeof(fp_data_t) * data_len);
	ptr += sizeof(fp_data_t) * data_len;
	memcpy(ptr, reinterpret_cast<const uint8_t*>(&_checksum), sizeof(fp_checksum_t));
	ptr += sizeof(fp_checksum_t);
	memcpy(ptr, reinterpret_cast<const uint8_t*>(&FP_MAGIC), sizeof(fp_magic_t));
	ptr += sizeof(fp_magic_t);
	*len_ptr = ptr - fp_event_serial_buf;
	return fp_event_serial_buf;
}

void FpEvent::dump() const
{
#ifdef DESKTOP
    cout << "FpEvent: id_set=0x" << hex << (long)_id_set 
        << ", type=" << (int)_type 
        << ", data_length=" << dec << (int)_data_length 
        << ", data=\"" << _data 
        << "\" [";
	for (uint8_t i=0; i<FP_MAX_DATA_LEN && i<_data_length; i++) {
		cout.fill('0');
		cout.width(2);
		cout << hex << (int)_data[i];
		if (i<FP_MAX_DATA_LEN-1 && i<_data_length-1)
			cout << " ";
	}
	//cout << "], cksum=" << hex << (int)_checksum 
	cout << "], cksum=" << hex << (int)this->_checksum
		<< " (" << (this->validate_checksum() ? "GOOD:0x" : "BAD:0x") << hex << (int)this->calculate_checksum() 
		<< ") complete=" << _complete << ", valid=" << is_valid() << endl;
#else
	Serial.print(F("FpEvent: id_set=0x"));
	Serial.print((long)_id_set, HEX);
	Serial.print(F(", type="));
	Serial.print((int)_type, DEC);
	Serial.print(F(", length="));
	Serial.print((int)_data_length, DEC);
	Serial.print(F(", data=\""));
	Serial.print(reinterpret_cast<const char*>(_data));
	Serial.print(F("\" ["));
	for (uint8_t i=0; i<FP_MAX_DATA_LEN && i<_data_length; i++) {
		Serial.print((int)_data[i], HEX);
		if (i<FP_MAX_DATA_LEN-1 && i<_data_length-1)
			Serial.print(F(" "));
	}
	Serial.print(F("], cksum="));
	Serial.print((int)this->_checksum, HEX);
	Serial.print(F(" ("));
	Serial.print(this->validate_checksum() ? F("GOOD:0x") : F("BAD:0x"));
	Serial.print((int)this->calculate_checksum(), HEX); 
	Serial.print(F(") complete="));
	Serial.print(_complete);
	Serial.print(F(", valid="));
	Serial.println(is_valid());
#endif
}


