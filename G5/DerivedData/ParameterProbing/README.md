# Probing G5

So far I have not worked out how to insert new FX into a G5.
If you know how to please create a new issue and give some hints!

Anyhow, inside the firmware are the usual OnOff values.
I do not yet see equivalent of ZDL as per B1ON. Therefore I grab the OnOff directly and process these.
They seem 0x30 long and one can derive the FX name, max, default, whether it is a pedal parameter etc.

=> OUTPUT of FXName.json

Next I took the PDF and exported to text and manually created JSON to describe the parameters. Zoom's FX order is different
to the sysex - this I call z\id.

=> g5\_params.json

Finally, I cycled the FXIDs from 0 to N (sysex), wrote down which FX appears. This ID I call p\id for pedalID

JOIN together in python.

You can find the *merge* files.

NOTE: In addition to the 8 FX one can also have a Z Pedal FX.
At the moment I have not worked out how to incarnate them with SYSEX.
But I record them, along with derived midi max/default values for future processing.


IF you want to generate your own DAT files then grab the Zoom Firmware Updater feed it into checkme.py
