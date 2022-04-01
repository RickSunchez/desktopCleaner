import sys
import os
import argparse
import random

FOLDER = "./test_desktop"
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
TYPES = [".txt", ".json", ".cfg", ".ini", ".jpg", ".xml", ".doc"]

def randName():
    length = random.randint(3, 10)
    out = ""

    for i in range(length):
        out += random.choice(ALPHABET)

    return out

parser = argparse.ArgumentParser()
parser.add_argument("--count", "-c", default="5", type=int)

args = parser.parse_args(sys.argv[1:])

if not os.path.isdir(FOLDER):
    os.mkdir(FOLDER)

if len(os.listdir(FOLDER)) >= args.count:
    print("Done")
    exit()

i = 0
while i < args.count:
    path = FOLDER + "/" + randName()
    if random.random() < 0.5:
        path += random.choice(TYPES)
        if os.path.isfile(path): continue

        with open(path, "w") as f: f.write("")
    else:
        if os.path.isdir(path): continue
        os.mkdir(path)

    i += 1
