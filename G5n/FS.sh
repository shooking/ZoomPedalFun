export MIDI_DEV=`amidi -l | grep ZOOM | awk '{print $2}'`
slot=$(($1-1))
hexSlot=`printf "%02x" $slot`
#                                               OnOff
probeString="F0 52 00 6E 64 03 00 ${hexSlot} 00 01 00 00 00 00 F7"
echo ${probeString}

amidi -p ${MIDI_DEV} -S ${probeString}
