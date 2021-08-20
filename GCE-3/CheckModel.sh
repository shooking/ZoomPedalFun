export MIDI_DEV=`amidi -l | grep ZOOM | awk '{print $2}'`
amidi -p ${MIDI_DEV} -S "f0 52 00 6E 58 02 F7" -r tm.bin -t 1 ; hexdump -C tm.bin
