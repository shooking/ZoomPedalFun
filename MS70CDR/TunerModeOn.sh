export MIDI_DEV=`amidi -l | grep ZOOM | awk '{print $2}'`
amidi -p ${MIDI_DEV} -S "B0 4A 40" -r temp.bin -t 1 ; hexdump -C temp.bin
