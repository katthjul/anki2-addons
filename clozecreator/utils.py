# -*- coding: UTF-8 -*-
# Author: Pauline Gomér <pauline.gomer@gmail.com>
# License: WTF Public License

import codecs, os, re
from collections import defaultdict

########################################
# Definitions

# Regex patterns
pCloze = re.compile("{{c(\d+)::(.+?)}}") # {{c<number>::<text>[::<hint>]}}
pFrame = re.compile("\s*(\D)(\d+)") # <kanji><number>

# Initialize our dictionaries
k2fdict = defaultdict(int)
f2kdict = defaultdict(str)

default_file = os.path.join(os.path.dirname(__file__), 
                            '.', 'frame-list.txt')

for ln in codecs.open(default_file, 'r', 'utf-8'):
    a,b = ln.split()
    k2fdict[a] = b
    f2kdict[b] = a

########################################
# Utility functions

def extractClozes(text):
    c2k = {}
    for (ci,ct) in pCloze.findall(text):
        #kanji = ct.split("::")[0]
        # zero-based index
        c2k[int(ci)] = ct.split("::")
    return c2k

def extractFrames(text):
    matches = pFrame.findall(text)
    return dict([(c,int(f)) for (c,f) in matches])

def extractKanji(text):
    kanji = []
    for c in text:
        if c in k2fdict and c not in kanji:
            kanji.append(c)
    return kanji

def formatCloze(index, cs):
    return "{{c%d::%s}}" % (index, '::'.join(c))

def formatFrame(token):
    kanji = f2kdict[token]
    frame = k2fdict[token]
    if not kanji and not frame:
       return None
    if kanji:
        return kanji + token
    return token + frame

def formatFrames(tokens):
    frames = []
    for token in tokens:
        frame = formatFrame(token)
        # don't destroy data
        if frame:
           frames.append(frame)
    return frames
