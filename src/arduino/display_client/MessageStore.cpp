#include "MessageStore.h"
#include <string.h>

MessageStore::MessageStore()
{
    clear();
}

void MessageStore::clear() {
    for(int i=0; i<MAX_MESSAGE_COUNT; i++) 
    {
        memset(_messages, 0, sizeof(char) * MAX_MESSAGE_LEN);
    }
    _count = 0;
}

MessageStore::~MessageStore()
{
}


// append a message if there is still room
void MessageStore::add(const char* message)
{
    if (_count < MAX_MESSAGE_COUNT) {
        strncpy(_messages[_count], message, MAX_MESSAGE_LEN);
        _count++;
    }
}

// get a message by id
const char* MessageStore::operator[](unsigned int n)
{
    if (n < _count) {
        return _messages[_count];
    } else {
        return NULL;
    }
}

// how many messages are stored
const int MessageStore::size()
{
    return _count;
}

