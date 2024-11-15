import sys
import json


# Process ZDL (Zoom FX DL version 1.0)
# ELF starts at offset 0x4c
# So ideally we want to write out the ELF part too
def check(zdlData, unknownCount):
    x = zdlData[64:64 + 8]
    #print(x)
    data = zdlData
    # try to find name. Is is 0x30 chars from OnOff
	# These "OnOff" blocks seems to 0x30 long and look until next 4 bytes are 00
    OnOffstart = data.find(b"OnOff")
    lastParam = False;
    if OnOffstart != -1:
        fxName=""
        OnOffblockSize = 0x30
        # Seems that the last 4 bytes of an OnOffBlock row tell us:
        # 4th from end && b100 => last parameter
        # 0x16 => stereo I think
        # & b10100 => tempo sync
        try:
            # first row is OnOff, a 1 in 0C and ID in 1C 1D
            # 2nd row should be name with FF FF FF FF in 0C 0D 0E 0F
            # then we keep reading one OnOff block at a time until we find byte 0x2c & b100 is set
            # this seems to be end of parameter
            allFF = True # assume we hit all FF
            for b4 in range(12, 16):
                allFF = allFF and (data[OnOffstart + OnOffblockSize + b4] == 0xFF)
            if allFF == False:
                # something wrong BAIL
                print("Did not find properly blanked name. Bailing")
                sys.exit(1)

            # OK so the 2nd line exists and is likely an FX Name - read it
            for j in range(12):
                if data[OnOffstart + j + OnOffblockSize] == 0x00:
                    break
                fxName = fxName + chr(data[OnOffstart + j + OnOffblockSize])
            tD = {
                "fxname" : fxName
            }

            # OK so we read in the name - now we examine OnOffblockSize at a time looking for param type
            mmax = []
            mdefault = []
            name = []
            tempoParam = []
            stereoParam = []
            numParameters = 0
            #print("OnOffStart at {}".format(OnOffstart))
            for j in range(2, 100):     # we expect to complete BEFORE we hit 100
                lastParam == False

                # GET parameter name
                currName = ""
                for i in range(12):
                    if data[OnOffstart + j * OnOffblockSize + i] == 0x00:
                        break
                    currName = currName + chr(data[OnOffstart + j * OnOffblockSize + i])
                name.append(currName)
                # GET max midi value
                mmax.append(    data[OnOffstart + j * OnOffblockSize + 12] + 
                                data[OnOffstart + j * OnOffblockSize + 13] * 256)
                # GET default midi value
                mdefault.append(data[OnOffstart + j * OnOffblockSize + 16] + 
                                data[OnOffstart + j * OnOffblockSize + 17] * 256)
                # Check status of 0x2c on row - this tells us
                testByte = data[OnOffstart + j * OnOffblockSize + 0x2C]
                if testByte & 0x04 == 0x04:
                    lastParam = True
                if testByte & 0x10 == 0x10:
                    stereoParam.append(True)
                else:
                    stereoParam.append(False)
                if testByte & 0x28 == 0x28:
                    tempoParam.append(True)
                else:
                    tempoParam.append(False)
                #print(mmax[j])
                #print(mdefault[j])
            
                #print("increment params")
                numParameters = numParameters + 1
                if lastParam == True:
                    break

            #print("Found {} parameters.".format(numParameters))
            if lastParam == False:
                print("PROCESSING " + fxName + "\t\t\tDIDNT FIND A NATURAL END OF PARAM??")
            mult = 256
            if x[2] & 0xC0 == 0:
                tD['fxid'] = str(hex( x[1] * mult + x[0] ))
                tD['gid'] = str(hex(x[3]) )
            else:
                tD['fxid'] = str(hex( x[1] * mult + x[0] ))
                tD['gid'] = str(hex( ( (x[3] * mult) + (x[2] & 0xC0)) >>4 ) )
            tD['version'] = "{}{}{}{}".format(chr(x[4]), chr(x[5]), chr(x[6]), chr(x[7]) )
            tD['Parameters'] = []
            # 0 is the OnOff state
            # 1 is the name
            # so actual paramters start from index 2, but clearly there are 2 less
            for i in range(numParameters):
                #print(i)
                tD['Parameters'].append({'name': name[i], 'mmax': mmax[i], 'mdefault': mdefault[i], 'stereo': stereoParam[i], 'tempo': tempoParam[i]})
            
            #json.dump(tD, sys.stdout, indent=4)
            with open(fxName+'.json', "w") as f:
                json.dump(tD, f, indent=4)
    
            # so we have the name now ... let's open an ELF file and write contents out
            with open(fxName+'.elf', "wb") as f:
                f.write(zdlData[0x4c:])
            return fxName+'.ZDL'
        except:
            # so we have the name now ... let's open an ELF file and write contents out
            with open(str(unknownCount)+'.elf', "wb") as f:
                f.write(zdlData[0x4c:])
            
            return None     
    else:
        # so we have the name now ... let's open an ELF file and write contents out
        with open(str(unknownCount)+'.elf', "wb") as f:
            f.write(zdlData[0x4c:])    
        return None

