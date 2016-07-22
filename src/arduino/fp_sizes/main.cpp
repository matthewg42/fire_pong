#include <iostream>
#include <FpEvent.h>
#include <string.h>
#include <stdint.h>

using namespace std;

int main(int argc, char** argv)
{
    cout << "FP_SERIAL_BUF_LEN = " << FP_SERIAL_BUF_LEN << endl;
    cout << "FP_MINIMUM_PACKET_LEN = " << FP_MINIMUM_PACKET_LEN << endl;
    cout << "FP_SERIAL_LENGTH_OFFSET = " << FP_SERIAL_LENGTH_OFFSET << endl;
    cout << "FP_SERIAL_ID_OFFSET = " << FP_SERIAL_ID_OFFSET << endl;
    cout << "FP_SERIAL_TYPE_OFFSET = " << FP_SERIAL_TYPE_OFFSET << endl;
    cout << "FP_SERIAL_DATA_OFFSET = " << FP_SERIAL_DATA_OFFSET << endl;
    cout << "FP_MAX_DATA_LEN = " << FP_MAX_DATA_LEN << endl;

	return 0;
}
