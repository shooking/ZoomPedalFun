#!/bin/bash
./EditorOn.sh
for i in {1..298}
do
	./LoadPatch.sh ${i}
	./GetCurrentPatch.sh
	mv currentPatch.bin current_sysex_`printf "%03d" ${i}`.bin
done
