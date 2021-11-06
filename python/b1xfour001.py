#!/usr/bin/python
#
# added TkInter and other functions.
# Stephen Hookings, May 2021
# Assumption is you run this from ZoomPedalFun/python directory
#
# https://stackoverflow.com/questions/68394825/ttk-combobox-triggers-listboxselect-event-in-different-tk-listbox
# mido examples
# https://github.com/snhirsch/katana-midi-bridge/blob/master/katana.py
import logging
import subprocess
logging.basicConfig(filename='midi.log', level=logging.DEBUG)
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter as tk
from tkinter import font
from io import BytesIO
from collections import Counter
from PIL import Image, ImageTk
win = Tk()

win.geometry("1800x900")
bigfont = font.Font(family="LucidaConsole", size = 20)
win.option_add("*Font", bigfont)
    
from construct import *
import re
# I think we need json5
import json5
import json
import os
import shutil
import sys
import mido
import binascii
from time import sleep

fxOn = [False, False, False, False, False, False, False, False, False]
# we use this to keep tabs of the FX slot
# so slot 1 is midi val 0
# slot 2 can be midi val 1, but if double slot then 2
# let's put the default values in first
# modify it on FX load
fxSlotID = [0, 1, 2, 3, 4, 5, 6, 7, 8]
# the FX's slot
activeFX = None

def FXM_ID(ioport, slot, fxid, gid):
    sysex = mido.Message('sysex')
    sendString = [0x52, 0x00, 0x6e, 0x64, 0x03, 0x00, slot - 1, 1, fxid & 0x7f, (fxid>>7) & 0x7f, 0, gid & 0x7f, (gid >> 7) & 0x7f]
    sysex.data = sendString
    ioport.send(sysex)


def FXM_PN(ioport, slot, pn, v):
    sysex = mido.Message('sysex')
    sendString = [0x52, 0x00, 0x6e, 0x64, 0x03, 0x00, slot - 1, pn + 1, v & 0x7f, (v>>7) & 0x7f, 0, 0, 0]
    sysex.data = sendString
    ioport.send(sysex)


def FXM_OnOff(ioport, slot, OnOff):
    sysex = mido.Message('sysex')
    sendString = [0x52, 0x00, 0x6e, 0x64, 0x03, 0x00, slot - 1, 0x00, OnOff, 0x00, 0x00, 0x00, 0x00]
    sysex.data = sendString
    ioport.send(sysex)


def LoadPatch(ioport, theIndex, bankSize):

    cc = mido.Message('control_change')
    cc.channel = 0
    cc.control = 0
    cc.value = 0
    ioport.send( cc )

    cc.control = 0x20
    cc.value = int(theIndex / bankSize)
    ioport.send( cc )

    pc = mido.Message('program_change')
    pc.channel = 0
    pc.program = theIndex % bankSize
    ioport.send( pc )



# returns data ready for display
def populatePatches():
    try:
        myPatches=[]
        logging.info("In populatePatches")
        for ri in range(0,len(rawPatches)):
            rp = rawPatches[ri]
            """
            # might need this later to determine placement
            slots = ""
            endLoop = rp['numFX']
            i = 0
            j = 0

            while i < endLoop:
                currSlot=rp['FX'][j]['numSlots']
                slots=slots + str(currSlot)
                j = j + 1
                i = i + currSlot
            """
            myPatches.append("[{}] {}".format(ri, rp['patchname']))
        return tuple(myPatches)
    except:
        pass
        return


def populateFX():
    try:
        myFX=[]
        myFXG=[]
        myFXNameIndex={}
        logging.info("In populateFX")
        for ri in range(0, len(rawFX)):
            if ri % 10 == 0:
                print("Loaded FX {}".format(ri))
            rfx = rawFX[ri]['FX']
            currFX = {
                'groupname': rfx['groupname'],
                'name': rfx['name'],
                'description': rfx['description'],
                #'version': rfx['version'],
                'fxid': rfx['fxid'],
                'gid': rfx['gid'],
                #'group': rfx['group'],
                'numParams': rfx['numParams'],
                'numSlots': rfx['numSlots'],
                'filename': rfx['filename']
            }
            myFX.append(currFX)
            myFXG.append(rfx['groupname'])
            myFXNameIndex[rfx['name']] = ri
        cnt = Counter(myFXG)
        x=[elem for elem in cnt] 
        return tuple(myFX), myFXNameIndex, x
    except:
        pass
        return None, None, None


