export MIDI_DEV=`amidi -l | grep ZOOM | awk '{print $2}'`
slot=$(($1+2))
hexSlot=`printf "%02x" $slot`
probeString="F0 52 00 6E 64 03 00 0A ${hexSlot} 01 00 00 00 00 F7"
theFile=rhythmnOnOff.bin
echo ${probeString}

amidi -p ${MIDI_DEV} -S ${probeString} -r ${theFile} -t 1 ; hexdump -C ${theFile}
