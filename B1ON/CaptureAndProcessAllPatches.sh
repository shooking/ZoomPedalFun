#!/bin/bash

theFile=TotalDecode.txt
for i in {1..100}
do
    pedalNum=$(($i - 1))
    fileNum=`printf "%03d" ${pedalNum}`
    echo "Processing Patch ${fileNum}"
    echo "Processing Patch ${fileNum}" >> ${theFile}
    ./EditorOn.sh
    ./LoadPatch.sh ${i}
	# grab it
    ./GetMoreData.sh && ./GetCurrentPatch.sh
    # process and rename output
    ./B1OnPatchUnpack000 currentPatch.bin >> ${theFile}
    mv currentPatch.bin patch_${fileNum}.bin
    # zero out parameters. Might be issue for multi slot
    echo "Zeroing parameters"
    for slot in {1..5}
    do
        for param in {1..9}
        do
            ./FXM_PN.sh ${slot} ${param} 0
        done
    done
    echo "Processing Zeroed Patch ${fileNum}"
    echo "Processing Zeroed Patch ${fileNum}" >> ${theFile}
    # grab it
    ./GetMoreData.sh && ./GetCurrentPatch.sh
    # process and rename it
    ./B1OnPatchUnpack000 currentPatch.bin >> ${theFile}
    mv currentPatch.bin patch_zero_${fileNum}.bin
    # reload original back
    ./LoadSysexFile.sh patch_${fileNum}.bin
done