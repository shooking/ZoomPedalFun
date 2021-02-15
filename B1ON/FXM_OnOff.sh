#!/bin/bash
export MIDI_DEV=`amidi -l | grep ZOOM | awk '{print $2}'`

# expect FX-1..5 0|1 off|on
# ie 1 
#    2 
theFX=$1
oo=$2
theFXMod=$(($theFX-1))
hexFX=`printf "%02x" $theFXMod`
OnOff=`printf "%02x" $oo`
probeString="F0 52 00 65 31 ${hexFX} 00 ${OnOff} 00 F7"
echo ${probeString}
theFile=temp.$$
amidi -p ${MIDI_DEV} -S ${probeString} -r ${theFile} -t 1 ; hexdump -C ${theFile}; rm ${theFile}

