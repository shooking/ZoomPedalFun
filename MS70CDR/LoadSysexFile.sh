export MIDI_DEV=`amidi -l | grep ZOOM | awk '{print $2}'`
# $1 is the file to load
amidi -p ${MIDI_DEV} -s ${1}
