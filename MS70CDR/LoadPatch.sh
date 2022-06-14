export MIDI_DEV=`amidi -l | grep ZOOM | awk '{print $2}'`
rawBank=$1
theBank=$(($rawBank-1))
hexBank=`printf "%02x" $theBank`
amidi -p ${MIDI_DEV} -S "b0 00 00 b0 20 00 c0 ${hexBank}" -r temp.bin -t 1 ; hexdump -C temp.bin

