#!/bin/bash
function GetScaleFactor() {
	#echo "In ScaleFactor"
	export MIDI_DEV=`amidi -l | grep ZOOM | awk '{print $2}'`
	amidi -p ${MIDI_DEV} -S "f0 52 00 6e 64 11 f7" -r gmd.bin -t 1 ; # hexdump -C gmd.bin
	hexdump -C gmd.bin
	tx1=`xxd -s7 -l1 gmd.bin | awk -F\: '{print $2}' | awk '{print "0x"$1}'`
	tx2=`xxd -s6 -l1 gmd.bin | awk -F\: '{print $2}' | awk '{print "0x"$1}'`
	x1=`printf "%d" $tx1`
	x2=`printf "%d" $tx2`
	scaleFactor=`printf "%d" $(( ${x1} * 128 + ${x2} ))`
	#echo $x1
	#echo $x2
	echo $scaleFactor
	#return $scaleFactor
}

GetScaleFactor
