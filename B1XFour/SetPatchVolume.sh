export MIDI_DEV=`amidi -l | grep ZOOM | awk '{print $2}'`
vol=$1
hexVol=`printf "%02x" ${vol}`
echo $hexVol
amidi -p ${MIDI_DEV} -S "f0 52 00 6e 64 03 00 0a 00 $hexVol 00 00 00 00 f7" -r temp.bin -t 1 ; hexdump -C temp.bin