def getImage(name):
    # check for BYPASS
    if name == '':
        return None
    image = Image.open(name)
    zoomFactor=4

    new_image = image.resize((image.size[0]*zoomFactor, image.size[1]*zoomFactor))
    python_image = ImageTk.PhotoImage(new_image)
    return python_image


def fx_clicked(i, theFX):
    global fxOn
    global activeFX
    logging.info(i)
    # set global current FX
    activeFX = theFX
    print("Active FX = {}".format(activeFX))
    fxOn[i] = not fxOn[i]
    if fxOn[i] == True:
        theFX['onoff'].config(text = "FX{} {}".format(i+1, "ON"))
        theFX['onoff'].config(bg = "green", relief = SUNKEN, borderwidth=4)
        theFX['label'].configure( bg="white", borderwidth=1)
        FXM_OnOff(ioport, activeFX['slot'], 1)
    else:
        theFX['onoff'].config(text = "FX{} {}".format(i+1, "OFF"))
        theFX['onoff'].config(bg = "red", relief = RAISED, borderwidth=1)
        theFX['label'].configure( bg="red", borderwidth=10)
        FXM_OnOff(ioport, activeFX['slot'], 0)


def fx_selected(FX):
    global activeFX
    activeFX = FX
    theGlobalIndex = fxNameIndex[activeFX['name']]
    print("Setting activeFX {} {}".format(activeFX, theGlobalIndex))
    rawdata = rawFX[theGlobalIndex]
    # need to look this up in a list and then find right data.
    if rawdata is not None and len(rawdata) != 0:
        # zero out the params
        for i in range(len(params)):
            params[i][0].grid_forget()
        logging.info(len(rawdata))
        data = rawdata['FX']
        pdata = rawdata['Parameters']
        numParams = data['numParams']
        for i in range(numParams):
            # move current slots's FX values into the Parameter frame.
            paramVal[i].set(activeFX['params'][i])
            print(pdata[i]['name'])
            print(pdata[i]['mmax'])
            (params[i][1]).configure(text = pdata[i]['name'])
            (params[i][2]).configure(to = pdata[i]['mmax'])
            (params[i][3]).config(text = paramVal[i].get())
            params[i][0].grid(row = int( i / 3), column = i % 3, sticky="w")


def param_slider_changed(val, i, ioport):
    logging.info(i)
    if activeFX is not None:
        newval = int(float(val))
        # move current slots's FX values into the Parameter frame.
        (params[i][3]).config(text = paramVal[i].get())
        # make FX param storage reflect changed value
        activeFX['params'][i] = newval
        print("activeFX, i, val is {} {} {}".format(activeFX, i, newval))
        # check i v i + 1
        FXM_PN(ioport, activeFX['slot'], i + 1, newval)

# i is the FX permutation
# allFX means we have handle on all FX slots and states
def fx_id_clicked(i, allFX, avail_FX):
    logging.info(i)

    # OK so I was using avail_FX to grab the current selected FX
    # then derive data ... but now I want to have a shorter list
    # and I need to then find the index from full list.
    theIndex = avail_FX.curselection()
    theValue = avail_FX.get(theIndex)
    theGlobalIndex = fxNameIndex[theValue]
    activeFX = allFX[i]
    print("Setting activeFX {}".format(activeFX))
    print("Selected {} {} {}".format(theIndex, theGlobalIndex, theValue))
    rawdata = rawFX[theGlobalIndex]
    # need to look this up in a list and then find right data.
    if rawdata is not None and len(rawdata) != 0:
        logging.info(len(rawdata))
        # convert text string into Dict - it should be
        data = rawdata['FX']
        logging.info(data)
        groupName   = data['groupname']
        fileName    = data['filename']
        fxid        = data['fxid']
        gid         = data['gid']
        #version     = data['version']
        # how to work out slot size??
        allFX[i]['effect'].config(text = "{}:{}".format(fxid, gid))

        # transfer FX param data to our memory BUT
        # because this comes from an FX we can only know about "mdefault"
        for q in range(len(rawdata['Parameters'])):
            baseParam = rawdata['Parameters'][q]
            # a raw FX doesnt have a param1, param2 but instead mdefault
            allFX[i]['params'][q] = baseParam['mdefault']
            # move current slots's FX values into the Parameter frame.
            paramVal[q].set(allFX[i]['params'][q])
            print(baseParam['name'])
            print(baseParam['mmax'])
            (params[q][1]).configure(text = baseParam['name'])
            (params[q][2]).configure(to = baseParam['mmax'])
            (params[q][3]).config(text = paramVal[q].get())
            (params[q][0]).grid(row = int( q / 3), column = q % 3, sticky="w")

        if fileName is None:
            allFX[i]['label'].configure( image = None)
            allFX[i]['label'].image = None
            return
        img = getImage(fileName)
        if img is not None:
            allFX[i]['label'].configure( image = img)
            allFX[i]['label'].image = img
            # i + 1 isnt right. I need to work out state of the patch, account for slots.
            # both missing and multi width.
            #runCommand('../../B1XFour/FXM_ID.sh {} {} {}'.format(allFX[i]['slot'], fxid, gid))
            FXM_ID(ioport, allFX[i]['slot'], fxid, gid)
    # should I also update the JSON for this patch?

