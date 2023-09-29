inputBytes = [
 0xfe,
 0x03,
 0xc1,
 0xe1,
 0xa1,
 0xe1,
 0xc1,
 0x01,
 0x01,
 0xc1,
 0xe1,
 0xa1,
 0xe1,
 0xc1,
 0x01,
 0x01,
 0xc1,
 0xe1,
 0xa1,
 0xe1,
 0xc1,
 0x03,
 0xfe,
 0xff,
 0x20,
 0x21,
 0x23,
 0x23,
 0x23,
 0x21,
 0x20,
 0x20,
 0x21,
 0x23,
 0x23,
 0x23,
 0x21,
 0x20,
 0x20,
 0x21,
 0x23,
 0x23,
 0x23,
 0x21,
 0x20,
 0xff,
 0xff,
 0x00,
 0xc0,
 0x40,
 0x80,
 0x00,
 0xc0,
 0x5f,
 0x40,
 0x1f,
 0xd1,
 0x11,
 0x00,
 0x1f,
 0xd5,
 0x55,
 0xc0,
 0x00,
 0xc0,
 0x00,
 0xc0,
 0x00,
 0xff,
 0x1f,
 0x30,
 0x27,
 0x24,
 0x23,
 0x20,
 0x27,
 0x25,
 0x25,
 0x20,
 0x27,
 0x24,
 0x24,
 0x20,
 0x27,
 0x21,
 0x27,
 0x20,
 0x21,
 0x27,
 0x21,
 0x30,
 0x1f,
 0x00,
 0x00,
 0x00,
 0x00
]

# rather arbitrary, I know
width = 23
height = 30
# WARNING GLOBALS BELOW

# as composed from 64 lines of pixxxels
screen = []

x = 0
y0 = 0

def addEightLines():
    global screen
    global y0
    for i in range(8):
        screen.append("")
        if y0 + i >=  height:
            break

# write a byte as bits, thus to 8 lines
def outputByte(toOutput):
    global screen
    global x
    global y0

    alreadyLines = len(screen)
    if (alreadyLines <= y0):
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
        if y0 + k >=  height:
            break
        screen[y0 + k] += toOutput[7 - k]
        
    # move to next x ...
    x = x + 1
    
    # until arrive to end of line, then move to next 8 lines
    if (x == width):
        x = 0
        y0 = y0 + 8 # bits in byte

for byteIndex in range(len(inputBytes)):
    actual = inputBytes[byteIndex]
    
    # take binary form, remove 0b prefix
    binary = bin(actual)[2:]
    # fill up to 8 bits
    binary = "0" * (8 - len(binary)) + binary
    
    #print("Consuming byte " + str(byteIndex) + " with value of " + str(actual) + " / " + binary)

    outputByte(binary)

print(f'Result is {len(screen)}')

for l in range(len(screen)):
    print(screen[l].replace("0", "░").replace("1", "█"))

print("Done")
for l in range(len(screen)):
    print(screen[l])