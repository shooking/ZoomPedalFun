export MIDI_DEV=`amidi -l | grep ZOOM | awk '{print $2}'`
amidi -p ${MIDI_DEV} -S "f0 7e 00 06 01 f7" -r temp.bin -t 1 ; hexdump -C temp.bin
