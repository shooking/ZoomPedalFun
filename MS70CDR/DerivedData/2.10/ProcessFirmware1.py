import sys
import os
import glob
from csplitb import CSplitB



# -*- coding: ascii -*-
import sys
import json

def check(zdlData):
    x = zdlData[64:64 + 8]
    #print(x)
    data = zdlData
    # try to find name. Is is 0x30 chars from OnOff
	# These "OnOff" blocks seems to 0x30 long and look until next 4 bytes are 00
    OnOffstart = data.find(b"OnOff")

    if OnOffstart != -1:
        fxName=""
        OnOffblockSize = 0x30
        for j in range(12):
            if data[OnOffstart + j + OnOffblockSize] == 0x00:
                break
            fxName = fxName + chr(data[OnOffstart + j + OnOffblockSize])
        tD = {
            "fxname" :fxName
        }
        mmax = []
        mdefault = []
        name = []
        mpedal = []
        numParameters = 0
        #print("OnOffStart at {}".format(OnOffstart))
        for j in range(0, 10):
            if  not ( data[OnOffstart + (j+1) * OnOffblockSize - 1] == 0x00
                 and  data[OnOffstart + (j+1) * OnOffblockSize - 2] == 0x00):
                # ZD2 format has a length and PRME offset. ZDL has none of this.
                print("End of the parameters")
                break
            if (      data[OnOffstart + (j) * OnOffblockSize    ] == 0x00
                  and data[OnOffstart + (j) * OnOffblockSize + 1] == 0x00
                  and data[OnOffstart + (j) * OnOffblockSize + 2] == 0x00
                  and data[OnOffstart + (j) * OnOffblockSize + 3] == 0x00 ):
                break
            currName = ""
            for i in range(12):
                if data[OnOffstart + j * OnOffblockSize + i] == 0x00:
                    break
                currName = currName + chr(data[OnOffstart + j * OnOffblockSize + i])
            name.append(currName)
            mmax.append(    data[OnOffstart + j * OnOffblockSize + 12] + 
                            data[OnOffstart + j * OnOffblockSize + 13] * 256)
            mdefault.append(data[OnOffstart + j * OnOffblockSize + 16] + 
                            data[OnOffstart + j * OnOffblockSize + 17] * 256)
            if data[OnOffstart + j * OnOffblockSize + 0x2C]:
                mpedal.append(True)
            else:
                mpedal.append(False)
            #print(mmax[j])
            #print(mdefault[j])
            """
            print("[{}] {} {} {} {}".format(
            OnOffstart + (j+1) * OnOffblockSize,
            hex(data[OnOffstart + (j+1) * OnOffblockSize]),
            hex(data[OnOffstart + (j+1) * OnOffblockSize + 1]),
            hex(data[OnOffstart + (j+1) * OnOffblockSize + 2]),
            hex(data[OnOffstart + (j+1) * OnOffblockSize + 3])) )
            """

            #print("increment params")
            numParameters = numParameters + 1

        #print("Found {} parameters.".format(numParameters))
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
        for i in range(numParameters - 2):
            #print(i)
            tD['Parameters'].append({'name': name[i+2], 'mmax': mmax[i + 2], 'mdefault': mdefault[i + 2], 'pedal': mpedal[i+2]})
        
        #json.dump(tD, sys.stdout, indent=4)
        f = open(fxName+'.json', "w")
        json.dump(tD, f, indent=4)
        f.close()
        return fxName+'.ZDL'
    else:
        return None

if __name__ == "__main__":
    if len(sys.argv) == 2:
        f = open(sys.argv[1], "rb")
        # we are looking for 6 bytes then 0000000053495A45
        # lets assume the pattern will be past 6th bytearray
        # and we need at least 8 bytes left to read pattern
        rawX = f.read()
        f.close()
        ZDL=bytearray()
        # note the loop variable is updated in the loop!
        for i in range(len(rawX) - 8):
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
                # should be beginning of a block ... so prevBlock should be FFFF
                if prevBlock != 65535:
                    print("Something wrong with this ZDL")
                else:
                    # now we got to keep going, sizeBlock at a time,
                    # a block will always be max 4090 large. Even if we get less
                    # the contents will be padded with FF
                    blockCount = 0
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
                    if nextBlock == 0xFFFF:
                        blockCount = blockCount + 1
                        ZDL.extend(rawX[i:i + sizeBlock])
                        # still must take a whole block
                        i = i + 4096
                        # now write out the ZDL. Function writes out JSON
                        #print(ZDL)                        
                        fxnamefile = check(ZDL) 
                        if None == fxnamefile:
                            continue
                         
                        g = open(fxnamefile, "wb")
                        g.write(ZDL)
                        g.close()
                        ZDL=bytearray()
                        print("{}  {}".format(fxnamefile, blockCount))
