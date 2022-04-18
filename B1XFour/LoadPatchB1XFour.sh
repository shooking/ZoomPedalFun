export MIDI_DEV=`amidi -l | grep ZOOM | awk '{print $2}'`
# we want patch 10 .. 50 ... 0 .. 40
thePatch=$(($1-10))
plow=$(($thePatch%10))
phigh=$(($thePatch/10))
hexLow=`printf "%02x" $plow`
hexHigh=`printf "%02x" $phigh`
echo $hexLow
echo $hexHigh
# "B0 00 00 B0 20 01 C0 03" is 23
probeString="B0 00 00 B0 20 ${hexHigh} 00 C0 ${hexLow}"
echo ${probeString}

amidi -p ${MIDI_DEV} -S ${probeString} -r patch_change${thePatch}.bin -t 1 ; hexdump -C patch_change${thePatch}.bin
