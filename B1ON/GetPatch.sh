export MIDI_DEV=`amidi -l | grep ZOOM | awk '{print $2}'`
thePatch=$(($1-1))
hexPatch=`printf "%02x" ${thePatch}`
echo $thePatch
echo $hexPatch
# NO ...               10's  units
# F0 52 00 65 63 09 00 00 00 F7
# F0 52 00 65 63 09 00 00 01 F7
#
probeString="F0 52 00 65 09 00 00 ${hexPatch} F7"

amidi -p ${MIDI_DEV} -S ${probeString} -r patch_${thePatch}.bin -t 1 ; hexdump -C patch_${thePatch}.bin
