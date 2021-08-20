#!/usr/bin/python
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

from PIL import Image, ImageTk
win = Tk()

win.geometry("1200x600")
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

fxOn = [False, False, False, False, False]
# we use this to keep tabs of the FX slot
# so slot 1 is midi val 0
# slot 2 can be midi val 1, but if double slot then 2
# let's put the default values in first
# modify it on FX load
fxSlotID = [0, 1, 2, 3, 4]

# returns data ready for display
def populatePatches():
    try:
        # need to see with BYPASS
        myPatches=[]
        logging.info("In populatePatches")
        for ri in range(0,len(rawPatches)):
            rp = rawPatches[ri]
            slots = ""
            for i in range(0, rp['numFX']): 
                slots=slots + str(rp['FX'][i]['numSlots'])
            currP = {
                'n': rp['patchname'],
                'd': rp['description'],
                's': slots
            }
            myPatches.append(currP)
        return tuple(myPatches)
    except:
        pass
        return


def populateFX():
    try:
        myFX=[]
        logging.info("In populatePatches")
        for ri in range(0, len(rawFX)):
            rp = rawFX[ri]['FX']
            """
            currP = {
                'name': rp['name'],
                'description': rp['description'],
                'version': rp['version'],
                'fxid': rp['fxid'],
                'gid': rp['gid'],
                'group': rp['group'],
                'groupname': rp['groupname'],
                'numParams': rp['numParams'],
                'numSlots': rp['numSlots'],
                'filename': rp['filename']
            }
            """
            currP = {
                'groupname': rp['groupname'],
                'name': rp['name'],
                'description': rp['description'],
                #'version': rp['version'],
                'fxid': rp['fxid'],
                'gid': rp['gid'],
                #'group': rp['group'],
                'numParams': rp['numParams'],
                'numSlots': rp['numSlots'],
                'filename': rp['filename']
            }
            myFX.append(currP)
        return tuple(myFX)
    except:
        pass
        return


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
    logging.info(i)
    fxOn[i] = not fxOn[i]
    if fxOn[i] == True:
        theFX['onoff'].config(text = "FX{} {}".format(i+1, "ON"))
        theFX['onoff'].config(bg = "green")
    else:
        theFX['onoff'].config(text = "FX{} {}".format(i+1, "OFF"))
        theFX['onoff'].config(bg = "red")
    runCommand('../../B1XFour/FXM_OnOff.sh {} {}'.format(theFX['slot'], 1  if fxOn[i] else 0))


# i is the FX permutation
# allFX means we have handle on all FX slots and states
def fx_id_clicked(i, allFX, avail_FX):
    logging.info(i)
    
    rawdata = avail_FX.get()
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
    for i in range(len(FX)):
        logging.info(i)
        FX[i]['slot'] = i + 1
        FX[i]['label'] = tk.Label(win)
        FX[i]['label'].place(x = wid * i, y = 000)
        FX[i]['onoff'] = tk.Button(win, text= "FX{} OnOff".format(i+1), 
            command = lambda  arg1 = i, arg2 = FX[i]: fx_clicked(arg1, arg2) )
        FX[i]['onoff'].place(x = wid * i, y = 200)
        # here we pass the whole FX cache because new slots need to be adjusted
        FX[i]['effect'] = tk.Button(win, text= "FX{} ID".format(i+1), 
            command = lambda  arg1 = i, arg2 = FX, arg3 = avail_FX:
                fx_id_clicked(arg1, arg2, arg3) )
        FX[i]['effect'].place(x = wid * i, y = 250)

def runCommand(cmd):
    print("STARTING INIT")
    p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)

    # run the command ... oh let the user know.
    out = p.stderr.read()
    # could put a message via stdout
    # to check it worked EXCEPT we check the files.
    #sys.stdout.write(str(out))
    sys.stdout.flush()
    print("FINISHED INIT")


# Tk's way is you _know_ what you bound this to.
def userSelectedPatch(event):
    theIndex = avail_Patches.current()
    theValue = avail_Patches.get()
    rp = rawPatches[theIndex]

    # we have index into the patch,
    # so walk the FX
    prevSlot=0
    for iFX in range(0, rp['numFX']):
        cfx = rp['FX'][iFX]
        img = getImage(cfx['filename'])
        theFX=currFX[iFX]
        if iFX == 0:
            theFX['slot'] = cfx['numSlots']
            prevSlot = theFX['slot']
        else:
            theFX['slot'] = cfx['numSlots'] + prevSlot

        theFX['label'].configure( image = img)
        theFX['label'].image = img
        if cfx['enabled'] == True:
            theFX['onoff'].config(text = "FX{} {}".format(iFX+1, "ON"))
            theFX['onoff'].config(bg = "green")
        else:
            theFX['onoff'].config(text = "FX{} {}".format(iFX+1, "OFF"))
            theFX['onoff'].config(bg = "red")
    # ok so how about we actually change the patch??
    runCommand('../../B1XFour/LoadPatch.sh {}'.format(theIndex + 10))


currFX = [{'onoff' : None, 'label': None, 'slot': x + 1, 'effect': None} for x in range(5)]

if __name__ == "__main__":
    
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
    # OK so now we should have allpatches.json and allfx.json
    if not(os.path.exists("allfx.json") and os.path.exists("allpatches.json")):
        print("Something wrong - expected to have created allfx.json and allpatches.json")
        print("Try replugging pedal into Pi. Ensure you only have one Zoom connected.")
        sys.exit(1)

    print("Loading FXs")
    with open('allfx.json', 'r') as fxFile:
        dataFX=fxFile.read()
    rawFX=json5.loads(dataFX)

    print("Loading Patches")
    with open('allpatches.json', 'r') as patchesFile:
        dataPatches=patchesFile.read()
    rawPatches=json5.loads(dataPatches)
    # add a dropdown with list of patches.
    patchesLabel = tk.Label(win, text="Patch")
    patchesLabel.place(x = 0, y = 500)
    selectedPatch = tk.StringVar()
    avail_Patches = ttk.Combobox(win, width="200", values=populatePatches(), textvariable=selectedPatch, state='readonly')
    avail_Patches.place(x=100, y = 500)

    # bind event to callback for avail_patches change
    avail_Patches.bind("<<ComboboxSelected>>", userSelectedPatch)   

    # add a dropdown with list of FXs.
    fxLabel = tk.Label(win, text="FX")
    fxLabel.place(x = 0, y = 550)
    selectedFX = tk.StringVar()
    avail_FX = ttk.Combobox(win, width="200", values=populateFX(), textvariable=selectedFX, state='readonly')
    avail_FX.place(x=100, y = 550)

    pedalFX = [{'groupname': None, 'Filename' : None, 'FXID': None, 'GID': None, 'version': None}]

    buildCurrFXGUI(win, avail_FX, currFX)
    # main()
    win.mainloop()

    # think of threading. Can we create/destroy a pedal? use that in threads?
