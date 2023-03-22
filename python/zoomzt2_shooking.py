#!/usr/bin/python
#
# Script decode/encode ZT2 file from Zoom F/W
# (c) Simon Wood, 11 July 2019
#

from construct import *
import re
# some of the files have traiing ,
# json5 accepts this, but is slower than json.
import json5
import json
import math
import logging
logging.basicConfig(filename='midi.log', level=logging.DEBUG)

#gidMask = 0x0FFFFFFF
gidMask = 0xFFFFFFFF
fxidMask = 0xFFFF
#--------------------------------------------------
# Define ZT2/ZD2 file format using Construct (v2.10)
# requires:
# https://github.com/construct/construct

Header = Struct(
    "a" / Const(b"\x3e\x3e\x3e\x00"),
    "b" / Padding(22),
    "name" / PaddedString(12, "ascii"),
    "c" / Padding(6),
    "d" / Const(b"\x01"),
    "e" / Padding(7),
    "f" / Const(b"\x3c\x3c\x3c\x00"),
    "g" / Padding(22),
)

Effect = Struct(
    "effect" / PaddedString(12, "ascii"),
    Const(b"\x00"),
    "version" / PaddedString(4, "ascii"),
    Const(b"\x00"),
    "installed" / Default(Byte, 1),     # "Guitar Lab additional effects" = 0
    "id" / Int32ul,
    "group" / Computed((this.id & 0xFF000000) >> 24),
    Check(this.group == this._.group),
    Const(b"\x00\x00\x00"),
)

Group = Struct(
    Const(b"\x3e\x3e\x3e\x00"),
    "group" / Byte,
    "groupname" / Enum(Computed(this.group),
        DYNAMICS = 1,
    FILTER = 2,
    DRIVE = 3,
    AMP = 4,
    CABINET = 5,
    MODULATION = 6,
    SFX = 7,
    DELAY = 8,
    REVERB = 9,
    PEDAL = 11,
    AG_MODEL = 20,
    ACOUSTIC = 29,
    ),
    Padding(21),
    "effects" / GreedyRange(Effect),
    Const(b"\x3c\x3c\x3c\x00"),
    "group_end" / Rebuild(Byte, this.group),
    Check(this.group_end == this.group),
    Padding(21),
)

ZT2 = Padded(8502, Sequence(
    "header" / Header,
    "groups" / GreedyRange(Group),
))

ICON = Struct(
        Const(b"ICON"),
        "length" / Int32ul,
        "data" / Bytes(this.length),
)

TXJ1 = Struct(
    Const(b"TXJ1"),
    "length" / Int32ul,
    Padding(this.length),
)

TXE1 = Struct(
    Const(b"TXE1"),
    "length" / Int32ul,
    "name" / PaddedString(this.length, "ascii"),
)

INFO = Struct(
        Const(b"INFO"),
        "length" / Int32ul,
        "data" / Bytes(this.length),
)

DATA = Struct(
        Const(b"DATA"),
        "length" / Int32ul,
        "data" / Bytes(this.length),
)

PRMJ = Struct(
        Const(b"PRMJ"),
        "length" / Int32ul,
        "data" / Bytes(this.length),
)

PRME = Struct(
        Const(b"PRME"),
        "length" / Int32ul,
        "data" / PaddedString(this.length, "ascii"),
)

# should be able to just import this in ??
ZD2 = Struct(
    Const(b"ZDLF"),
    "length" / Int32ul,
    "unknown" / Bytes(81),
    "version" / PaddedString(4, "ascii"),
    Const(b"\x00\x00"),
    "group" / Byte,
    "id" / Int32ul,
    "name" / CString("ascii"),
    "unknown2" / Bytes(lambda this: 10 - len(this.name)),
    "groupname" / CString("ascii"),
    "unknown3" / Bytes(lambda this: 16 - len(this.groupname)),
    "ICON" / ICON,
    "TXJ1" / TXJ1,
    "TXE1" / TXE1,
    "INFO" / INFO,
    "DATA" / DATA,
    "PRMJ" / PRMJ,
    "PRME" / PRME,
)


EDTB2 = Struct( # Working with a Byte-reversed copy of data
    Padding(9),
    "control" / Bitwise(Struct(
        Padding(6),
        "param8" / BitsInteger(8),
        "param7" / BitsInteger(8),
        "param6" / BitsInteger(8),
        "param5" / BitsInteger(12),
        "param4" / BitsInteger(12),
        "param3" / BitsInteger(12),
        "param2" / BitsInteger(12),
        "param1" / BitsInteger(12),
        "unknown" / Bit, # always '0', so far
        "id" / BitsInteger(28),
        "enabled" / Flag,
    )),
)

EDTB1 = Struct(
    #"dump" / Peek(HexDump(Bytes(24))),
    "autorev" / ByteSwapped(Bytes(24)),
    "reversed" / RestreamData(this.autorev, EDTB2), # this does not allow re-build of data :-(
)

EDTB = Struct(
    Const(b"EDTB"),
    "length" / Int32ul,
    "effects" / Array(this._.fx_count, EDTB1),
)

PPRM = Struct(
    Const(b"PPRM"),
    "length" / Int32ul,
    #"pprm_dump" / Peek(HexDump(Bytes(this.length))),
    Padding(this.length),
)

