export MIDI_DEV=`amidi -l | grep ZOOM | awk '{print $2}'`

#for i in `ls patch_??_??.bin`
for i in `ls patch_??.bin`
do
	echo "Loading $i"
	../../SetPatch.sh $i
	sleep 1
done
