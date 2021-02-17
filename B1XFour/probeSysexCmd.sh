#!/bin/bash -x

export MIDI_DEV=`amidi -l | grep ZOOM | awk '{print $2}'`
./EditorOn.sh
./PCModeOn.sh
for i in {0..127}
do
	fs=`printf "%03d" $i`
	hexSlot=`printf "%02x" $i`
     	probeString="F0 52 00 6E ${hexSlot} F7"
	theFile=p_${hexSlot}_${fs}.bin
       	amidi -p ${MIDI_DEV} -S ${probeString} -r ${theFile} -t 1
	let x=`ls -l ${theFile} | grep -c " 0 "`
       	if [ $x -eq 1 ]
	then
		echo $x
		rm ${theFile}
	fi
	./EditorOn.sh
done
./PCModeOff.sh
