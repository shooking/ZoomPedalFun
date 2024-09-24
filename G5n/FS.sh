export MIDI_DEV=`amidi -l | grep ZOOM | awk '{print $2}'`
# So on an G5n one sees FS1, FS2, FS3, FS4
# But these are logically 0 - 8 based on the FX's 1 - 9
if [[ $# -ne 2 ]]; then
	echo "Usage FS.sh [1-9] [0-1]"
	exit
fi
logicalFS=$(($1-1))
hexSlot=`printf "%02x" $logicalFS`
onOff=$2 #
#                                               OnOff
probeStringOnOff="F0 52 00 6E 64 03 00 ${hexSlot} 00 ${onOff} 00 00 00 00 F7"
# 1          f0 52 00 6e 64 03 00 00         00 01 00 00 00 00 f7 
# 2	     f0 52 00 6e 64 03 00 01         00 01 00 00 00 00 f7
echo ${probeString}

amidi -p ${MIDI_DEV} -S ${probeStringOnOff}
