export MIDI_DEV=`amidi -l | grep ZOOM | awk '{print $2}'`
# we want patch 10 .. 50 ... 0 .. 40
amidi -p ${MIDI_DEV} -s ${1}
