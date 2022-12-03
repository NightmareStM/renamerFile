from asyncio.windows_events import NULL
from ctypes import cdll
from distutils.extension import Extension
from pathlib import Path
from tkinter import Tk
from tkinter.filedialog import askdirectory
from os import mkdir, walk
import time
import os
import sys
import array

def getFiles(path):
    return next(walk(path), (None, None, []))[2]

path = askdirectory(title='Select Folder')

filenames = getFiles(path)

cds = NULL
drs = NULL

for name in filenames:
    cod = os.path.splitext(name)[0].split('_')[0].title()
    alb = os.path.splitext(name)[0].split('[')[0][8:-1].replace("_", " ").title()
    trc = os.path.splitext(name)[0].split('[')[1].replace("]", "").replace("_", " ").title()
    ext = os.path.splitext(name)[-1].lower()

    print(
        "Nome: \"" + str(name) + "\"\n" +
        "Codice: \"" + str(cod) + "\"\n" +
        "Album: \"" + str(alb) + "\"\n" +
        "Traccia: \"" + str(trc) + "\"\n" +
        "Estensione: \"" + str(ext) + "\"\n" +
        "\n"
        )

    if cod != cds:
        cds = cod
        drs = os.path.join(path, alb)
        if not os.path.exists(drs):
            os.mkdir(drs)

    i = 0
    while(int(i) != -1):
        try:
            os.rename(os.path.join(path, name), os.path.join(drs, str(trc + (" (" + str(i) + ")" if i > 0 else "") + ext)))
            i = -1
        except:
            i += 1