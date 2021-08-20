export MIDI_DEV=`amidi -l | grep ZOOM | awk '{print $2}'`
outFile=CheckIfMakesB3n.txt
for midiString in `grep "^SEND" ChangeToB3n.txt | awk -F\: '{print $2}'`
do
	echo "Sending next command"
	echo "SEND: ${midiString}" >> ${outFile}
	amidi -p ${MIDI_DEV} -S ${midiString} -r tm.bin -t 1 ; hexdump -C tm.bin
	cat tm.bin >> ${outFile}
	rm tm.bin
done


