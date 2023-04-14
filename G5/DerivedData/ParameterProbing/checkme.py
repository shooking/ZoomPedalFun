# -*- coding: ascii -*-
import sys
import json

def check(data):
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
        try:
            # this is WAY too large, let except break the loop
            for j in range(0, 2000):
                """
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
                """
                currName = ""
                for i in range(12):
                    if data[OnOffstart + j * OnOffblockSize + i] == 0x00:
                        break
                    currName = currName + chr(data[OnOffstart + j * OnOffblockSize + i])
                    if data[OnOffstart + j * OnOffblockSize + i] & 0x80:
                        raise Exception("Non binary char")
                if currName == "":
                    break
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
        except:
            # The idea here is we probe 2000 parameters and expect to go past end
            # so we expect to hit an exception.cd
            pass
        #print("Found {} parameters.".format(numParameters))
        tD['Parameters'] = []
        # 0 is the OnOff state
        # 1 is the name
        # so actual paramters start from index 2, but clearly there are 2 less
        for i in range(numParameters - 2):
            #print(i)
            tD['Parameters'].append({'name': name[i+2], 'mmax': mmax[i + 2], 'mdefault': mdefault[i + 2], 'pedal': mpedal[i+2]})
        
        #json.dump(tD, sys.stdout, indent=4)
        with open(fxName+'.json', "w") as f:
            json.dump(tD, f, indent=4)
        return fxName+'.OnOff'
    return None

# handles a zoom firmware
if __name__ == "__main__":
    if len(sys.argv) == 2:
        with open(sys.argv[1], "rb") as f:
            data = f.read()

        x = check(data)
        print(x)