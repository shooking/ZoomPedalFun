#!/bin/bash
export MIDI_DEV=`amidi -l | grep ZOOM | awk '{print $2}'`
#
# expect SLOT FX_ID FX_GROUP
#
# So we get string like
# LMT1176.ZD2
# 1.50
# 01 20
# 80 01
#
# or
# CRNTRI3S.ZD2
# 1.10
# 01 31
# 00 06
#
# in 01 20 the 20 is the FX ID
# in 01 31, sometimes we need 0x30 = 48
#
# So the last two are "reversed" is 80 1 == 1 80, 00 06 = 06 00
#
# ie 1 48 
#    2 3 20
#
# we read in theSlot and bias by -1

theSlot=$1
theSlotMod=$(($theSlot-1))
hexSlot=`printf "%02x" $theSlotMod`

# We read in the FX ID and convert to low/high

theFXID=$2
hexFXLow=$(($theFXID & 127))
hexFXHigh=$(( ($theFXID / 128) & 127 ))
hexFXValueLow=`printf "%02x" $hexFXLow`
hexFXValueHigh=`printf "%02x" $hexFXHigh`

# We read in the FX GROUP and convert to low/high
theValue=$3
theValueMod=$(($theValue / 32 ))

# we switch FX on
OnOff=`printf "%02x" 1`

hexGroupVal=`printf "%02x" $theValueMod`

#                                 sl    ID       GID
#            F0 52 00 6E 64 03 00 00 01 30 00 00 08 00 F7
probeString="F0 52 00 6E 64 03 00 ${hexSlot} ${OnOff} ${hexFXValueLow} ${hexFXValueHigh} 00 ${hexGroupVal} 00 F7"
echo ${probeString}
theFile=temp.$$
amidi -p ${MIDI_DEV} -S ${probeString} -r ${theFile} -t 1 ; hexdump -C ${theFile}; rm ${theFile}

