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
# -f (--film) Sostituisce tutti i '.' & '_' con ' '
# -s (--subdir) aplica la rinomina anche alle sottocartelle
# -m (--mkdir) dopo rinomina crea cartella con nome del file e inserisce dentro il file
# -h (--help) stampa messaggio help

### DEFINIZIONE ARGOMENTI ###

film = 0 #-f --film
subdir = 0 #-s --subdir
mkdir = 0 #-m --mkdir

### CONSOLE COLORS ###

RESET = "\033[0m";                          # Text Reset

BLACK = "\033[0;30m";                       # BLACK
RED = "\033[0;31m";                         # RED
GREEN = "\033[0;32m";                       # GREEN
YELLOW = "\033[0;33m";                      # YELLOW
BLUE = "\033[0;34m";                        # BLUE
PURPLE = "\033[0;35m";                      # PURPLE
CYAN = "\033[0;36m";                        # CYAN
WHITE = "\033[0;37m";                       # WHITE
                                        #BOLD
BLACK_BOLD = "\033[1;30m";                  # BLACK 
RED_BOLD = "\033[1;31m";                    # RED
GREEN_BOLD = "\033[1;32m";                  # GREEN
YELLOW_BOLD = "\033[1;33m";                 # YELLOW
BLUE_BOLD = "\033[1;34m";                   # BLUE
PURPLE_BOLD = "\033[1;35m";                 # PURPLE
CYAN_BOLD = "\033[1;36m";                   # CYAN
WHITE_BOLD = "\033[1;37m";                  # WHITE
                                        #UNDERLINED
BLACK_UNDERLINED = "\033[4;30m";            # BLACK
RED_UNDERLINED = "\033[4;31m";              # RED
GREEN_UNDERLINED = "\033[4;32m";            # GREEN
YELLOW_UNDERLINED = "\033[4;33m";           # YELLOW
BLUE_UNDERLINED = "\033[4;34m";             # BLUE
PURPLE_UNDERLINED = "\033[4;35m";           # PURPLE
CYAN_UNDERLINED = "\033[4;36m";             # CYAN
WHITE_UNDERLINED = "\033[4;37m";            # WHITE
                                        #BACKGROUND
BLACK_BACKGROUND = "\033[40m";              # BLACK
RED_BACKGROUND = "\033[41m";                # RED
GREEN_BACKGROUND = "\033[42m";              # GREEN
YELLOW_BACKGROUND = "\033[43m";             # YELLOW
BLUE_BACKGROUND = "\033[44m";               # BLUE
PURPLE_BACKGROUND = "\033[45m";             # PURPLE
CYAN_BACKGROUND = "\033[46m";               # CYAN
WHITE_BACKGROUND = "\033[47m";              # WHITE
                                        #BRIGHT
BLACK_BRIGHT = "\033[0;90m";                # BLACK
RED_BRIGHT = "\033[0;91m";                  # RED
GREEN_BRIGHT = "\033[0;92m";                # GREEN
YELLOW_BRIGHT = "\033[0;93m";               # YELLOW
BLUE_BRIGHT = "\033[0;94m";                 # BLUE
PURPLE_BRIGHT = "\033[0;95m";               # PURPLE
CYAN_BRIGHT = "\033[0;96m";                 # CYAN
WHITE_BRIGHT = "\033[0;97m";                # WHITE
                                        #BOLD BRIGHT
BLACK_BOLD_BRIGHT = "\033[1;90m";           # BLACK
RED_BOLD_BRIGHT = "\033[1;91m";             # RED
GREEN_BOLD_BRIGHT = "\033[1;92m";           # GREEN
YELLOW_BOLD_BRIGHT = "\033[1;93m";          # YELLOW
BLUE_BOLD_BRIGHT = "\033[1;94m";            # BLUE
PURPLE_BOLD_BRIGHT = "\033[1;95m";          # PURPLE
CYAN_BOLD_BRIGHT = "\033[1;96m";            # CYAN
WHITE_BOLD_BRIGHT = "\033[1;97m";           # WHITE
                                        #BACKGROUND BRIGHT
BLACK_BACKGROUND_BRIGHT = "\033[0;100m";    # BLACK
RED_BACKGROUND_BRIGHT = "\033[0;101m";      # RED
GREEN_BACKGROUND_BRIGHT = "\033[0;102m";    # GREEN
YELLOW_BACKGROUND_BRIGHT = "\033[0;103m";   # YELLOW
BLUE_BACKGROUND_BRIGHT = "\033[0;104m";     # BLUE
PURPLE_BACKGROUND_BRIGHT = "\033[0;105m";   # PURPLE
CYAN_BACKGROUND_BRIGHT = "\033[0;106m";     # CYAN
WHITE_BACKGROUND_BRIGHT = "\033[0;107m";    # WHITE

