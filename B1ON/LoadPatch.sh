export MIDI_DEV=`amidi -l | grep ZOOM | awk '{print $2}'`
# we want patch 1..100
thePatch=$(($1-1))
plow=$(($thePatch))
hexLow=`printf "%02x" $plow`
# "B0 00 00 B0 20 00 C0 17" is 23
#probeString="B0 00 00 B0 20 00 00 C0 ${hexLow}"
probeString="C0 ${hexLow}"
echo ${probeString}

amidi -p ${MIDI_DEV} -S ${probeString} -r patch_change${thePatch}.bin -t 1 ; hexdump -C patch_change${thePatch}.bin
