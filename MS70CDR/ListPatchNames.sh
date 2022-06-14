#!/bin/bash
# what is current patch
./CurrentBankNumber.sh
# Stores in currentBank.bin
fileOut=MS70CDRContents.txt
rm ${fileOut}

./EditorOn.sh
for i in {1..50}
do
	./LoadPatch.sh ${i}
	./GetMoreData.sh
	./GetCurrentPatch.sh ${i}
	./MS70CDRPatchGetName currentPatch.bin ${i} >> ${fileOut}
	./EditorOn.sh
done
