#!/bin/bash # Define variables
SRCDIR=./B1ON
BINDIR=./B1ON
CXX=g++
CXXFLAGS="-Wall -Wextra -pedantic"
${CXX} ${CXXFLAGS} ${SRCDIR}/B1OnPatchGetName.cpp -o ${BINDIR}/B1OnPatchGetName
exit $?