ZPTC = Padded(760, Struct(
    Const(b"PTCF"),
    Padding(8),
    "fx_count" / Int32ul,
    Padding(10),
    "name" / PaddedString(10, "ascii"),
    "ids" / Array(this.fx_count, Int32ul),

    "TXJ1" / TXJ1,
    "TXE1" / TXE1,
    "EDTB" / EDTB,
    "PPRM" / PPRM,
))

#--------------------------------------------------
import os
import sys
import mido
import binascii
from time import sleep

def printhex(direct, msg):
    logging.info(direct)
    l = []
    numchar=0
    for n in msg:
        l.append(n)
        numchar=numchar+1
        if numchar % 16 == 0:
            logging.info(" ".join( "{0:#0{1}x}".format(int( m ), 4) for m in l))
            l = []
    if l is not None:
        logging.info(" ".join( "{0:#0{1}x}".format(int( m ), 4) for m in l))
        
def printExtrahex(direct, msg):
    logging.info(direct + "0xf0 ")
    printhex(direct, msg)
    logging.info(direct + " 0xf7 ")


def sniffMidiOut(mtype, data, printme = False):

    logging.info("MIDI OUT")
    if printme == True:
        logging.info("sniffMidiOut")
        if mtype == "sysex":
            printExtrahex("===>    ", data)
        else:
            printhex("===>    ", data)
    return mido.Message(mtype, data = data)


def sniffMidiIn(self, printme = False):

    logging.info("MIDI IN")
    msg = self.inport.receive()
    if printme == True:
        logging.info("sniffMidiIn")
        if msg.type == "sysex":
            printExtrahex("<====    ", msg.data)
        else:
            printhex("<====    ", msg.data)
    return msg


if sys.platform == 'win32':
    mido.set_backend('mido.backends.rtmidi_python')
    midiname = b"ZOOM G"
else:
    midiname = "ZOOM G"

