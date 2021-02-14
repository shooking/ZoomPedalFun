CPP        = g++
CPPFLAGS   = -Wall -g -c

SOURCES    := ${wildcard *.cpp}
OBJECTS    := ${SOURCES:.cpp=.o}

.PHONY:    all clean

.SUFFIXES: .cpp .o

all:       main

main:      $(OBJECTS)

.cpp.o:
	$(CPP) $(CPPFLAGS) $< -o $@

clean:
	rm -fv *.o
