export MIDI_DEV=`amidi -l | grep ZOOM | awk '{print $2}'`
probeString="f0 52 00 6e 64 03 00 0a 03 01 01 00 00 00 f7"
probeString="f0 52 00 6e 64 03 00 0a 01 00 00 00 00 00 f7 f0 52 00 6e 64 03 00 0a 03 00 00 00 00 00 f7 f0 52 00 6e 64 03 00 0a 01 00 00 00 00 00 f7"
theFile=looperrecplay.bin
echo ${probeString}

amidi -p ${MIDI_DEV} -S ${probeString} -r ${theFile} -t 1 ; hexdump -C ${theFile}
