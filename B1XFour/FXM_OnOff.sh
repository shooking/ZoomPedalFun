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
#                                       on/off
#            F0 52 00 6E 64 03 00 00 00 01 00 00 00 00 F7
#            F0 52 00 6E 64 03 00 02   00 01 00 00 00 00 F7
#            F0 52 00 6E 64 03 00 PP-1 00 01 00 00 00 00 F7
probeString="F0 52 00 6E 64 03 00 ${hexFX} 00 ${OnOff} 00 00 00 00 F7"
echo ${probeString}
theFile=temp.$$
amidi -p ${MIDI_DEV} -S ${probeString} -r ${theFile} -t 1 ; hexdump -C ${theFile}; rm ${theFile}

