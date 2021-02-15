export MIDI_DEV=`amidi -l | grep ZOOM | awk '{print $2}'`
vol=$1
hexVol=`printf "%02x" ${vol}`
echo $hexVol
#                                       FX6
amidi -p ${MIDI_DEV} -S "f0 52 00 65 31 06 00 $hexVol 00 f7" -r temp.bin -t 1 ; hexdump -C temp.bin