def buildCurrFXGUI(win, avail_FX, FX):
    # create a label frame and put the widgets in there
    wid = 200
    baseHeight = 50
    currFXLabelFrame = LabelFrame(win, text="Current FX", height=350, width = wid * len(FX))
    currFXLabelFrame.pack(fill="both", expand="yes")
    for i in range(len(FX)):
        logging.info(i)
        FX[i]['slot'] = i + 1
        FX[i]['label'] = tk.Button(currFXLabelFrame, image = None,
            command = lambda  arg1 = FX[i]: fx_selected(arg1) )
        FX[i]['label'].place(x = wid * i, y = baseHeight)
        FX[i]['onoff'] = tk.Button(currFXLabelFrame, text= "FX{} OnOff".format(i+1), 
            command = lambda  arg1 = i, arg2 = FX[i]: fx_clicked(arg1, arg2) )
        FX[i]['onoff'].place(x = wid * i, y = 200 + baseHeight)
        # here we pass the whole FX cache because new slots need to be adjusted
        FX[i]['effect'] = tk.Button(currFXLabelFrame, text= "FX{} ID".format(i+1), 
            command = lambda  arg1 = i, arg2 = FX, arg3 = avail_FX:
                fx_id_clicked(arg1, arg2, arg3) )
        FX[i]['effect'].place(x = wid * i, y = 250 + baseHeight)

def runCommand(cmd):
    print("STARTING INIT")
    p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)

    # run the command ... oh let the user know.
    out = p.stderr.read()
    # could put a message via stdout
    # to check it worked EXCEPT we check the files.
    sys.stdout.write(str(out))
    sys.stdout.flush()
    print("FINISHED INIT")


# Tk's way is you _know_ what you bound this to.
def userSelectedPatch(event):
    print("In USERSELECTEDPATCH")
    selection = event.widget.curselection()
    if selection:
        theIndex = selection[0]
        theValue = event.widget.get(theIndex)
    else:
        theIndex=0
        theValue=0

    rp = rawPatches[theIndex]

    patchLabel.config(text = "Patch: {}\nDescription: {}".format(rp['patchname'], rp['description']))
    patchLabel.pack(side=TOP, anchor="w")
    # Zero out existing GUI first
    for i in range(0, len(currFX)):
        print("zeroing out gui {}".format(i))
        currFX[i]['onoff'].config(text = "FX{} {}".format(i+1, "OFF"))
        currFX[i]['onoff'].config(bg = "red", relief = RAISED, borderwidth=1)
        currFX[i]['label'].image = None
        currFX[i]['label'].configure( image = None )
        currFX[i]['slot'] = i + 1
        currFX[i]['effect'].config(text = "FX{} ID".format(i+1))
        currFX[i]['name'] = "Bypass" 
            
    # we have index into the patch,
    # so walk the FX
    endLoop = rp['numFX']
    i = 0 # actual slot
    j = 0 # logical slot
    # walk the logical slots (j), but set FX value in actual slot (i).
    while j < endLoop:
        cfx = rp['FX'][j]
        img = getImage(cfx['filename'])
        theFX=currFX[i]
        theFX['name'] = cfx['name']
        theFX['slot'] = i + 1
        theFX['label'].configure( image = img)
        theFX['label'].image = img
        if cfx['enabled'] == True:
            theFX['onoff'].config(text = "FX{} {}".format(i+1, "ON"))
            theFX['onoff'].config(bg = "green", relief = SUNKEN, borderwidth=4)
            if img:
                theFX['label'].configure( bg="white", borderwidth=1)
        else:
            theFX['onoff'].config(text = "FX{} {}".format(i+1, "OFF"))
            theFX['onoff'].config(bg = "red", relief = RAISED, borderwidth=1)
            if img:
                theFX['label'].configure( bg="red", borderwidth=10)
        i = i + cfx['numSlots']
        for q in range(len(cfx['Parameters'])):
            baseParam = cfx['Parameters'][q]
            theFX['params'][q] = baseParam["param{}".format(q+1)]
            # move current slots's FX values into the Parameter frame.
            paramVal[q].set(theFX['params'][q])
            print(baseParam['name'])
            print(baseParam['mmax'])
            (params[q][1]).configure(text = baseParam['name'])
            (params[q][2]).configure(to = baseParam['mmax'])
            (params[q][3]).config(text = paramVal[q].get())
            (params[q][0]).grid(row = int( q / 3), column = q % 3, sticky="w")
        j = j + 1


    # ok so how about we actually change the patch??
    bankSize = int(model['bankSize'])
    LoadPatch(ioport, theIndex, bankSize)


