export MIDI_DEV=`amidi -l | grep ZOOM | awk '{print $2}'`
tempo=$1
hexTempoLow=`printf "%02x" $((tempo & 0x7F))`
hexTempoHigh=`printf "%02x" $(( (tempo / 128 ) & 0x7F))`
echo $hexTempo
amidi -p ${MIDI_DEV} -S "f0 52 00 6e 64 03 00 0a 02 $hexTempoLow $hexTempoHigh 00 00 00 f7" -r temp.bin -t 1 ; hexdump -C temp.bin
