CPP        = g++
CPPFLAGS   = -Wall -g 
#-munaligned-access

SOURCES	:= ${wildcard *.cpp}
OBJECTS	:= ${SOURCES:.cpp=.o}
EXES	:= ${SOURCES:.cpp=}

all: $(EXES)

B1XFour_09_PTCF: B1XFour_09_PTCF.cpp
	echo "Making $?"
	$(CPP) $(CPPFLAGS) $< -o $@

B1XFourPTCF: B1XFourPTCF.cpp
	echo "Making $?"
	$(CPP) $(CPPFLAGS) $< -o $@

B1XFourPatchGetName: B1XFourPatchGetName.cpp
	echo "Making $?"
	$(CPP) $(CPPFLAGS) $< -o $@

B1XFourPatchUnpack000: B1XFourPatchUnpack000.cpp
	echo "Making $?"
	$(CPP) $(CPPFLAGS) $< -o $@

B1XFourFX00: B1XFourFX00.cpp
	echo "Making $?"
	$(CPP) $(CPPFLAGS) $< -o $@

B1XFourUnpack_ZD2: B1XFourUnpack_ZD2.cpp
	echo "Making $?"
	$(CPP) $(CPPFLAGS) $< -o $@

ParseZD2_000: ParseZD2_000.cpp
	echo "Making $?"
	$(CPP) $(CPPFLAGS) $< -o $@


clean:
	rm -fv $(OBJECTS) $(EXES)
