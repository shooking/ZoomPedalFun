#!/bin/bash
export MIDI_DEV=`amidi -l | grep ZOOM | awk '{print $2}'`
#
# seems to also dump, sometimes, state of the effect?
# but not consistently - likely based on EditorOn
#
# expect FX Param value
# ie 1 1 10
#    2 3 20
theFX=$1
theParam=$2
theValue=$3
theFXMod=$(($theFX-1))
theParamMod=$(($theParam+1))
hexFX=`printf "%02x" $theFXMod`
hexParam=`printf "%02x" $theParamMod`
theVlow=$(($theValue & 127))
theVhigh=$(( ($theValue / 128) & 127 ))
hexValueLow=`printf "%02x" $theVlow`
hexValueHigh=`printf "%02x" $theVhigh`
echo $theValue
echo $hexValueLow
echo $hexValueHigh

#            F0 52 00 6E 64 03 00 02 02 01 00 00 00 00 F7
probeString="F0 52 00 6E 64 03 00 ${hexFX} ${hexParam} ${hexValueLow} ${hexValueHigh} 00 00 00 F7"
echo ${probeString}
theFile=temp.$$
amidi -p ${MIDI_DEV} -S ${probeString} -r ${theFile} -t 1 ; hexdump -C ${theFile}; rm ${theFile}

