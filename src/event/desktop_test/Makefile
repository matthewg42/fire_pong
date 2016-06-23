CFLAGS = -g -I../lib/fire_pong -DDESKTOP
LFLAGS = 
CXX = g++
TARGET = test
SOURCES = $(wildcard *.cpp) $(wildcard ../lib/fire_pong/*.cpp)
OBJECTS = $(subst .cpp,.o,$(SOURCES))

run: $(TARGET)
	./$(TARGET)
	
$(TARGET) : $(OBJECTS)
	$(CXX) $(LFLAGS) $^ -o $@
	
%.o : %.cpp
	$(CXX) $(CFLAGS) -c $< -o $@

.PHONY: clean
clean:
	rm -f $(TARGET) $(OBJECTS)


