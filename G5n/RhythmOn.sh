export MIDI_DEV=`amidi -l | grep ZOOM | awk '{print $2}'`
probeString="F0 52 00 6E 64 03 00 0A 05 01 00 00 00 00 F7"
theFile=rhythmnOnOff.bin
echo ${probeString}

amidi -p ${MIDI_DEV} -S ${probeString} -r ${theFile} -t 1 ; hexdump -C ${theFile}


