export MIDI_DEV=`amidi -l | grep ZOOM | awk '{print $2}'`
amidi -p ${MIDI_DEV} -S "f0 52 00 6e 64 0a f7" -r temp.bin -t 1 ; hexdump -C temp.bin
