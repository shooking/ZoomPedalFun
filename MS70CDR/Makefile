CPP        = g++
CPPFLAGS   = -Wall -g

SOURCES	:= ${wildcard *.cpp}
OBJECTS	:= ${SOURCES:.cpp=.o}
#EXES	:= ${SOURCES:.cpp=}

all: MS70CDRPatchUnpack000 MS70CDRPatchTempo MS70CDRInjectFX MS70CDRExaminePatch
readFile.o:	readFile.cpp
	echo "Compiling $?"
	$(CPP) $(CPPFLAGS) -c $<

writeFile.o:	writeFile.cpp
	echo "Compiling $?"
	$(CPP) $(CPPFLAGS) -c $<

unpack.o:	unpack.cpp
	echo "Compiling $?"
	$(CPP) $(CPPFLAGS) -c $<

pack.o:	pack.cpp
	echo "Compiling $?"
	$(CPP) $(CPPFLAGS) -c $<

MS70CDRPatchUnpack000: MS70CDRPatchUnpack000.o readFile.o unpack.o
	echo "Making $?"
	$(CPP) $(CPPFLAGS) -o $@ $< readFile.o unpack.o

MS70CDRPatchUnpack000.o: MS70CDRPatchUnpack000.cpp
	echo "Compiling $?"
	$(CPP) $(CPPFLAGS) -c $<

MS70CDRPatchTempo: MS70CDRPatchTempo.o readFile.o writeFile.o unpack.o pack.o
	echo "Making $?"
	$(CPP) $(CPPFLAGS) -o $@ $< readFile.o writeFile.o unpack.o pack.o

MS70CDRPatchTempo.o: MS70CDRPatchTempo.cpp
	echo "Compiling $?"
	$(CPP) $(CPPFLAGS) -c $<

MS70CDRPatchGetName: MS70CDRPatchGetName.cpp
	echo "Making $?"
	$(CPP) $(CPPFLAGS) $< -o $@


MS70CDRInjectFX.o: MS70CDRInjectFX.cpp
	echo "Making $?"
	$(CPP) $(CPPFLAGS) -c $<

MS70CDRInjectFX: MS70CDRInjectFX.o readFile.o writeFile.o unpack.o pack.o
	echo "Making $?"
	$(CPP) $(CPPFLAGS) -o $@ $< readFile.o writeFile.o unpack.o pack.o

MS70CDRExaminePatch.o:	MS70CDRExaminePatch.cpp
	echo "Compiling $?"
	$(CPP) $(CPPFLAGS) -c $<

MS70CDRExaminePatch: MS70CDRExaminePatch.o readFile.o writeFile.o unpack.o pack.o
	echo "Making $?"
	$(CPP) $(CPPFLAGS) -o $@ $< readFile.o writeFile.o unpack.o pack.o

clean:
	rm -fv $(OBJECTS) $(EXES)
