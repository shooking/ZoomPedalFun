export MIDI_DEV=`amidi -l | grep ZOOM | awk '{print $2}'`
amidi -p ${MIDI_DEV} -S "f0 7e 00 06 01 f7" -r temp.bin -t 1 ; hexdump -C temp.bin

#                   DEV           1  .  2  1
# f0 7e 00 06 02 52 65 00  00 00 31 2e 32 31 f7     |.~...Re...1.21.|
