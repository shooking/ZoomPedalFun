80#!/usr/bin/python
#
# added TkInter and other functions.
# Stephen Hookings, May 2021
# Assumption is you run this from ZoomPedalFun/python directory
#

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

win.geometry("1800x800")
bigfont = font.Font(family="LucidaConsole", size = 20)
win.option_add("*Font", bigfont)
    
from construct import *
import re
# I think we need json5
import json5

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

# returns data ready for display
def populatePatches():
    try:
        myPatches=[]
        logging.info("In populatePatches")
        for ri in range(0,len(rawPatches)):
            rp = rawPatches[ri]
            # might need this later to determine placement
            slots = ""
            endLoop = rp['numFX']
            i = 0
            j = 0
            # if we do not have any "2" effects the limit is endLoop
            # but for a 2 effect we need to got to endLoop + 1.
            # check how to do this better.
            print(endLoop)
            while j < endLoop:
                print(i, j)
                currSlot=rp['FX'][j]['numSlots']
                slots=slots + str(currSlot)
                j = j + 1
                i = i + currSlot
            """
            currP = {
                'n': rp['patchname'],
                'd': rp['description'],
                's': slots
            }
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
    print(image.mode)
    new_image = image.resize((image.size[0]*zoomFactor, image.size[1]*zoomFactor))
    python_image = ImageTk.PhotoImage(new_image)
    return python_image


def fx_clicked(i, theFX):
    global fxOn
    logging.info(i)
    fxOn[i] = not fxOn[i]
    if fxOn[i] == True:
        theFX['onoff'].config(text = "FX{} {}".format(i+1, "ON"))
        theFX['onoff'].config(bg = "green", relief = SUNKEN, borderwidth=4)
    else:
        theFX['onoff'].config(text = "FX{} {}".format(i+1, "OFF"))
        theFX['onoff'].config(bg = "red", relief = RAISED, borderwidth=1)
    runCommand('../../B1XFour/FXM_OnOff.sh {} {}'.format(theFX['slot'], 1  if fxOn[i] else 0))


# i is the FX permutation
# allFX means we have handle on all FX slots and states
def fx_id_clicked(i, allFX, avail_FX):
    logging.info(i)

    # OK so I was using avail_FX to grab the current selected FX
    # then derive data ... but now I want to have a shorter list
    # and I need to then find the index from full list.
    rawdata = avail_FX.get()
    print(rawdata)
    # need to look this up in a list and then find right data.
    if rawdata is not None and len(rawdata) != 0:
        logging.info(len(rawdata))
        # convert text string into Dict - it should be
        data = eval(rawdata)
        logging.info(data)
        groupName   = data['groupname']
        fileName    = data['filename']
        fxid        = data['fxid']
        gid         = data['gid']
        #version     = data['version']
        # how to work out slot size??
        allFX[i]['effect'].config(text = "{}:{}".format(fxid, gid))
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
            runCommand('../../B1XFour/FXM_ID.sh {} {} {}'.format(allFX[i]['slot'], fxid, gid))


def buildCurrFXGUI(win, avail_FX, FX):
    wid = 200
    baseHeight = 50
    for i in range(len(FX)):
        logging.info(i)
        FX[i]['slot'] = i + 1
        FX[i]['label'] = tk.Label(win)
        FX[i]['label'].place(x = wid * i, y = baseHeight)
        FX[i]['onoff'] = tk.Button(win, text= "FX{} OnOff".format(i+1), 
            command = lambda  arg1 = i, arg2 = FX[i]: fx_clicked(arg1, arg2) )
        FX[i]['onoff'].place(x = wid * i, y = 200 + baseHeight)
        # here we pass the whole FX cache because new slots need to be adjusted
        FX[i]['effect'] = tk.Button(win, text= "FX{} ID".format(i+1), 
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
    selection = event.widget.curselection()
    if selection:
        theIndex = selection[0]
        theValue = event.widget.get(theIndex)
    else:
        theIndex=0
        theValue=0

    rp = rawPatches[theIndex]

    # Zero out existing GUI first
    for i in range(0, len(currFX)):
        print("zeroing out gui {}".format(i))
        currFX[i]['onoff'].config(text = "FX{} {}".format(i+1, "OFF"))
        currFX[i]['onoff'].config(bg = "red", relief = RAISED, borderwidth=1)
        currFX[i]['label'].configure( image = None )
        currFX[i]['label'].image = None
        currFX[i]['slot'] = i + 1
        currFX[i]['effect'].config(text = "FX{} ID".format(i+1))
            
    # we have index into the patch,
    # so walk the FX
    endLoop = rp['numFX']
    i = 0 # actual slot
    j = 0 # logical slot
    print(endLoop)
    while j < endLoop:
        print(i, j)
        cfx = rp['FX'][j]
        img = getImage(cfx['filename'])
        theFX=currFX[i]
        theFX['slot'] = i + 1
        theFX['label'].configure( image = img)
        theFX['label'].image = img
        if cfx['enabled'] == True:
            theFX['onoff'].config(text = "FX{} {}".format(i+1, "ON"))
            theFX['onoff'].config(bg = "green", relief = SUNKEN, borderwidth=4)
        else:
            theFX['onoff'].config(text = "FX{} {}".format(i+1, "OFF"))
            theFX['onoff'].config(bg = "red", relief = RAISED, borderwidth=1)
        i = i + rp['FX'][j]['numSlots']
        j = j + 1

    # ok so how about we actually change the patch??
    bankSize = model['bankSize']
    runCommand('../../B1XFour/LoadPatch.sh {} {}'.format( int(theIndex / bankSize), theIndex % bankSize) )

def userSelectedFX(event):
    # so here we got an event from Avail_FX group subset.
    # Now we need to expand this selection into global array
    # and call the fx clicked,
    selection = event.widget.curselection()
    if selection:
        theIndex = selection[0]
        theValue = event.widget.get(theIndex)
    else:
        theIndex=0
        theValue=0

    print("Selected {} {}".format(theIndex, theValue))
    # Now I need to lookup theValue in global array
    theGlobalIndex = fxNameIndex[theValue]
    print("Selected {} {} {}".format(theIndex, theGlobalIndex, theValue))


    """
    rp = rawPatches[theIndex]

    # Zero out existing GUI first
    for i in range(0, len(currFX)):
        print("zeroing out gui {}".format(i))
        currFX[i]['onoff'].config(text = "FX{} {}".format(i+1, "OFF"))
        currFX[i]['onoff'].config(bg = "red", relief = RAISED, borderwidth=1)
        currFX[i]['label'].configure( image = None )
        currFX[i]['label'].image = None
        currFX[i]['slot'] = i + 1
        currFX[i]['effect'].config(text = "FX{} ID".format(i+1))
            
    # we have index into the patch,
    # so walk the FX
    endLoop = rp['numFX']
    i = 0 # actual slot
    j = 0 # logical slot
    print(endLoop)
    while j < endLoop:
        print(i, j)
        cfx = rp['FX'][j]
        img = getImage(cfx['filename'])
        theFX=currFX[i]
        theFX['slot'] = i + 1
        theFX['label'].configure( image = img)
        theFX['label'].image = img
        if cfx['enabled'] == True:
            theFX['onoff'].config(text = "FX{} {}".format(i+1, "ON"))
            theFX['onoff'].config(bg = "green", relief = SUNKEN, borderwidth=4)
        else:
            theFX['onoff'].config(text = "FX{} {}".format(i+1, "OFF"))
            theFX['onoff'].config(bg = "red", relief = RAISED, borderwidth=1)
        i = i + rp['FX'][j]['numSlots']
        j = j + 1

    # ok so how about we actually change the patch??
    bankSize = model['bankSize']
    runCommand('../../B1XFour/LoadPatch.sh {} {}'.format( int(theIndex / bankSize), theIndex % bankSize) )

    """

def avail_FXGrp_clicked(event):
    selection = event.widget.get()
    FXListBox.delete(0, 'end')
    for item in fxPop:
        if item['groupname'].lower() == (selection).lower():
            print("MATCHED!!{}".format(item['name']))
            FXListBox.insert('end', item['name'])

    FXListBox.config(yscrollcommand = scrollbarFXFrame.set)
    scrollbarFXFrame.config(command = FXListBox.yview)


def GenFX():
    return [{'onoff' : None, 'label': None, 'slot': x + 1, 'effect': None} for x in range(9)]

def InitializeFXState(currFX):
    for fx in currFX:
        fx = {'onoff' : None, 'label': None, 'slot': x + 1, 'effect': None}

currFX = GenFX()

if __name__ == "__main__":
    
    # change to it
    #"""
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
    """
    # OK so now we should have allpatches.json and allfx.json
    if not(os.path.exists("allfx.json") and os.path.exists("allpatches.json")):
        print("Something wrong - expected to have created allfx.json and allpatches.json")
        print("Try replugging pedal into Pi. Ensure you only have one Zoom connected.")
        sys.exit(1)

    print("Loading Pedal")
    with open('model.dat', 'r') as fxFile:
        model=fxFile.read()
    model=json5.loads(model)
    print(model)
    print("Loading FXs")
    with open('allfx.json', 'r') as fxFile:
        dataFX=fxFile.read()
    rawFX=json5.loads(dataFX)

    print("Loading Patches")
    with open('allpatches.json', 'r') as patchesFile:
        dataPatches=patchesFile.read()
    rawPatches=json5.loads(dataPatches)
        # add device label at top of the screen

    # render the model etc
    # {'model': 'G5n', 'numPatches': 200, 'bankSize': 4, 'ptcSize': 760, 'version': '3.00', 'gce3version': '1.20'}
    modelLabel = tk.Label(win, text="{} ver {} GCE Model {} ver. {} patches, {} per bank"
            .format(model['model'], model['version'], model['gce3version'], model['numPatches'], model['bankSize']))

    modelLabel.place(x = 100, y = 0)

    patchAndFX = tk.Frame(win, height = 450, width = 1800)
    patchAndFX.pack(side=BOTTOM, fill=BOTH)

    # create frame with scrollbar for patches
    patchFrame = tk.Frame(patchAndFX, height = 400, width=350, highlightcolor="blue", bg="red")
    patchFrame.pack(side=LEFT, fill=BOTH)
    textPatchFrame = Label(patchFrame, text = "Patches", bg="red")
    textPatchFrame.pack(side=TOP)

    lbSelPatch = tk.StringVar()
    patchListBox = tk.Listbox(patchFrame, listvariable=lbSelPatch)
    for item in populatePatches():
        patchListBox.insert('end', item)
    patchListBox.pack(side = LEFT, fill = BOTH)
    scrollbarPatchFrame = tk.Scrollbar(patchFrame, orient="vertical")
    scrollbarPatchFrame.pack(side = RIGHT, fill = BOTH)

    patchListBox.config(yscrollcommand = scrollbarPatchFrame.set)
    scrollbarPatchFrame.config(command = patchListBox.yview)
    patchListBox.bind("<<ListboxSelect>>", userSelectedPatch)

    # add a dropdown with list of FXs.
    fxFrame = tk.Frame(patchAndFX, height=400, width=350, highlightcolor="blue", bg="yellow")
    fxFrame.pack(side=RIGHT, fill = BOTH)
    fxLabel = tk.Label(fxFrame, text="FX Group", bg="yellow")
    fxLabel.pack(side=TOP)

    fxPop, fxNameIndex, fxGrp = populateFX()

    selectedFXGrp = tk.StringVar()
    avail_FXGrp = ttk.Combobox(fxFrame, width="20", values=fxGrp, textvariable=selectedFXGrp, state='readonly')
    avail_FXGrp.pack(side = TOP)
    avail_FXGrp.bind("<<ComboboxSelected>>", avail_FXGrp_clicked)

    selectedFX = tk.StringVar()
    fxLBFrame=tk.Frame(fxFrame, height=350, width=350, highlightcolor="blue", bg="blue")
    fxLBFrame.pack(side=RIGHT, fill = BOTH)
    FXListBox = tk.Listbox(fxLBFrame, listvariable=selectedFX)
    for item in fxPop:
        print("checking {}".format(item))
        if item['groupname'].lower() == (fxGrp[1]).lower():
            print("MATCHED!! {}".format(item['name']))
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

    # main()
    win.mainloop()
