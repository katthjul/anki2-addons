# -*- coding: UTF-8 -*-
# Author: Pauline Gomér <pauline.gomer@gmail.com>
# License: WTF Public License
#
# Bulk-add clozes that are sorted by frequency of use.
#

import os, re, itertools
from anki.hooks import addHook
from anki.utils import stripHTML
from aqt import mw
from aqt.qt import *
import codecs
from collections import defaultdict

# (model, source, destination)
targets = [
    (u'Cloze', u'Text', u'Extra'),
    (u'穴埋め', u'テキスト', u'追加'),
]
default_file = os.path.join(os.path.dirname(__file__), 
                            '.', 'frame-list.txt')
# Initialize our dictionaries
k2fdict = defaultdict(int)
f2kdict = defaultdict(str)

# Regex patterns
pCloze = re.compile("{{c(\d+)::(.+?)}}") # {{c<number>::<text>}}
pFrame = re.compile("\s*(\D)(\d+)") # <kanji><number>

def initAddon():
    for ln in codecs.open(default_file, 'r', 'utf-8'):
        a,b = ln.split()
        k2fdict[a] = b
        f2kdict[b] = a

def clozeFields(note):
    cloze = None
    extra = None
    for (m,c,e) in targets:
       if m in note.model()['name']:
           cloze = c
           extra = e
           break
    return (cloze,extra)

def extractFrameNumbers(text):
    matches = pFrame.findall(text)
    return dict([(c,int(f)) for (c,f) in matches])

def extractClozes(text):
    c2k = {}
    for (ci,ct) in pCloze.findall(text):
        kanji = ct.split("::")[0]
        # zero-based index
        c2k[int(ci)] = kanji
    return c2k

def formatFrameNumber(token):
    kanji = f2kdict[token]
    frame = k2fdict[token]
    if not kanji and not frame:
       return None
    if kanji:
        return kanji + token
    return token + frame

def bulkAddClozes(nids):
    mw.checkpoint("Bulk-add clozes")
    mw.progress.start()
    for nid in nids:
        note = mw.col.getNote(nid)
        (c,e) = clozeFields(note)
        # does it contain data?
        if not c or not e or not note[c] or not note[e]:
            continue
        _formatFrameNumbers(note, c, e)
        _createClozes(note, c, e)
        _repositionCards(note, c, e)
    mw.progress.finish()
    mw.reset()

def formatFrameNumbers(nids):
    mw.checkpoint("Format frame numbers")
    mw.progress.start()
    for nid in nids:
        note = mw.col.getNote(nid)
        (c,e) = clozeFields(note)
        # does it contain data?
        if not e or not note[e]:
           continue
        _formatFrameNumbers(note, c, e)
    mw.progress.finish()
    mw.reset()

def _formatFrameNumbers(note, clozeField, extraField):
    extraText = stripHTML(note[extraField])
    txt = []
    for token in extraText.split():
        frame = formatFrameNumber(token)
        # don't destroy data
        if not frame:
           txt.append(token)
           continue
        txt.append(frame)
    note[extraField] = u' '.join(txt)
    note.flush()

def createClozes(nids):
    mw.checkpoint("Create clozes")
    mw.progress.start()
    for nid in nids:
        note = mw.col.getNote(nid)
        (c,e) = clozeFields(note)
        # does it contain data?
        if not c or not e or not note[c] or not note[e]:
            continue
        _createClozes(note, c, e)
    mw.progress.finish()
    mw.reset()

def _createClozes(note, clozeField, extraField):
    c2k = extractClozes(note[clozeField])
    k2f = extractFrameNumbers(note[extraField])
    # cannot handle note with existing clozes
    if c2k:
        return
    text = []
    index = 1
    for c in note[clozeField]:
        if c in k2f:
            text.append("{{c%d::%s}}" % (index, c))
            index += 1
        else:
            text.append(c)
    note[clozeField] = ''.join(text)
    note.flush()

def repositionCards(nids):
    mw.checkpoint("Reposition cards")
    mw.progress.start()
    for nid in nids:
        note = mw.col.getNote(nid)
        (c,e) = clozeFields(note)
        # does it contain data?
        if not c or not e:
           continue
        _repositionCards(note, c, e)
    mw.progress.finish()
    mw.reset()

def _repositionCards(note, clozeField, extraField):
    clozeText = stripHTML(mw.col.media.strip(note[clozeField]))
    k2f = extractFrameNumbers(note[extraField])
    c2k = extractClozes(clozeText)
    for card in note.cards():
        # only modify new cards
        if card.type != 0:
            continue
        kanji = c2k[card.ord + 1]
        if kanji not in k2f:
            continue
        card.due = k2f[kanji]
        card.flush()

def regenerateFrameNumbers(nids):
    mw.checkpoint("Regenerate frame numbers")
    mw.progress.start()
    for nid in nids:
        note = mw.col.getNote(nid)
        (c,e) = clozeFields(note)
        # right note type?
        if not c:
           continue
        clozeText = stripHTML(mw.col.media.strip(note[c]))
        kanji = []
        for c in clozeText:
            if c in k2fdict and c not in kanji:
                kanji.append(c)
        note[e] = u' '.join([formatFrameNumber(c) for c in kanji])
        note.flush()
    mw.progress.finish()
    mw.reset()

def setupMenu(browser):
    menuCloze = QMenu(browser.form.menubar)
    menuCloze.setTitle("&Cloze")
    browser.form.menubar.insertMenu(
        browser.form.menu_Help.menuAction(), menuCloze)
    a = QAction("Bulk-add clozes", browser)
    browser.connect(a, SIGNAL("triggered()"), lambda e=browser: onBulkAdd(e))
    menuCloze.addAction(a)
    menuCloze.addSeparator()
    a = QAction("&Format frame numbers", browser)
    browser.connect(a, SIGNAL("triggered()"), lambda e=browser: onFormat(e))
    menuCloze.addAction(a)
    a = QAction("&Create clozes", browser)
    browser.connect(a, SIGNAL("triggered()"), lambda e=browser: onCreate(e))
    menuCloze.addAction(a)
    a = QAction("&Reposition cards", menuCloze)
    browser.connect(a, SIGNAL("triggered()"), lambda e=browser: onReposition(e))
    menuCloze.addAction(a)
    menuCloze.addSeparator()
    a = QAction("Re&generate frame numbers", browser)
    browser.connect(a, SIGNAL("triggered()"), lambda e=browser: onRegenerate(e))
    menuCloze.addAction(a)

def onBulkAdd(browser):
    bulkAddClozes(browser.selectedNotes())

def onFormat(browser):
    formatFrameNumbers(browser.selectedNotes())

def onCreate(browser):
    createClozes(browser.selectedNotes())

def onReposition(browser):
    repositionCards(browser.selectedNotes())

def onRegenerate(browser):
    regenerateFrameNumbers(browser.selectedNotes())

initAddon()
addHook("browser.setupMenus", setupMenu)
