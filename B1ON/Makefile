CPP        = g++
CPPFLAGS   = -Wall -g

SOURCES	:= ${wildcard *.cpp}
OBJECTS	:= ${SOURCES:.cpp=.o}
EXES	:= ${SOURCES:.cpp=}

all: $(EXES)

B1OnPatchGetName: B1OnPatchGetName.cpp
	echo "Making $?"
	$(CPP) $(CPPFLAGS) $< -o $@

B1OnPatchUnpack000: B1OnPatchUnpack000.cpp
	echo "Making $?"
	$(CPP) $(CPPFLAGS) $< -o $@

ExamineUpdater: ExamineUpdater.cpp
	echo "Making $?"
	$(CPP) $(CPPFLAGS) $< -o $@

clean:
	rm -fv $(OBJECTS) $(EXES)
