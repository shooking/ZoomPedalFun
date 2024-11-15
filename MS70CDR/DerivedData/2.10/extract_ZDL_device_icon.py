# See https://github.com/ELynx/zoom-fx-modding for original extraction code
# credit to above
# WARNING GLOBALS BELOW

# as composed from 64 lines of pixels
screen = []
# rather arbitrary, I know    
zdl_width = 128
zdl_x = 0
zdl_y0 = 0
# Extract images embedded in the ELF/Code section of ZD2 file

from PIL import Image
import numpy as np


def addEightLines():
    global screen
    for i in range(8):
        screen.append("")

# write a byte as bits, thus to 8 lines
def outputByte(toOutput):
    global screen
    global zdl_x
    global zdl_y0

    alreadyLines = len(screen)
    if (alreadyLines <= zdl_y0):
        if (alreadyLines < 64):
            # before we fill 64 lines, just go at it
            addEightLines()
        else:
            # gracefully allow padding if it is padded with 0x00
            if(toOutput == "00000000"):
                print("Padding detected, ignoring")
                return
            else:
                print("WARNING, overrun")
                addEightLines()

    # k is the bit in byte
    for k in range(0,8):
        screen[zdl_y0 + k] += toOutput[7 - k]
        
    # move to next x ...
    zdl_x = zdl_x + 1
    
    # until arrive to end of line, then move to next 8 lines
    if (zdl_x == zdl_width):
        zdl_x = 0
        zdl_y0 = zdl_y0 + 8

def doStuff(inputBytes):
    # these should not appear since values are always composed of 1s and 0s
    twoBefore = "zzzzzzzz"
    oneBefore = "yyyyyyyy"
    
    for byteIndex in range(len(inputBytes)):
        actual = inputBytes[byteIndex]
        
        # take binary form, remove 0b prefix
        binary = bin(actual)[2:]
        # fill up to 8 bits
        binary = "0" * (8 - len(binary)) + binary
        
       # print("Consuming byte " + str(byteIndex) + " with value of " + str(actual) + " / " + binary)
    
        if (twoBefore == oneBefore):
           # print("Found repeat instruction, printing repeats")
            for i in range(actual):
                outputByte(oneBefore)
            # reset repeats detection
            twoBefore = "zzzzzzzz"
            oneBefore = "yyyyyyyy"
        else:
           #print("Found regular, printing as is")
            outputByte(binary)
            # do not forget to shift both detections
            twoBefore = oneBefore
            oneBefore = binary
    
    print("Result is")
    
    for l in range(len(screen)):
        print(screen[l].replace("0", "░").replace("1", "█"))
    
    return screen
    print("Done")
    

# see https://github.com/mungewell/zoom-zt2
# for this part (I modified it)
#--------------------------------------------------
def main():
    from argparse import ArgumentParser
    from sys import exit
    from re import match

    # from https://github.com/sashs/filebytes
    from filebytes.elf import ELF

    parser = ArgumentParser(prog="extract_device_icon")

    parser.add_argument('files', metavar='FILE', nargs=1,
        help='File to process')
    parser.add_argument("-e", "--elf",
        help="read elf directly, rather than ZD2",
        action="store_true", dest="elf")

    parser.add_argument("-l", "--list",
        help="list available symbols",
        action="store_true", dest="list")
    parser.add_argument("-t", "--target",
        default = "_*picTotalDisplay_.*", dest="target",
        help="regex to describe target icon (_*picTotalDisplay_.*)")
    parser.add_argument("-S", "--skip",
        default = 0, type=int,
        help="skip a number of targets when found", dest="skip")
    parser.add_argument("-s", "--stripes",
        default = 4, type=int,
        help="number of 'stripes' in image", dest="stripes")

    parser.add_argument("-r", "--raw",
        help="saw as raw bytes",
        action="store_true", dest="raw")
    parser.add_argument("-o", "--output",
        help="output image to FILE", dest="output")

    options = parser.parse_args()

    e = None
    if options.elf:
        # Read ELF file directly from disk
        e = ELF(options.files[0])
    else:
        print("This program requires ELF input. Exiting")

    if not e:
        exit("Error in reading ELF file")

    a = None
    l = None
    rawData = None

    for s in e.sections:
        if s.name == '.symtab':
            if options.list:
                for z in s.symbols:
                    print(z.name)
                quit()

            for z in s.symbols:
                if match(options.target, z.name):
                    print("Target matched:", z.name)
                    if options.skip:
                        options.skip -= 1
                    elif z.header.st_size:
                        a = z.header.st_value
                        l = z.header.st_size
                        break

    if not l:
        exit("Target not found: " + options.target)

    for s in e.segments:
        if a >= s.vaddr and a < (s.vaddr + len(s.bytes)): 
            print("Symbol located:", hex(a))
            rawData = bytes(s.bytes[a - s.vaddr : a - s.vaddr + l])
            break

    if rawData:
        # ZDLs appear to be 64 x 128
        theImage = doStuff(rawData)
        array = np.zeros([128, 128], dtype=np.uint8)
        #print(len(theImage))
        for imRow in range(len(theImage)):
            #print(len(theImage[imRow]))
            for imCol in range(128):
                array[2 * imRow, imCol] = 0 if (theImage[imRow][imCol] =='1') else 255
                array[1 + 2 * imRow, imCol] = 0 if (theImage[imRow][imCol] =='1') else 255
        #print(theImage)
        img2 = Image.fromarray(array)
        
        if options.output:
            img2.save(options.output)
        else:
            img2.save("icon.png")

if __name__ == "__main__":
    main()

