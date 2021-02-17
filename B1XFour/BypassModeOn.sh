export MIDI_DEV=`amidi -l | grep ZOOM | awk '{print $2}'`
amidi -p ${MIDI_DEV} -S "f0 52 00 6e 64 0b f7 B0 62 0C B0 63 00" -r temp.bin -t 1 ; hexdump -C temp.bin
