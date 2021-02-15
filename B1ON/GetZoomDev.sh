export MIDI_DEV=`amidi -l | grep ZOOM | awk '{print $2}'`
