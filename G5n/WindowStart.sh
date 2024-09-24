export MIDI_DEV=`amidi -l | grep ZOOM | awk '{print $2}'`
# Sets G5n window 
# 1 is FX1 - 4
# 2 is FX2 - 5
# 3 is FX3 - 6
# 4 is FX4 - 7
# 5 is FX5 - 8
# 6 is FX6 - 9
#
if [[ $# -ne 1 ]]; then
	echo "Usage WindowStart.sh [1-6]"
	exit
fi
if [[ $1 -lt 1 ]]; then
	echo "Usage WindowStart.sh [1-6]"
	exit
fi
if [[ $1 -gt 6 ]]; then
	echo "Usage WindowStart.sh [1-6]"
	exit
fi


logicalFS=$(($1-1))
hexSlot=`printf "%02x" $logicalFS`
#                                               OnOff
probeString="F0 52 00 6E 64 03 00 0a 01 ${hexSlot} 00 00 00 00 F7"

echo ${probeString}

amidi -p ${MIDI_DEV} -S ${probeString}
