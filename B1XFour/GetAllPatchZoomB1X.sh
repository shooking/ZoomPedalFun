#!/bin/bash
for i in {10..59}
do
	./GetPatch.sh ${i}
	./GetPatchBankPgm.sh ${i}
done
