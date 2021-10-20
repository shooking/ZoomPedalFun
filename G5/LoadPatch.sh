#!/bin/bash
export MIDI_DEV=`amidi -l | grep ZOOM | awk '{print $2}'`
# we want patch 1..100
theBank=$(($1-1))
blow=$(($theBank % 3))
bhexLow=`printf "%02x" $blow`
plow=$(($theBank / 3))
phexLow=`printf "%02x" $plow`
# "B0 00 00 B0 20 00 C0 17" is 23
probeString="B0 00 00 B0 20 ${phexLow} C0 ${bhexLow}"
echo ${probeString}

amidi -p ${MIDI_DEV} -S ${probeString} 
#-r patch_change${theBank}.bin -t 1 ; hexdump -C patch_change${theBank}.bin
