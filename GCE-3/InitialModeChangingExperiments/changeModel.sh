export MIDI_DEV=`amidi -l | grep ZOOM | awk '{print $2}'`
outFile=Check${1}.txt
for midiString in `grep "^SEND" ChangeTo${1}.txt | awk -F\: '{print $2}'`
do
	echo "Sending next command"
	echo "SEND: ${midiString}" >> ${outFile}
	amidi -p ${MIDI_DEV} -S ${midiString} -r tm.bin -t 1 ; hexdump -C tm.bin > tm.txt
	cat tm.txt >> ${outFile}
	rm tm.bin tm.txt
done


