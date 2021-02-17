#!/bin/bash
export MIDI_DEV=`amidi -l | grep ZOOM | awk '{print $2}'`

# expect FX
# ie 1 
#    2 
theFX=$1
theFXMod=$(($theFX-1))
hexFX=`printf "%02x" $theFXMod`
#1
#01
#00
#                                 FX  wr id
#            F0 52 00 6E 64 03 00 01  01 10 00 00 28 00 F7
#            F0 52 00 6E 64 03 00 02  01 00 00 00 00 00 F7
#            F0 52 00 6E 64 03 00 PP-1 01 00 00 00 00 00 F7
probeString="F0 52 00 6E 64 03 00 ${hexFX} 01 00 00 00 00 00 F7"
echo ${probeString}
theFile=temp.$$
amidi -p ${MIDI_DEV} -S ${probeString} -r ${theFile} -t 1 ; hexdump -C ${theFile}; rm ${theFile}