#
# Find signature of a ZDL
# Get the blocks (4096 but 6 bytes used for prev, next, end)
# Relative to the ZDL, the ELF is 0x4c chars in.
# We want to store this as well so we can derive the bitmap image data
#
# So I need to think this thru. I need to check, when we move next block,
# what happens at end. Should we move the byte size or the full block?
# 
if __name__ == "__main__":
    if len(sys.argv) == 2:
        with open(sys.argv[1], "rb") as f:
            # we are looking for 6 bytes then 0000000053495A45
            # lets assume the pattern will be past 6th bytearray
            # and we need at least 8 bytes left to read pattern
            rawX = f.read()
        ZDL=bytearray()
        # note the loop variable is updated in the loop!
        unknownCount = 0
        i = 0
        foundFirst = False
        while i < len(rawX) - 8:
            if (rawX[i  ] == 0x00 and
                rawX[i+1] == 0x00 and
                rawX[i+2] == 0x00 and
                rawX[i+3] == 0x00 and
                rawX[i+4] == 0x53 and
                rawX[i+5] == 0x49 and
                rawX[i+6] == 0x5A and
                rawX[i+7] == 0x45):
                # a match -- assert that previous bytes
                checkMe = rawX[i-6:i]
                prevBlock = checkMe[1] * 256 + checkMe[0]
                nextBlock = checkMe[3] * 256 + checkMe[2]
                sizeBlock = checkMe[5] * 256 + checkMe[4]
                #print("{} {} {}: {}".format(prevBlock, nextBlock, sizeBlock, i))
                if prevBlock == 0:
                    # we found the large FLTSEQ part ... 
                    i = i + 1
                    continue
                elif prevBlock != 65535:
                    # So we skipped block 0 ...
                    # next valid block pattern should be 65535(-1) Next size
                    i = i + 1
                #    print("Something wrong with this ZDL")
                else:
                    # now we got to keep going, sizeBlock at a time,
                    # a block will always be max 4090 large. Even if we get less
                    # the contents will be padded with FF
                    blockCount = 0
                    processBlock = True
                    #print("ZDL found at offset " + hex(i))
                    while (nextBlock != 0xFFFF):
                        blockCount = blockCount + 1
                        # this should be removing unused/formatting bytes
                        ZDL.extend(rawX[i:i + sizeBlock])
                        i = i + 4096
                        checkMe = rawX[i-6:i]
                        prevBlock = checkMe[1] * 256 + checkMe[0]
                        #print("new prevBlock {} old nextBlock: {}".format(prevBlock, nextBlock))
                        #print("new prevBlock == old nextBlock: {}".format(prevBlock==nextBlock))
                        nextBlock = checkMe[3] * 256 + checkMe[2]
                        sizeBlock = checkMe[5] * 256 + checkMe[4]
                        #print("{} {} {}: {}".format(prevBlock, nextBlock, sizeBlock, i))
                        if (prevBlock == 0xFFFF):
                            # this seems to be corruption or a single block FX
                            # i is our incr - it was updated above to next block
                            # so here exit the while, process current chunk
                            # and leave the above increment to find new FX on next loop
                            #print("oh we a new start block - we need to break")
                            processBlock = False
                            break
                    #
                    # OK we are are the next block ...
                    if (processBlock == True) or (nextBlock == 0xFFFF):
                        blockCount = blockCount + 1
                        ZDL.extend(rawX[i:i + sizeBlock])
                        # at the sizeBlock (less then 4090) we get to 0xFF's until
                        # next start block. So skip next 4096.
                        i = i + 4096
                        # now write out the ZDL. Function writes out JSON
                        #print(ZDL)                        
                    fxnamefile = check(ZDL, unknownCount) 
                    if None == fxnamefile:
                        g = open(str(unknownCount) + '.ZDL', "wb")
                        g.write(ZDL)
                        g.close()
                        unknownCount = unknownCount + 1
                        ZDL=bytearray()
                    
                        continue
                             
                    g = open(fxnamefile, "wb")
                    g.write(ZDL)
                    g.close()
                    ZDL=bytearray()
                    #print("{}  {}".format(fxnamefile, blockCount))
                    foundFirst = True
                    continue
            i = i + 1