def userSelectedFX(event):
    # so here we got an event from Avail_FX group subset.
    # Now we need to expand this selection into global array
    # and call the fx clicked,
    print("\t\tUSERSELECTEDFX")
    selection = event.widget.curselection()
    if selection:
        theIndex = selection[0]
        theValue = event.widget.get(theIndex)
        print("Selected {} {}".format(theIndex, theValue))
        # Now I need to lookup theValue in global array
        theGlobalIndex = fxNameIndex[theValue]
        print("Selected {} {} {}".format(theIndex, theGlobalIndex, theValue))


def avail_FXGrp_clicked(event):
    print("\tAVAIL_FXGRP")
    selection = event.widget.get()
    FXListBox.delete(0, 'end')
    for item in fxPop:
        if item['groupname'].lower() == (selection).lower():
            FXListBox.insert('end', item['name'])

    FXListBox.config(yscrollcommand = scrollbarFXFrame.set)
    scrollbarFXFrame.config(command = FXListBox.yview)


def GenFX(lim):
    return [{'onoff' : None, 'label': None, 'slot': x + 1, 'effect': None, 'name': None, 'params': [ 0 for y in range(9)]} for x in range(lim)]

def InitializeFXState(currFX):
    x = 0
    for fx in currFX:
        fx = {'onoff' : None, 'label': None, 'slot': x + 1, 'effect': None, 'name' : None}
        x = x + 1