class zoomzt2(object):
    inport = None
    outport = None
    model = None
    numPatches = 0
    bankSize = 0
    ptcSize = 0
    version = 0
    gce3version = 0
    maxFX = 0
    def is_connected(self):
        if self.inport == None or self.outport == None:
            return(False)
        else:
            return(True)

    def connect(self):
        for port in mido.get_input_names():
            logging.info("{}, {}".format(port, midiname))
            if port[:len(midiname)]==midiname:
                self.inport = mido.open_input(port)
                #print("Using Input:", port)
                break
        for port in mido.get_output_names():
            logging.info("{}".format(port))
            if port[:len(midiname)]==midiname:
                self.outport = mido.open_output(port)
                #print("Using Output:", port)
                break

        if self.inport == None or self.outport == None:
            #print("Unable to find Pedal")
            return(False)

        # ask pedal for some info

        logging.info("Grab Pedal Info")
        data = [0x52, 0x00, 0x6e, 0x50]
        msg = sniffMidiOut("sysex", data)
        self.outport.send(msg); sleep(0); msg = sniffMidiIn(self)

        data = [0x7e, 0x00, 0x06, 0x01]
        msg = sniffMidiOut("sysex", data)
        self.outport.send(msg); sleep(0); msg = sniffMidiIn(self)
        d = msg.data
        print(d)
        if len(d) < 12:
            print("odd - too short")
            sys.exit(1)
        if d[5] == 0x6e and d[6] == 0x00 and d[7] == 0x10:
            # a Zoom GCE-3
            self.gce3version = chr(d[9]) + chr(d[10]) + chr(d[11]) + chr(d[12])
            # check model
            data = [0x52, 0x00, 0x6e, 0x58, 0x02]
            msg = sniffMidiOut("sysex", data)
            self.outport.send(msg); sleep(0); msg = sniffMidiIn(self)
            d = msg.data
            if d[5] == 0x6e and d[6] == 0x00:
                if   d[7] == 0x00:
                    self.model = "G5n"
                    self.version = "3.00"
                    self.maxFX = 9
                elif d[7] == 0x02:
                    self.model = "G3n"
                    self.version = "2.20"
                    self.maxFX = 7
                elif d[7] == 0x03:
                    self.model = "G3Xn"
                    self.version = "2.20"
                    self.maxFX = 7
                elif d[7] == 0x04:
                    self.model = "B3n"
                    self.version = "2.20"
                    self.maxFX = 7
                elif d[7] == 0x0c:
                    self.model = "G1 Four"
                    self.version = "2.00"
                    self.maxFX = 5
                elif d[7] == 0x0d:
                    self.model = "G1X Four"
                    self.version = "2.00"
                    self.maxFX = 5
                elif d[7] == 0x0e:
                    self.model = "B1 FOUR"
                    self.version = "2.00"
                    self.maxFX = 5
                elif d[7] == 0x0f:
                    self.model = "B1X Four"
                    self.version = "2.00"
                    self.maxFX = 5
                elif d[7] == 0x10:
                    self.model = "GCE-3" # aguess
                    self.version = "1.20"
                    self.maxFX = 5
                elif d[7] == 0x11:
                    self.model = "A1 Four"
                    self.version = "1.01"
                elif d[7] == 0x12:
                    self.model = "A1X Four"
                    self.version = "1.01"
                    self.maxFX = 5
                elif d[7] == 0x13:
                    self.model = "??"
                    self.version = "1.50"
                    self.maxFX = 5
                elif d[7] == 0x17:
                    self.model = "??"
                    self.version = "1.30"
                    self.maxFX = 5
                elif d[7] == 0x19:
                    self.model = "??"
                    self.version = "1.30"
                    self.maxFX = 5
        elif d[5] == 0x6e and d[6] == 0x00:
            self.version = chr(d[9]) + chr(d[10]) + chr(d[11]) + chr(d[12])
            if   d[7] == 0x00:
                self.model = "G5n"
                self.maxFX = 9
            elif d[7] == 0x02:
                self.model = "G3n"
                self.maxFX = 7
            elif d[7] == 0x03:
                self.model = "G3Xn"
                self.maxFX = 7
            elif d[7] == 0x04:
                self.model = "B3n"
                self.maxFX = 7
            elif d[7] == 0x0c:
                self.model = "G1 Four"
                self.maxFX = 5
            elif d[7] == 0x0d:
                self.model = "G1X Four"
                self.maxFX = 5
            elif d[7] == 0x0e:
                self.model = "B1 FOUR"
                self.maxFX = 5
            elif d[7] == 0x0f:
                self.model = "B1X Four"
                self.maxFX = 5
            elif d[7] == 0x10:
                self.model = "GCE-3" # aguess
                self.version = "1.20"
                self.maxFX = 5
            elif d[7] == 0x11:
                self.model = "A1 Four"
                self.maxFX = 5
            elif d[7] == 0x12:
                self.model = "A1X Four"
                self.maxFX = 5
            elif d[7] == 0x13:
                self.model = "??"
                self.maxFX = 5
            elif d[7] == 0x17:
                self.model = "??"
                self.maxFX = 5
            elif d[7] == 0x19:
                self.model = "??"
                self.maxFX = 5
        # how big is patch etc
        data = [0x52, 0x00, 0x6e, 0x44]
        msg = sniffMidiOut("sysex", data)
        self.outport.send(msg); sleep(0); msg = sniffMidiIn(self)
        d = msg.data
        self.numPatches = d[5] * 128 + d[4]
        self.bankSize = d[11] * 128 + d[10]
        self.ptcSize = d[7] * 128 + d[6]

        # write out pedal state
        out1 = open("model.dat", "w")
        if not out1:
            sys.exit("Unable to open FILE for writing")
        tD = {
                "model": self.model,
                "numPatches": self.numPatches,
                "bankSize": self.bankSize,
                "ptcSize": self.ptcSize,
                "version": self.version,
                "gce3version": self.gce3version,
                "maxFX": self.maxFX
            }
        print(tD)
        json.dump(tD, out1, indent = 6)
        out1.close()

        # Enable PC Mode
        logging.info("Enable PC Mode")
        data = [0x52, 0x00, 0x6e, 0x52]
        msg = sniffMidiOut("sysex", data)
        #msg = mido.Message("sysex", data = [0x52, 0x00, 0x6e, 0x52])
        self.outport.send(msg); sleep(0); msg = sniffMidiIn(self)
        return(True)

    def disconnect(self):
        # Disable PC Mode
        logging.info("Disable PC Mode")
        data = [0x52, 0x00, 0x6e, 0x53]
        msg = sniffMidiOut("sysex", data)
        #msg = mido.Message("sysex", data = [0x52, 0x00, 0x6e, 0x53])
        self.outport.send(msg); sleep(0); msg = sniffMidiIn(self)

        self.inport = None
        self.outport = None

    def pack(self, data):
        # Pack 8bit data into 7bit, MSB's in first byte followed
        # by 7 bytes (bits 6..0).
        packet = bytearray(b"")
        encode = bytearray(b"\x00")

        for byte in data:
            encode[0] = encode[0] + ((byte & 0x80) >> len(encode))
            encode.append(byte & 0x7f)

            if len(encode) > 7:
                packet = packet + encode
                encode = bytearray(b"\x00")

        # don't forget to add last few bytes
        if len(encode) > 1:
            packet = packet + encode

        return(packet)

    def unpack(self, packet):
        # Unpack data 7bit to 8bit, MSBs in first byte
        logging.info("Packet length {}".format(len(packet)))
        data = bytearray(b"")
        loop = -1
        hibits = 0

        for byte in packet:
            if loop !=-1:
                if (hibits & (2**loop)):
                    data.append(128 + byte)
                else:
                    data.append(byte)
                loop = loop - 1
            else:
                hibits = byte
                # do we need to acount for short sets (at end of block block)?
                loop = 6

        return(data)

    def add_effect(self, data, name, version, id):
        logging.info("add_effect")
        config = ZT2.parse(data)
        head, tail = os.path.split(name)
        
        group_new = (id & 0xFF000000) >> 24
        group_found = False

        for group in config[1]:
            if group['group'] == group_new:
                group_found = True
                effects = group['effects']
                slice = 0
                for effect in effects:
                    if effect['effect'] == tail:
                        del effects[slice]
                    slice = slice + 1

                new = dict(effect=tail, version=version, id=id)
                effects.append(new)

        if not group_found:
            effects = []
            new = dict(effect=tail, version=version, id=id, group=group_new)
            effects.append(new)
            new = dict(group=group_new, groupname=group_new, effects=effects, groupend=group_new)
            config[1].append(new)

        return ZT2.build(config)

    def add_effect_from_filename(self, data, name):
        binfile = open(name, "rb")
        if binfile:
            bindata = binfile.read()
            binfile.close()

            binconfig = ZD2.parse(bindata)
            head, tail = os.path.split(name)

            return self.add_effect(data, tail, binconfig['version'], binconfig['id'])
        return data


    def remove_effect(self, data, name):
        config = ZT2.parse(data)
        head, tail = os.path.split(name)
        
        for group in config[1]:
            effects = group['effects']
            slice = 0
            for effect in effects:
                if effect['effect'] == tail:
                    del effects[slice]
                slice = slice + 1

        return ZT2.build(config)

    def filename(self, packet, name):
        # send filename (with different packet headers)
        logging.info(" send filename (with different packet headers")
        head, tail = os.path.split(name)
        for x in range(len(tail)):
            packet.append(ord(tail[x]))
        packet.append(0x00)

        msg = sniffMidiOut("sysex", data = packet)
        #msg = mido.Message("sysex", data = packet)
        self.outport.send(msg); sleep(0); msg = sniffMidiIn(self)
        return(msg)

    def file_check(self, name):
        # check file is present on device
        logging.info(" Checking file is present on device")
        packet = bytearray(b"\x52\x00\x6e\x60\x25\x00\x00")
        head, tail = os.path.split(name)
        self.filename(packet, tail)

        data = [0x52, 0x00, 0x6e, 0x60, 0x05, 0x00]
        msg = sniffMidiOut("sysex", data)
        #msg = mido.Message("sysex", data = [0x52, 0x00, 0x6e, 0x60, 0x05, 0x00])
        self.outport.send(msg); sleep(0); msg = sniffMidiIn(self)
        logging.info(msg)
        if msg.data[6] == 127 and msg.data[7] == 127:
            return(False)
        logging.info("We are checking the file HERE")
        data = [0x52, 0x00, 0x6e, 0x60, 0x27]
        msg = sniffMidiOut("sysex", data = data)
        #msg = mido.Message("sysex", data = [0x52, 0x00, 0x6e, 0x60, 0x27])
        self.outport.send(msg); sleep(0); msg = sniffMidiIn(self)
        logging.info(msg)
        return(True)
    
    def file_wild(self, first):
        if first:
            packet = bytearray(b"\x52\x00\x6e\x60\x25\x00\x00")
        else:
            packet = bytearray(b"\x52\x00\x6e\x60\x26\x00\x00")
        msg = self.filename(packet, "*")

        if msg.data[4] == 4:
            for x in range(14,27):
                if msg.data[x] == 0:
                    return bytes(msg.data[14:x]).decode("utf-8")
        else:
            return ""

    def file_download(self, name):
        # download file from pedal to PC
        logging.info("In file_download {}".format(name))
        packet = bytearray(b"\x52\x00\x6e\x60\x20\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00")
        logging.info("packet")
        head, tail = os.path.split(name)
        self.filename(packet, tail)

        msg = sniffMidiOut("sysex", data = packet)
        # msg = mido.Message("sysex", data = packet)
        self.outport.send(msg); sleep(0); msg = sniffMidiIn(self)
        
        # Read parts 1 through 17 - refers to FLST_SEQ, possibly larger
        data = bytearray(b"")
        while True:
            sData = [0x52, 0x00, 0x6e, 0x60, 0x05, 0x00]
            msg = sniffMidiOut("sysex", data=sData)
            #msg = mido.Message("sysex", data = [0x52, 0x00, 0x6e, 0x60, 0x05, 0x00])
            self.outport.send(msg); sleep(0); msg = sniffMidiIn(self)

            #sData = [0x52, 0x00, 0x6e, 0x60, 0x22, 0x14, 0x2f, 0x60, 0x00, 0x0c, 0x00, 0x04, 0x00, 0x00, 0x00]
            sData = [0x52, 0x00, 0x6e, 0x60, 0x22, 0x14, 0x2f, 0x60, 0x00, 0x0c, 0x00, 0x02, 0x00, 0x00, 0x00]
            msg = sniffMidiOut("sysex", data=sData)
            #msg = mido.Message("sysex", data = [0x52, 0x00, 0x6e, 0x60, 0x22, 0x14, 0x2f, 0x60, 0x00, 0x0c, 0x00, 0x04, 0x00, 0x00, 0x00])
            self.outport.send(msg); sleep(0); msg = sniffMidiIn(self)

            sData = [0x52, 0x00, 0x6e, 0x60, 0x05, 0x00]
            msg = sniffMidiOut("sysex", data=sData)
            #msg = mido.Message("sysex", data = [0x52, 0x00, 0x6e, 0x60, 0x05, 0x00])
            self.outport.send(msg); sleep(0); msg = sniffMidiIn(self)

            #decode received data
            packet = msg.data
            length = int(packet[9]) * 128 + int(packet[8])
            # 2047 is a "I dont exist"
            if length == 0 or length == 2047:
                logging.info("WE GOT ZERO LEN BACK")
                break
            block = self.unpack(packet[10:10 + length + int(length/7) + 1])

            #print("HERE IS THE BLOCK!! {} from {}".format(len(block), len(packet)+2))
            #printhex("BLOCK ", block, False)
            # confirm checksum (last 5 bytes of packet)
            # note: mido packet does not have SysEx prefix/postfix
            checksum = packet[-5] + (packet[-4] << 7) + (packet[-3] << 14) \
                    + (packet[-2] << 21) + ((packet[-1] & 0x0F) << 28) 
            if (checksum ^ 0xFFFFFFFF) == binascii.crc32(block):
                data = data + block
            else:
                logging.info("Checksum error {}".format(hex(checksum)))
                break
        return(data)

    def file_upload(self, name, data):
        packet = bytearray(b"\x52\x00\x6e\x60\x24")
        head, tail = os.path.split(name)
        self.filename(packet, tail)

        packet = bytearray(b"\x52\x00\x6e\x60\x20\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00")
        head, tail = os.path.split(name)
        self.filename(packet, tail)

        d1 = [0x52, 0x00, 0x6e, 0x60, 0x05, 0x00]
        msg = sniffMidiOut("sysex", d1 )
        # msg = mido.Message("sysex", data = [0x52, 0x00, 0x6e, 0x60, 0x05, 0x00])
        self.outport.send(msg); sleep(0); msg = sniffMidiIn(self)

        while len(data):
            packet = bytearray(b"\x52\x00\x6e\x60\x23\x40\x00\x00\x00\x00")
            if len(data) > 512:
                length = 512
            else:
                length = len(data)
            packet.append(length & 0x7f)
            packet.append((length >> 7) & 0x7f)
            packet = packet + bytearray(b"\x00\x00\x00")

            packet = packet + self.pack(data[:length])

            # Compute CRC32
            crc = binascii.crc32(data[:length]) ^ 0xFFFFFFFF
            packet.append(crc & 0x7f)
            packet.append((crc >> 7) & 0x7f)
            packet.append((crc >> 14) & 0x7f)
            packet.append((crc >> 21) & 0x7f)
            packet.append((crc >> 28) & 0x0f)

            data = data[length:]
            #print(hex(len(packet)), binascii.hexlify(packet))

            msg = sniffMidiOut("sysex", data = packet)
            # msg = mido.Message("sysex", data = packet)
            self.outport.send(msg); sleep(0); msg = sniffMidiIn(self)

            sData = [0x52, 0x00, 0x6e, 0x60, 0x05, 0x00]
            msg = sniffMidiOut("sysex", data = sData)
            # msg = mido.Message("sysex", data = [0x52, 0x00, 0x6e, 0x60, 0x05, 0x00])
            self.outport.send(msg); sleep(0); msg = sniffMidiIn(self)

    def file_delete(self, name):
        packet = bytearray(b"\x52\x00\x6e\x60\x24")
        head, tail = os.path.split(name)
        self.filename(packet, tail)

    def file_close(self):
        data = [0x52, 0x00, 0x6e, 0x60, 0x21, 0x40, 0x00, 0x00, 0x00, 0x00]
        msg = sniffMidiOut("sysex", data)
        #msg = mido.Message("sysex", data = [0x52, 0x00, 0x6e, 0x60, 0x21, 0x40, 0x00, 0x00, 0x00, 0x00])
        self.outport.send(msg); sleep(0); msg = sniffMidiIn(self)
        
        data = [0x52, 0x00, 0x6e, 0x60, 0x09]
        msg = sniffMidiOut("sysex", data)
        #msg = mido.Message("sysex", data = [0x52, 0x00, 0x6e, 0x60, 0x09])
        self.outport.send(msg); sleep(0); msg = sniffMidiIn(self)
 
 
    def patch_download(self, location):
        logging.info("patch_download")
        packet = bytearray(b"\x52\x00\x6e\x09\x00")
        #packet.append(int(location/10)-1)
        #packet.append(location % 10)
        a1=int(location / self.bankSize)
        b1=location % self.bankSize
        packet.append(a1)
        packet.append(b1)

        msg = sniffMidiOut("sysex", data = packet)
        #msg = mido.Message("sysex", data = packet)
        self.outport.send(msg); sleep(0); msg = sniffMidiIn(self)

        # decode received data
        packet = msg.data
        length = int(packet[8]) * 128 + int(packet[7])
        if length == 0:
            return()
        data = self.unpack(packet[9:9 + length + int(length/7) + 1])

        # confirm checksum (last 5 bytes of packet)
        checksum = packet[-5] + (packet[-4] << 7) + (packet[-3] << 14) \
                + (packet[-2] << 21) + ((packet[-1] & 0x0F) << 28) 

        if (checksum ^ 0xFFFFFFFF) != binascii.crc32(data):
            logging.info("Checksum error {}".format( hex(checksum)) )

        return(data)


    def patch_upload(self, location, data):
        packet = bytearray(b"\x52\x00\x6e\x08\x00")
        a1=int(location / self.bankSize)
        b1=location % self.bankSize
        packet.append(a1)
        packet.append(b1)

        length = len(data)
        packet.append(length & 0x7f)
        packet.append((length >> 7) & 0x7f)

        packet = packet + self.pack(data[:length])

        # Compute CRC32
        crc = binascii.crc32(data[:length]) ^ 0xFFFFFFFF
        packet.append(crc & 0x7f)
        packet.append((crc >> 7) & 0x7f)
        packet.append((crc >> 14) & 0x7f)
        packet.append((crc >> 21) & 0x7f)
        packet.append((crc >> 28) & 0x0f)

        #print(hex(len(packet)), binascii.hexlify(packet))

        msg = sniffMidiOut("sysex", data = packet)
        #msg = mido.Message("sysex", data = packet)
        self.outport.send(msg); sleep(0); msg = sniffMidiIn(self)

    '''
    def patch_download_current(self):
        packet = bytearray(b"\x52\x00\x6e\x29")

    def patch_upload_current(self, data):
        packet = bytearray(b"\x52\x00\x6e\x28")
    '''
    def getfile(self, name):
        logging.info("options.receive - getting {}".format(name))
        state = self.file_check(name)
        if (state == False):
            self.disconnect()
            sys.exit("Filename doesnt exist")
        data = self.file_download(name)        
        self.file_close()
        binconfig = ZD2.parse(data)

        # print("Writing ZD2")
        outfile = open(name, "wb")
        if not outfile:
            sys.exit("Unable to open FILE for writing")
        # print("data is ", len(data))
        outfile.write(data)
        outfile.close()

        # writing BMP
        outBMfile = open(name + ".BMP", "wb")
        if not outBMfile:
            sys.exit("Unable to open FILE for writing")
        outBMfile.write(binconfig['ICON']['data'])
        outBMfile.close()

        # A1X has training ,. So use json5 to parse it.
        x = json5.loads(binconfig['PRME']['data'])
        # lets find the OnOff

        # lets find the TXE1
        TXdescription = (binconfig['TXE1']['name']).replace('\r','').replace('\n','')

        logging.info("Desc {}".format( TXdescription))

        
        # lets find the OnOff
        OnOffstart = data.find("OnOff".encode())
        mmax = []
        mdefault = []
        if OnOffstart != 0:
            logging.info("In OnOffstart")
            for j in range(0, 10):
                mmax.append(data[OnOffstart + j * 0x38 + 12] + 
                    data[OnOffstart + j * 0x38 + 13] * 256)
                mdefault.append(data[OnOffstart + j * 0x38 + 16] + 
                data[OnOffstart + j * 0x38 + 17] * 256);

            numParams = len(x['Parameters'])
            for j in range(numParams):
                x['Parameters'][j]['mmax'] = mmax[j+2]
                x['Parameters'][j]['mdefault'] = mdefault[j+2]
            #print(x)
            # get description the hard way.
            # DIRTY SHOOKING HACK
            # If we find a A1X4 MDL (gid 34) make it 162
            myGid = ((binconfig['id'] & gidMask) >> 16) >> 5
            if myGid == 34:
                myGid = 34 + 128

            xAdd = {
                "FX" : 
                { 
                    "name": binconfig['name'],
                    "description": TXdescription,
                    "version": binconfig['version'],
                    "fxid": (binconfig['id'] & fxidMask),
                    "gid": myGid,
                    "group": binconfig['group'], 
                    "groupname": "{}" .format( binconfig['groupname']),
                    "numParams": numParams,
                    "numSlots": math.ceil(numParams / 4),
                    "filename": name + '.BMP'
                }
            }
            xAdd['Parameters'] = x['Parameters']
            out_file = open(name + ".json", "w")
            json.dump(xAdd, out_file, indent = 6)
            out_file.close()
            return xAdd 

    def allpatches(self, total_pedal = None, fxLookup = None):
        thesePatches = []
        for i in range(0, self.numPatches):
            print("processing patch {}".format(i))
            data = self.patch_download(i)
            outfile = open("patch_{}".format(i), "wb")
            if not outfile:
                sys.exit("Unable to open FILE for writing")
            outfile.write(data)
            outfile.close()
            thisPatch = {}
            if data:
                ZPTC = Padded(self.ptcSize, Struct(
                    Const(b"PTCF"),
                    Padding(8),
                    "fx_count" / Int32ul,
                    Padding(10),
                    "name" / PaddedString(10, "ascii"),
                    "ids" / Array(this.fx_count, Int32ul),
                    "TXJ1" / TXJ1,
                    "TXE1" / TXE1,
                    "EDTB" / EDTB,
                    "PPRM" / PPRM,
                ))

                config = ZPTC.parse(data)
                #print("PatchNumber: {}".format(i))
                numFX = (config['fx_count'])
                thisPatch['numFX'] = numFX
                patchName = (config['name'])
                thisPatch['patchname'] = patchName
                patchDescription = (config['TXE1']['name'])
                thisPatch['description'] = patchDescription
                logging.info ("Patch: {}".format(patchName))
                logging.info ("Desc: {}".format(patchDescription))
                theseFX = []
                for fx in config['EDTB']['effects']:
                    thisFX={}
                    idN = "id{}".format(fx)
                    effectN = "effect{}".format(fx)
                    #logging.info("  enabled: {}".format(config['EDTB'][effectN]['reversed']['control']['enabled']))
                    currID = fx['reversed']['control']['id']
                    if currID == 1:
                        # this is part of a multiFX
                        continue
                    logging.info("  FXID={}, GID={}".format(str(currID & fxidMask), str( ( (currID & gidMask)>>16)>>5) ) )
                    thisFX['fxid'] = (currID & fxidMask)
                    thisFX['gid'] = (currID & gidMask)>>21
                    thisFX['enabled'] = fx['reversed']['control']['enabled']
                    # assume numParameters is 8, unless we already looked up FX and have a hit.
                    np = 8
                    npi = -1
                    fxName=""
                    fxDescription=""
                    fxVersion=""
                    fxFilename=""
                    fxnumSlots=1
                    if fxLookup is not None and total_pedal is not None:
                        try:
                            # DIRTY SHOOKING HACK
                            # we dont have name (it is in a patch)
                            # Mungewell's decoder things id is 28 bits
                            # but we need the full 32.
                            # GID of 34 (and maybe others) needs to be 162
                            if thisFX['gid'] == 34:
                                thisFX['gid'] = 162 # 34 + 128

                            npi = fxLookup[thisFX['fxid'], thisFX['gid']]
                            baseFX = total_pedal[npi]['FX']
                            np = baseFX['numParams']
                            fxName = baseFX['name']
                            fxVersion = baseFX['version']
                            fxDescription = baseFX['description']
                            fxFilename = baseFX['filename']
                            fxnumSlots = baseFX['numSlots']
                        except KeyError:
                            logging.info("Exception looking up FXID: {} {} {} {} {}".format(thisFX['fxid'], \
                                    thisFX['gid'], patchName, currID, hex(int(currID))))
                            logging.info(fxLookup)
                            # hack - often these are loopers or rhythm.
                            fxnumSlots = 2
                            np = 8
                    thisFX['name'] = fxName
                    thisFX['description'] = fxDescription
                    thisFX['version'] = fxVersion
                    thisFX['numSlots'] = fxnumSlots
                    thisFX['filename'] = fxFilename
                    thisFX['Parameters'] = []
                    # might not want to make param1 param2?
                    for j in range(1,np+1):
                        pj = "param{}".format(j)
                        thisParam = {}
                        if npi != -1:
                            baseP = total_pedal[npi]['Parameters'][j - 1]
                            thisParam = {
                                    pj: fx['reversed']['control'][pj],
                                    "name" : baseP['name'],
                                    "explanation": baseP['explanation'],
                                    "blackback": baseP['blackback'],
                                    "pedal": baseP['pedal'],
                                    "mmax": baseP['mmax'],
                                    "mdefault": baseP['mdefault']
                                    }
                        else:
                            logging.info("   {} = {}".format(pj, fx['reversed']['control'][pj]))
                            thisParam = {pj: fx['reversed']['control'][pj]}
                        thisFX['Parameters'].append(thisParam)
 
                    theseFX.append(thisFX)
                thisPatch['FX'] = theseFX        
                logging.info(thisPatch)
                thesePatches.append(thisPatch)
        logging.info("PRINTING THESE PATCHES")
        logging.info(thesePatches)
        out_file = open("allpatches.json", "w")
        json.dump(thesePatches, out_file, indent = 4)
        out_file.close()
        
