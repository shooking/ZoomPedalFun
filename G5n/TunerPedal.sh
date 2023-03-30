export MIDI_DEV=`amidi -l | grep ZOOM | awk '{print $2}'`
# you have to prime the rhythm then choose slot
# optional - you can turn editor on it you want to see interaction.
probeString="F0 52 00 6E 63 0b F7 b0 62 0c b0 63 00"
theFile=rhythmnOnOff.bin
echo ${probeString}

amidi -p ${MIDI_DEV} -S ${probeString} -r ${theFile} -t 1 ; hexdump -C ${theFile}
