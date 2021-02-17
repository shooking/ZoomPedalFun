export MIDI_DEV=`amidi -l | grep ZOOM | awk '{print $2}'`
pos=$(($1-1))
val=$2
# NOTE got to be sure to check range is 0 ... 9 input 1 ... 10
# r = 114 no idea of the charset.
hexCharPos=`printf "%02x" ${pos}`
hexCharVal=`printf "%02x" ${val}`
echo $hexCharPos
echo $hexCharVal
amidi -p ${MIDI_DEV} -S "f0 52 00 6e 64 03 00 09 $hexCharPos $hexCharVal 00 00 00 00 f7" -r t1.bin -t 1; hexdump -C t1.bin; rm t1.bin
