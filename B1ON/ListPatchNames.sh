#!/bin/bash
# what is current patch
./CurrentBankNumber.sh
# Stores in currentBank.bin
fileOut=B1OnContents.txt
rm ${fileOut}

./EditorOn.sh
for i in {1..100}
do
	./LoadPatch.sh ${i}
	./GetMoreData.sh
	./GetCurrentPatch.sh ${i}
	./B1OnPatchGetName currentPatch.bin ${i} >> ${fileOut}
	./EditorOn.sh
done

./PlayFile.sh currentBank.bin
