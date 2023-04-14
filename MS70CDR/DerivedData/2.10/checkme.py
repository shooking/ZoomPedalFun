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
        for j in range(0, 20):
            if  not ( data[OnOffstart + (j+1) * OnOffblockSize - 1] == 0x00
                 and  data[OnOffstart + (j+1) * OnOffblockSize - 2] == 0x00):
                # ZD2 format has a length and PRME offset. ZDL has none of this.
                print("End of the parameters")
                break;
            if not (      data[OnOffstart + (j) * OnOffblockSize + 0x18  ] == 0x00
                  and data[OnOffstart + (j) * OnOffblockSize + 0x19] == 0x00
                  and data[OnOffstart + (j) * OnOffblockSize + 0x1A] == 0x00
                  and data[OnOffstart + (j) * OnOffblockSize + 0x1B] == 0x00 ):
                print("Empty next slot")
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
                            data[OnOffstart + j * OnOffblockSize + 17] * 256);
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
<<<<<<< HEAD
        f = open(fxName+'.json', "w")
        json.dump(tD, f, indent=4)
        f.close()
        return fxName+'.ZDL'
    return None
=======
        with open(fxName+'.json', "w") as f:
            json.dump(tD, f, indent=4)
            return fxName+'.ZDL'
    return "Not found!"

>>>>>>> 3abe0579e765d544010bdc30dc0b204a26a0619d

# handles a processed ZDL
# if you want to extract from the firmware you have to
# read the fileblocks and handle appropriately.
if __name__ == "__main__":
    if len(sys.argv) == 2:
        with open(sys.argv[1], "rb") as f:
            data = f.read()
<<<<<<< HEAD

        check(data)
=======
            res = check(data)
            print(res)
>>>>>>> 3abe0579e765d544010bdc30dc0b204a26a0619d
