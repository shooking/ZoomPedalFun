#!/bin/bash
export MIDI_DEV=`amidi -l | grep ZOOM | awk '{print $2}'`

#            F0 52 00 5B 29 00 F7
probeString="F0 52 00 5B 29 F7"
echo ${probeString}
theFile=currentPatch.bin
rm -f ${theFile}
#amidi -p ${MIDI_DEV} -S ${probeString} -r ${theFile} -t 1 ; hexdump -C ${theFile}
amidi -p ${MIDI_DEV} -S ${probeString} -r ${theFile} -t 1 