def criticalError(err):
    print(WHITE_BOLD_BRIGHT + RED_BACKGROUND_BRIGHT + "[ CRITICAL ERROR ]" + RESET + " " + RED_UNDERLINED + err + RESET)

def error(err):
    print(RED_BOLD_BRIGHT + "[ ERROR ]" + RESET + " " + err)

def warning(wrn):
    print(YELLOW_BOLD_BRIGHT + "[ WARNING ]" + RESET + " " + wrn)

def ok(okk):
    print(GREEN_BOLD_BRIGHT + "[ OK ]" + RESET + " " + okk)

def help():
    print(
        "\n\nrename.py [path] [argv]\n\n" +
        "ARGOMENTI:\n" +
        "\t-f (--film)\t\tsostituisce tutti i caratteri PUNTO e UNDERSCORE con caratteri SPAZIO\n" +
        "\t-s (--subdir)\t\tapplica le modifiche di nome anche ai file DENTRO le sotto cartelle\n" +
        "\t-m (--mkdir)\t\tcrea cartella, con lo stesso nome del file, e ci sposta il file dentro\n" +
        "\t-h (--help)\t\tstampa dell'help (questo messaggio)\n"
        )

def mkdirMode(name, path):
    if int(mkdir) == 1:
        drs = os.path.join(path, name)
        print(drs)
        
        if not os.path.isdir(drs):
            os.mkdir(drs)
        else:
            os.rename(drs, drs)

    return name

def filmMode(name):
    if int(film) == 1: #se modalita' film attiva converte tutti i '.' & '_' in ' '
        name = name.replace(".", " ").replace('_', ' ')

    return name

def getFiles(path):
    return next(walk(path), (None, None, []))[2] #acquisizione dei file nella cartella

def rename(name, path):
    newName = os.path.splitext(name.title())[0] #acquisizione file senza estansione
    ext = os.path.splitext(name)[-1].lower() #acquisizione estensione

    if len(ext) == 0:
        return name

    newName = filmMode(newName)
    newName = mkdirMode(newName, path)
    
    i = 0
    while(int(i) != -1):
        try:
            os.rename(os.path.join(path, name), (path + '\\' + (newName + '\\' + newName if mkdir == 1 else newName) + (' (' + str(i) + ')' if i > 0 else '') + ext))
            i = -1
        except:
            i += 1

    print(
        "(OLD NAME)\n\t" +
        name + "\n" +
        "(NEW NAME)\n\t" +
        (str(newName) + '\\' if mkdir == 1 else '') + str(newName) + (' (' + str(i) + ')' if (i > 0) else '') + ext + '\n'
        )

### ACQUISIZIONE DEGLI ARGOMENTI ###

path = None

if len(sys.argv) <= 1:
    path = askdirectory(title='Select Folder') #Seleziona cartella e passa path
elif len(sys.argv) == 2:
    if str(sys.argv[1]) != "--help" and str(sys.argv[1]) != "-h":
        path = str(sys.argv[1]) #in caso di 1 argomento prende come path
    else:
        help()
else:
    print()
    path = str(sys.argv[1]) #prende primo argomento come path
    for i in range(2, len(sys.argv)): #controllo degi restanti argomenti
        match str(sys.argv[i]):
            case "-f" | "--film":
                film = 1
            case "-s" | "--subdir":
                subdir = 1
            case "-m" | "--mkdir":
                mkdir = 1
            case "-h" | "--help":
                help()
            case _: #argomento non trovato
                warning("argomento \'" + str(sys.argv[i]) + "\' non trovato")

print( #dichiarazione modalita' attive
    "Modalita':\n" +
    "\tfilm: " + ("ATTIVA" if film == 1 else "disattiva") + "\n" +
    "\tsub-directory: " + ("ATTIVA" if subdir == 1 else "disattiva") + "\n" +
    "\tcreazione cartelle: " + ("ATTIVA" if mkdir == 1 else "disattiva") + "\n"
    )

if path != None:
    print("Folder: " + path + "\n") #dichiarazione path di utilizzo

    filenames = getFiles(path)

    ### OPERAZIONE DI RINOMINA DEL FILE ###
    if os.path.isfile(path):
        ok("file singolo\n")
        print(os.path.basename(path), '\\'.join(path.split('\\')[0:-1]))
        rename(os.path.basename(path), '\\'.join(path.split('\\')[0:-1]))
    elif subdir == 1:
        ok("cartella e sotto cartelle")
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
        error("files or path not found")

    #print("cartelle")
    #subdirs = [x[0] for x in os.walk(path)]
    #print(subdirs)

#time.sleep(500)
