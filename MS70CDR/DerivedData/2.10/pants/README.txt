Make sure to have install all necessary python libs
Nowadays this means using a venv
pip install Pillow
pip install numpy
pip install filebytes

ProcessFirmware1.py MS70.exe

DoElf.sh



extract the ASM from the ELF (elf is 0x4c into my traditional ZDL cut point).

We are interested in

picEffectType_Cave:

so in general picEffectType_<<something to do with pedal model>>

We are also interested in floating point numbers

>>> import struct
>>> struct.unpack('!f', bytes.fromhex('41973333'))[0]
18.899999618530273
>>> struct.unpack('!f', bytes.fromhex('41995C29'))[0]
19.170000076293945
>>> struct.unpack('!f', bytes.fromhex('470FC614'))[0]
36806.078125

>>> struct.unpack('!f', bytes.fromhex('3f800000'))[0]
1.0