#--------------------------------------------------
def main():
    from optparse import OptionParser

    data = bytearray(b"")
    logging.info("in main .. data is ...")
    pedal = zoomzt2()

    usage = "usage: %prog [options] FILENAME"
    parser = OptionParser(usage)
    parser.add_option("-d", "--dump",
        help="dump configuration to text",
        action="store_true", dest="dump")
    parser.add_option("-s", "--summary",
        help="summarized configuration in human readable form",
    action="store_true", dest="summary")
    parser.add_option("-b", "--build",
        help="output commands required to build this FLTS_SEQ",
        dest="build")
    
    parser.add_option("-A", "--add",
        help="add effect to FLST_SEQ", dest="add")
    parser.add_option("-v", "--ver",
        help="effect version (use with --add)", dest="ver")
    parser.add_option("-i", "--id",
        help="effect id (use with --add)", dest="id")
    parser.add_option("-D", "--delete",
    help="delete effect from FLST_SEQ", dest="delete")
    
    parser.add_option("-t", "--toggle",
        help="toggle install/uninstall state of effect NAME in FLST_SEQ", dest="toggle")

    parser.add_option("-w", "--write", dest="write",
        help="write config back to same file", action="store_true")
    parser.add_option("-g", "--getfile",
        help="getfile from Zoom", dest="getfile")


    # interaction with attached device
    parser.add_option("-R", "--receive",
        help="Receive FLST_SEQ from attached device",
        action="store_true", dest="receive")
    parser.add_option("-S", "--send",
        help="Send FLST_SEQ to attached device",
        action="store_true", dest="send")
    parser.add_option("-I", "--install",
        help="Install effect binary to attached device", dest="install")
    parser.add_option("-U", "--uninstall",
        help="Remove effect binary from attached device", dest="uninstall")

    # attached device's effect patches
    parser.add_option("-p", "--patch",
        help="download specific patch (10..59)", dest="patch")
    # all attached device patches
    parser.add_option("-a", "--allpatches",
        help="download all patches (10..59)")
    parser.add_option("-P", "--upload",
        help="upload specific patch (10..59)", dest="upload")

    (options, args) = parser.parse_args()
    logging.info(options)
    logging.info(args)
    if len(args) != 1:
        parser.error("FILE not specified")

    if options.getfile:
        logging.info("options: ", options.getfile)
        logging.info("args[0] = ", args[0])

    if options.install and options.uninstall:
        sys.exit("Cannot use 'install' and 'uninstall' at same time")

    if options.patch:
        if int(options.patch) < 10 or int(options.patch) > 59:
            sys.exit("Patch number should be between 10 and 59")

    if options.upload:
        if int(options.upload) < 10 or int(options.upload) > 59:
            sys.exit("Patch number should be between 10 and 59")

    if options.receive or options.send or options.install or options.patch or options.upload or options.getfile:
        if not pedal.connect():
            sys.exit("Unable to find Pedal")

    if options.patch:
        logging.info("options.patch")
        data = pedal.patch_download(int(options.patch))
        pedal.disconnect()

        outfile = open(args[0], "wb")
        if not outfile:
            sys.exit("Unable to open FILE for writing")

        outfile.write(data)
        outfile.close()
        exit(0)

    if options.allpatches:
        logging.info("options.allpatches")

        pedal.allpatches()

        pedal.disconnect()

        exit(0)


    if options.upload:
        infile = open(args[0], "rb")
        if not infile:
            sys.exit("Unable to open FILE for reading")
        else:
            data = infile.read()
        infile.close()

        if len(data):
            data = pedal.patch_upload(int(options.upload), data)
        pedal.disconnect()

        exit(0)

    if options.getfile:
        pedal.getfile(options.getfile)

    if options.receive:
        pedal.file_check("FLST_SEQ.ZT2")
        data = pedal.file_download("FLST_SEQ.ZT2")
        logging.info("options.receive - getting FLST_SEQ.ZT2")
        pedal.file_close()

        # so now interpret the data to get the ZD2's.
        # and for each call getfile(name)
        # we also create a total pedal JSON
        # we need to create a "blank" entry for BYPASS
        total_pedal = [{
            "FX": {
                "name": "Bypass",
                "description": "No effect.",
                "version": "1.00",
                "fxid": 0,
                "gid": 0,
                "group": 0,
                "groupname": "BYPASS",
                "numParams": 0,
                "numSlots": 1,
                "filename": ""
            },
            "Parameters": []
            }
        ]

        fxLookup = {}
        fxLookup[0, 0] = 0
        j = 1
        config = ZT2.parse(data)
        for group in config[1]:
            logging.info("Group{}: {}".format( dict(group)["group"],  dict(group)["groupname"]))
    
            for effect in dict(group)["effects"]:
                myG = dict(effect)["id"]
                myGID = ((myG & gidMask) >> 16) >> 5
                myID = (myG & fxidMask)
                logging.info("myID is {} {}".format( myID, hex(myID)))
                logging.info("myGID is {} {}".format( int(myGID), hex(int(myGID))))
                logging.info("   {} (ver={}), group={}, id={}, fxid={}, gid={}, installed={}".format(dict(effect)["effect"], dict(effect)["version"], \
                    dict(effect)["group"], hex(dict(effect)["id"]), \
                    hex(myID), \
                    hex(int(myGID)), \
                    dict(effect)["installed"]))
                logging.info("Getting {}".format(dict(effect)["effect"]))
                currFX = pedal.getfile(dict(effect)["effect"])
                total_pedal.append(currFX)
                fxLookup[myID, myGID] = j 
                j = j + 1
        out_file = open("allfx.json", "w")
        json.dump(total_pedal, out_file, indent = 6)
        out_file.close()

        # now find list of Patches, pass in the fxLookup and total_pedal
        # we should use 6e 44 to determine how name patches.
        pedal.allpatches(total_pedal = total_pedal, fxLookup = fxLookup)
    else:
        # Read data from file
        infile = open(args[0], "rb")
        if not infile:
            sys.exit("Unable to open config FILE for reading")
        else:
            data = infile.read()
        infile.close()

    if options.add and options.ver and options.id:
        if options.id[:2] == "0x":
            data = pedal.add_effect(data, options.add, options.ver, int(options.id, 16))
        else:
            data = pedal.add_effect(data, options.add, options.ver, int(options.id))

    if options.delete:
        data = pedal.remove_effect(data, options.delete)
    
    if options.dump and data:
        logging.info("dump")
        config = ZT2.parse(data)
        logging.info(config)
    
    if options.toggle and data:
        logging.info("toggle")
        config = ZT2.parse(data)
        groupnum=0
    
        for group in config[1]:
            for effect in dict(group)["effects"]:
                if dict(effect)["effect"] == options.toggle:
                    if dict(effect)["installed"] == 1:
                        config[1][groupnum]["effects"][0]["installed"] = 0
                    else:
                        config[1][groupnum]["effects"][0]["installed"] = 1

            groupnum = groupnum + 1
        data = ZT2.build(config)
    
    if options.summary and data:
        logging.info("summary")
        config = ZT2.parse(data)
        for group in config[1]:
            logging.info("Group{}: {}".format( dict(group)["group"],  dict(group)["groupname"]))
    
            for effect in dict(group)["effects"]:
                myG = dict(effect)["id"]
                myGID = ((myG & gidMask) >> 16) >> 5
                myID = (myG & fxidMask)
                logging.info("myID is {} {}".format( myID, hex(myID)))
                logging.info("myGID is {} {}".format( int(myGID), hex(int(myGID))))
                logging.info("   {} (ver={}), group={}, id={}, fxid={}, gid={}, installed={}".format(dict(effect)["effect"], dict(effect)["version"], \
                    dict(effect)["group"], hex(dict(effect)["id"]), \
                    hex(myID), \
                    hex(int(myGID)), \
                    dict(effect)["installed"]))
                logging.info("Getting {}".format(dict(effect)["effect"]))
                currFX = pedal.getfile(dict(effect)["effect"])
                total_pedal.append(currFX)

    if options.build and data:
        logging.info("options.build")
        config = ZT2.parse(data)
        for group in config[1]:
            for effect in dict(group)["effects"]:
                print("python3 zoomzt2_shooking.py -i ", hex(dict(effect)["id"]), \
                    "-A", dict(effect)["effect"], "-v", dict(effect)["version"], \
                    "-w", options.build)

    if options.write and data:
       logging.info("options.write")
       outfile = open(args[0], "wb")
       if not outfile:
           sys.exit("Unable to open FILE for writing")
    
       outfile.write(data)
       outfile.close()

    binfile = None
    if options.install:
        # Read data from file
        binfile = open(options.install, "rb")
        if infile:
            binfile.close()

            pedal.file_check(options.install)
            pedal.file_upload(options.install)

    if options.uninstall:
        pedal.file_check(options.uninstall)
        pedal.file_delete(options.uninstall)

    if options.send:
        pedal.file_check("FLST_SEQ.ZT2")
        pedal.file_upload("FLST_SEQ.ZT2", data)
    
    if options.send or options.install or options.uninstall:
        pedal.file_close()
    
    if pedal.is_connected():
        pedal.disconnect()
    
if __name__ == "__main__":
    main()
