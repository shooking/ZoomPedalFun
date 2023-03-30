export MIDI_DEV=`amidi -l | grep ZOOM | awk '{print $2}'`

theParam=$1
theParamMod=$(($theParam-1))
hexParam=`printf "%02x" $theParamMod`

probeString="F0 52 00 61 32 01 00 00 ${hexParam} 00 00 00 00 00 F7"
echo $probeString
amidi -p ${MIDI_DEV} -S $probeString -r temp.bin -t 1 ; hexdump -C temp.bin
