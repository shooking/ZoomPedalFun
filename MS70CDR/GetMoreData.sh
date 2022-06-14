#!/bin/bash
export MIDI_DEV=`amidi -l | grep ZOOM | awk '{print $2}'`

probeString="F0 52 00 61 60 05 00 F7"
echo ${probeString}
theFile=temp.$$
amidi -p ${MIDI_DEV} -S ${probeString} -r ${theFile} -t 1 ; hexdump -C ${theFile}; rm ${theFile}