currFX = GenFX(9)
if __name__ == "__main__":
    
    # change to it
    """
    os.chdir("mypedal")
    """
    # remote directory mypedal
    if os.path.exists("mypedal"):
        shutil.rmtree("mypedal")
    # create it, it will be 755
    os.mkdir("mypedal")
    # change to it
    os.chdir("mypedal")
    # populate the directory. Assumption is you run this from
    # ZoomPedalFun/python directory
    # we then create and move to subdirectory mypedal
    # so the script is up one directory level
    cmd = 'python3 ../zoomzt2_shooking.py -R -w my_pedal.zt2'
    runCommand(cmd)
    #"""
    # OK so now we should have allpatches.json and allfx.json
    if not(os.path.exists("allfx.json") and os.path.exists("allpatches.json")):
        print("Something wrong - expected to have created allfx.json and allpatches.json")
        print("Try replugging pedal into Pi. Ensure you only have one Zoom connected.")
        sys.exit(1)

    midiname = "ZOOM G"
    for port in mido.get_input_names():
        logging.info("{}, {}".format(port, midiname))
        if port[:len(midiname)]==midiname:
            ioport = mido.open_ioport(port)
            print("Using Input:", port)
            break
    print("ioport {}".format(ioport))
    
    print("Loading Pedal")
    with open('model.dat', 'r') as fxFile:
        model=fxFile.read()
    #model=json5.loads(model)
    model=json.loads(model)
    print(model)
    print("Loading FXs")
    with open('allfx.json', 'r') as fxFile:
        dataFX=fxFile.read()
    #rawFX=json5.loads(dataFX)
    rawFX=json.loads(dataFX)

    print("Loading Patches")
    with open('allpatches.json', 'r') as patchesFile:
        dataPatches=patchesFile.read()
    #rawPatches=json5.loads(dataPatches)
    rawPatches=json.loads(dataPatches)
        # add device label at top of the screen

    # render the model etc
    # {'model': 'G5n', 'numPatches': 200, 'bankSize': 4, 'ptcSize': 760, 'version': '3.00', 'gce3version': '1.20'}
    modelLabel = tk.Label(win, text="{} ver {} GCE Model {} ver. {} patches, {} per bank"
            .format(model['model'], model['version'], model['gce3version'], model['numPatches'], model['bankSize']))

    modelLabel.pack(side=TOP)

    patchLabel = tk.Label(win, text="Patch: {}\nDescription: {}".format("UNSET", ""))
    patchLabel.pack(side=TOP, anchor="w")


    patchAndFX = tk.Frame(win, height = 450, width = 1800)
    patchAndFX.pack(side=BOTTOM, fill=BOTH)

    # create frame with scrollbar for patches
    textPatchLabelFrame = tk.LabelFrame(patchAndFX, text = "Patches", bg="red", height = 400, width=350, highlightcolor="blue")


    lbSelPatch = tk.StringVar()
    patchListBox = tk.Listbox(textPatchLabelFrame, listvariable=lbSelPatch)
    for item in populatePatches():
        patchListBox.insert('end', item)
    patchListBox.pack(side = RIGHT, fill=BOTH)
    scrollbarPatchFrame = tk.Scrollbar(textPatchLabelFrame, orient="vertical")
    scrollbarPatchFrame.pack(side = RIGHT, fill=BOTH)

    patchListBox.config(yscrollcommand = scrollbarPatchFrame.set)
    scrollbarPatchFrame.config(command = patchListBox.yview)
    patchListBox.bind("<<ListboxSelect>>", userSelectedPatch)

    textPatchLabelFrame.pack(side=LEFT, fill=BOTH)

    mainParamLabelFrame = tk.LabelFrame(patchAndFX, text="Parameters", bg="green", height=400, width=900)
    mainParamLabelFrame.pack(side=LEFT, fill=BOTH)

    # add a dropdown with list of FXs.
    fxLabelFrame = tk.LabelFrame(patchAndFX, text = "FX Group", height=400, width=350, highlightcolor="blue", bg="yellow")
    fxLabelFrame.pack(side=LEFT, fill=BOTH)

    fxPop, fxNameIndex, fxGrp = populateFX()

    selectedFXGrp = tk.StringVar()
    avail_FXGrp = ttk.Combobox(fxLabelFrame, width="20", values=fxGrp,
            textvariable=selectedFXGrp, state='readonly', exportselection=False)
    avail_FXGrp.pack(side = TOP, fill=BOTH)
    avail_FXGrp.bind("<<ComboboxSelected>>", avail_FXGrp_clicked)

    selectedFX = tk.StringVar()
    fxLBFrame=tk.Frame(fxLabelFrame, height=350, width=350, highlightcolor="blue", bg="blue")
    fxLBFrame.pack(side=RIGHT, fill = BOTH)
    FXListBox = tk.Listbox(fxLBFrame, listvariable=selectedFX, exportselection=False)
    for item in fxPop:
        if item['groupname'].lower() == (fxGrp[1]).lower():
            FXListBox.insert('end', item['name'])
    FXListBox.pack(side = RIGHT, fill = BOTH)
    scrollbarFXFrame = tk.Scrollbar(fxLBFrame, orient="vertical")
    scrollbarFXFrame.pack(side = RIGHT, fill = BOTH)

    FXListBox.config(yscrollcommand = scrollbarFXFrame.set)
    scrollbarFXFrame.config(command = FXListBox.yview)
    # add in command to take name and find fx values
    FXListBox.bind("<<ListboxSelect>>", userSelectedFX)

    avail_FX = FXListBox

    #pedalFX = [{'groupname': None, 'Filename' : None, 'FXID': None, 'GID': None, 'version': None}]

    buildCurrFXGUI(win, avail_FX, currFX)

    # add in 9 Parameters for the N FX.
    paramVal = [tk.IntVar() for x in range(9)]
    params = []
    for i in range(9):
        # dont forget to bias the parameter by 1
        pLF = tk.LabelFrame(mainParamLabelFrame, text="P{}".format(i+1), bg="green")
        pLF.grid(row = int( i / 3), column = i % 3, sticky="w")
        sl = ttk.Label(pLF, text="Param{}".format(i))
        sl.grid(column= 0, row=0, sticky="w")
        s = ttk.Scale(pLF, from_ = 0, to = 100, orient='horizontal',
            variable=paramVal[i], 
            command=lambda  arg1 = paramVal[i], arg2=i, arg3=ioport: param_slider_changed(arg1, arg2, arg3))
        s.grid(row=0, column=1, sticky = "w")
        scvl = ttk.Label(pLF, text="Value: ")
        scvl.grid(row=1, column=0, sticky = "w")
        scvlv = ttk.Label(pLF, text="10")
        scvlv.grid(row=1, column=1, sticky="w")
        params.append( [pLF, sl, s, scvlv] )
    # main()
    win.mainloop()
