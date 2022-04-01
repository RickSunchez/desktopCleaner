from nis import cat
import tkinter as tk
import tkinter.filedialog as fd

import os

from configparser import ConfigParser

CONFIG_FILE = "./config.cfg"
SEPARATOR = ";"
config = ConfigParser()

if not os.path.isfile(CONFIG_FILE):
    config["DEFAULT"] = {
        "DesktopFolder": "./test_desktop",
        "LockedFiles": ""
    }
    config["USER"] = {
        "DesktopFolder": "",
        "LockedFiles": ""
    }
    try:
        with open(CONFIG_FILE, "w") as f:
            config.write(f)
    except Exception:
        print(Exception)
else:
    config.read(CONFIG_FILE)

root = tk.Tk()

def getFolder():
    config.read(CONFIG_FILE)

    directory = fd.askdirectory(title="Открыть папку", initialdir="./")
    if directory:
        config["USER"]["DesktopFolder"] = directory
        re()

        try:
            with open(CONFIG_FILE, "w") as f:
                config.write(f)
        except Exception:
            print(Exception)

def onSelect(ev):
    elems = []
    for i in ev.widget.curselection():
        elems.append(ev.widget.get(i))

    locked = SEPARATOR.join(elems)
    config.read(CONFIG_FILE)
    config["USER"]["LockedFiles"] = locked

    try:
        with open(CONFIG_FILE, "w") as f:
            config.write(f)
    except Exception:
        print(Exception)

def exterminate():
    if config["USER"]["DesktopFolder"] == "": return False
    
    path = config["USER"]["DesktopFolder"]
    locked = config["USER"]["LockedFiles"].split(SEPARATOR)

    for f in os.listdir(path):
        if f in locked: continue
        fullpath = path + "/" + f

        if os.path.isdir(fullpath):
            os.rmdir(fullpath)
        else:
            os.remove(fullpath)

    re()

def re():
    listWidget.delete(0, tk.END)

    path = config["USER"]["DesktopFolder"] \
        if config["USER"]["DesktopFolder"] != "" \
        else config["DEFAULT"]["DesktopFolder"]

    locked = config["USER"]["LockedFiles"].split(SEPARATOR)

    for file in os.listdir(path):
        listWidget.insert(tk.END, file)

        if file in locked:
            listWidget.select_set(tk.END)

def generateBat():
    path = config["USER"]["DesktopFolder"] \
        if config["USER"]["DesktopFolder"] != "" \
        else config["DEFAULT"]["DesktopFolder"]

    locked = config["USER"]["LockedFiles"].split(SEPARATOR)

    cmd =  "echo @off\n"
    cmd += "cd \"%s\"\n" % path
    
    files = []
    dirs = []
    for l in locked:
        fullpath = path + "/" + l

        if os.path.isdir(fullpath):
            dirs.append(l)
        else:
            files.append(l)

    cmd += "rm -f !(%s)\n" % "|".join(files)
    cmd += "rd -f !(%s)" % "|".join(dirs)

    # rm -f !(file.txt|data.dat)
    try:
        with open("desktop_cleaner.bat", "w") as f:
            f.write(cmd)
    except Exception:
        print(Exception)

mainmenu = tk.Menu(root)
root.config(menu=mainmenu)

filemenu = tk.Menu(mainmenu, tearoff=0)
filemenu.add_command(label="Указать папку", command=getFolder)

mainmenu.add_cascade(label="Настройки", menu=filemenu)

listWidget = tk.Listbox(root, selectmode=tk.MULTIPLE)

re()

listWidget.bind('<<ListboxSelect>>', onSelect)
listWidget.pack()

btn = tk.Button(text="Exec", command=exterminate)
btn.pack()
btn = tk.Button(text="Gen", command=generateBat)
btn.pack()

root.mainloop()