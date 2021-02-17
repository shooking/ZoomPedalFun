export MIDI_DEV=`amidi -l | grep ZOOM | awk '{print $2}'`
thePatch=$(($1-10))
bank=$(($thePatch/10))
hexBank=`printf "%02x" $bank`
PGM=$((thePatch % 10))
hexPGM=`printf "%02x" ${PGM}`
echo $thePatch
echo $bank
echo $PGM
echo $hexBank
echo $hexPGM
probeString="F0 52 00 6E 09 00 ${hexBank} ${hexPGM} F7"
echo $probeString
theFile="patch_${bank}_${PGM}.bin"
amidi -p ${MIDI_DEV} -S ${probeString} -r ${theFile} -t 1 ; hexdump -C ${theFile}
