from asyncio.windows_events import NULL
from distutils.extension import Extension
from pathlib import Path
from tkinter import Tk
from tkinter.filedialog import askdirectory
from os import walk
import time
import os
import sys
import mimetypes

# DESCRIZIONE COMANDO
# rename.py [path] [argv]
# -film Sostituisce tutti i '.' con ' '
# -subdir aplica la rinomina anche alle sottocartelle

### DEFINIZIONE ARGOMENTI ###

film = 0 #-film
subdir = 0 #-subdir

def help():
    print(
        "\n\nrename.py [path] [argv]\n\n" +
        "ARGOMENTI:\n" +
        "\t-film\t\tsostituisce tutti i caratteri PUNTO con caratteri SPAZIO\n" +
        "\t-subdir\t\tapplica le modifiche di nome anche ai file DENTRO le sotto cartelle" +
        "\n"
        )

def filmMode(name, path):
    if int(film) == 1: #se modalita' film attiva converte tutti i '.' & '_' in ' '
        name = name.replace(".", " ").replace('_', ' ')
        drs = os.path.join(path, name)
        print(drs)
        
        if not os.path.isdir(drs):
            os.mkdir(drs)
        else:
            os.rename(drs, drs)

    return name

def getFiles(path):
    return next(walk(path), (None, None, []))[2] #acquisizione dei file nella cartella

def rename(name, path):
    newName = os.path.splitext(name.title())[0] #acquisizione file senza estansione
    ext = os.path.splitext(name)[-1].lower() #acquisizione estensione

    if len(ext) == 0:
        return name

    newName = filmMode(newName, path)
    
    i = 0
    while(int(i) != -1):
        try:
            os.rename(os.path.join(path, name), (path + '\\' + (newName + '\\' + newName if film == 1 else newName) + (' (' + str(i) + ')' if i > 0 else '') + ext))
            i = -1
        except:
            i += 1

    print(
        "(OLD NAME)\n\t" +
        name + "\n" +
        "(NEW NAME)\n\t" +
        (str(newName) + '\\' if film == 1 else '') + str(newName) + (' (' + str(i) + ')' if (i > 0) else '') + ext + '\n'
        )

### ACQUISIZIONE DEGLI ARGOMENTI ###

path = NULL

if len(sys.argv) <= 1:
    path = askdirectory(title='Select Folder') #Seleziona cartella e passa path
elif len(sys.argv) == 1:
    if str(sys.argv)[1] != "-help":
        path = str(sys.argv[1]) #in caso di 1 argomento prende come path
    else:
        help()
else:
    path = str(sys.argv[1]) #prende primo argomento come path
    for i in range(len(sys.argv)): #controllo degi restanti argomenti
        match str(sys.argv[i]):
            case "-film": #riconoscimento argomento -film
                film = 1
            case "-subdir":
                subdir = 1
            case "-help":
                help()
            case _: #argomento non trovato
                print("argomento \'" + str(sys.argv[i]) + "\' non trovato")

print( #dichiarazione modalita' attive
    "Modalita':\n" +
    "\tfilm: " + ("ATTIVA" if film == 1 else "disattiva") + "\n" +
    "\tsub-directory: " + ("ATTIVA" if subdir == 1 else "disattiva") + "\n"
    )
print("Folder: " + path + "\n") #dichiarazione path di utilizzo

filenames = getFiles(path)

### OPERAZIONE DI RINOMINA DEL FILE ###
if os.path.isfile(path):
    print("file singolo\n")
    print(os.path.basename(path), '\\'.join(path.split('\\')[0:-1]))
    rename(os.path.basename(path), '\\'.join(path.split('\\')[0:-1]))
elif subdir == 1:
    print("cartella e sotto cartelle")
    for path in [x[0] for x in os.walk(path)]:
        print(path)
        filenames = getFiles(path)
        for name in filenames:
            rename(name, path)
elif len(filenames) > 0: #controllo esistenza file
    print("cartella con file\n")
    for name in filenames: #passaggio dei file
        rename(name, path)
else: #se non e' stato trovato alcun file
    print("Files or path not found")

#print("cartelle")
#subdirs = [x[0] for x in os.walk(path)]
#print(subdirs)

#time.sleep(500)