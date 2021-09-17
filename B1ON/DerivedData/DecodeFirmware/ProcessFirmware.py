import sys
import os
import glob
from csplitb import CSplitB



# -*- coding: ascii -*-
import sys
import json

def check(name):
    f = open(name, "rb")
    f.read(64)
    x = f.read(8)
    data = f.read()
    f.close()
    # try to find name. Is is 0x30 chars from OnOff
    OnOffstart = data.find("OnOff".encode())
    fxName=""
    for j in range(12):
        if data[OnOffstart + j + 0x30] == 0x00:
            break
        fxName = fxName + chr(data[OnOffstart + j + 0x30])

    #print( "{} {} {} {}".format( hex(x[0]), hex(x[1]), hex(x[2]), hex(x[3]) ) )
    mult = 256
    tD = {
            "filename": name,
            "fxname" :fxName
         }
    if x[2] & 0xC0 == 0:
        tD['fxid'] = str(hex( x[1] * mult + x[0] ))
        tD['gid'] = str(hex(x[3]) )
        """
        print("{} {}\t\t{} {} {}{}{}{}".format(name, fxName, str(hex( x[1] * mult + x[0] )), str(hex(x[3]) ),
            chr(x[4]), chr(x[5]), chr(x[6]), chr(x[7])) )
        """
    else:
        tD['fxid'] = str(hex( x[1] * mult + x[0] ))
        tD['gid'] = str(hex( ( (x[3] * mult) + (x[2] & 0xC0)) >>4 ) )
        """
        print("{} {} \t\t{} {} {}{}{}{}".format(name, fxName, str(hex( x[1] * mult + x[0] )), str(hex(( (x[3] * mult) + (x[2] & 0xC0)) >> 4) ),
            chr(x[4]), chr(x[5]), chr(x[6]), chr(x[7])) )
        """
    tD['version'] = "{}{}{}{}".format(chr(x[4]), chr(x[5]), chr(x[6]), chr(x[7]) )

    json.dump(tD, sys.stdout, indent=4)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        csplitb = CSplitB("0000000053495A45", sys.argv[1], 3, "FX", ".ZDL")
        csplitb.run()
        for file in glob.glob(r"*.ZDL"):
            check(file)
