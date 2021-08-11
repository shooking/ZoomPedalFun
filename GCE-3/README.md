I will put GCE-3 data in here

CAUTION - You do everything at your own risk!

I bricked my GCE-3 temporarily.
I am ok with losing £60 to experiment. Your mileage may vary.

HOW DID I UNBRICK?

1. Uninstall the Guitar Lab
2. Reinstall the Zoom PC drivers (get from Zoom's site)
3. Reboot PC
4. Reinstall 1.20 Firmware -- this took a long time. Seemed to get stuck on step 6. Patience.
5. End of install asked you to unpower the GCE-3. Pulled USB C out... plugged back in. Light went green
6. Restart Guitar Lab.
7. Grab a coffee - it seems to take an age to discover your GCE-3. I think it goes of to the internet to find stuff?

First useful info:

When you emulate a pedal on your GCE-3 then majority of its functionality works.
Looper and rhythm does not always work but the patches and FX are stored on the pedal.

This means you can, with midi command, change patch.
And for the "4" models (B1XFour etc) it is possible to edit FX's, parameter values in real time.

AVAILABLE ZOOM Emulations

hex id     | model     | version
---------- | ----------| -------
0x6E001400 | unselected| na
0x6E000000 | G5n       | 3.00
0x6E000200 | G3n       | 2.20
0x6E000300 | G3Xn      | 2.20
0x6E000400 | B3n       | 2.20
0x6E000C00 | G1 FOUR   | 2.00
0x6E000D00 | G1X FOUR  | 2.00
0x6E000E00 | B1 FOUR   | 2.00
0x6E000F00 | B1X FOUR  | 2.00
0x6E001000 | ??        | 1.20
0x6E001100 | A1 FOUR   | 1.01
0x6E001200 | A1X FOUR  | 1.01
0x6E001300 | ?         | 1.50
0x6E001700 | ?         | 1.30
0x6E001900 | ?         | 1.30

So put pedal in EditorOn mode.
Then ask "what mode are you in please?"

pi@raspberrypi:~/Software/ZoomPedal $ amidi -p ${MIDI_DEV} -S "f0 52 00 6E 58 02 F7" -r temp.bin -t 1 ; hexdump -C temp.bin

11 bytes read
00000000  f0 52 00 6e 58 01 6e 00  12 00 f7                 |.R.nX.n....|
0000000b

Notice 6e 00 12 00 => A1X Four.

And indeed that is what mode the stored state of my GCE-3 currently is.
So can we change it?




