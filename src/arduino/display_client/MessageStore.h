#pragma once

#define MAX_MESSAGE_COUNT       5
#define MAX_MESSAGE_LEN         80

class MessageStore {
public:
    MessageStore();
    ~MessageStore();

    // append a message if there is still room
    void add(const char* message);

    // get a message by index
    const char* operator[](unsigned int n);

    // how many messages are stored
    const int size();

private:
    void clear();

    char* _messages[MAX_MESSAGE_COUNT];
    unsigned int _count;
};
