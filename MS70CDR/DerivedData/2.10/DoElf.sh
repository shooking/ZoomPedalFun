#!/bin/bash

outlog=process.log
rm -f $(outlog)

for ELF in *.elf
do 
	echo "${ELF}" | tee -a ${outlog}
	picName=`basename "${ELF}" .elf`.png
	python extract_ZDL_device_icon.py -e "$ELF" -t "picEffectType_" -o "${picName}" 2>&1 | tee -a ${outlog}
done

