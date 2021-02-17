export MIDI_DEV=`amidi -l | grep ZOOM | awk '{print $2}'`
thePatch=$(($1-10))
hexPatch=`printf "%02x" ${thePatch}`
echo $thePatch
echo $hexPatch
# NO ...               10's  units
# F0 52 00 6E 46 00 00 01 00 09 00 F7
# F0 52 00 6E 46 00 00 02 00 00 00 F7
#
probeString="F0 52 00 6E 46 00 00 00 00 ${hexPatch} 00 F7"

amidi -p ${MIDI_DEV} -S ${probeString} -r patch_${thePatch}.bin -t 1 ; hexdump -C patch_${thePatch}.bin
