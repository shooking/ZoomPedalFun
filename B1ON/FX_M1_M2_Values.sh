#!/bin/bash
export MIDI_DEV=`amidi -l | grep ZOOM | awk '{print $2}'`
#
# seems to also dump, sometimes, state of the effect?
# but not consistently - likely based on EditorOn
#
# expect FX slot values start end
# ie 1 1
#    1 3
# so if we say 1, we want MIDI to ask for 0
FXStart=$1
FXEnd=$2

theFXStart=$(($FXStart-1))
theFXEnd=$(($FXEnd-1))

hexFXStart=`printf "%02x" $theFXStart`
hexFXEnd=`printf "%02x" $theFXEnd`

probeString="F0 52 00 65 64 02 ${hexFXStart} ${hexFXEnd} 00 F7"
echo ${probeString}
theFile=temp.$$
amidi -p ${MIDI_DEV} -S ${probeString} -r ${theFile} -t 1 ; hexdump -C ${theFile}; rm ${theFile}

