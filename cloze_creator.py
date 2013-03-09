# -*- coding: UTF-8 -*-
import os, re
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
                            'cloze_creator', 'frame-list.txt')
# Initialize our dictionaries
k2fdict = defaultdict(int)
f2kdict = defaultdict(str)

def initAddon():
    for ln in codecs.open(default_file, 'r', 'utf-8'):
        a,b = ln.split()
        k2fdict[a] = b
        f2kdict[b] = a

def targetFields(note):
    cloze = None
    extra = None
    for (m,c,e) in targets:
       if m in note.model()['name']:
           cloze = c
           extra = e
           break
    return (cloze,extra)

def extractFrameNumbers(text):
    matches = re.findall("\s*(\D)(\d+)", text)
    return dict([(c,int(f)) for (c,f) in matches])

def extractClozes(text):
    c2k = {}
    for (ci,ct) in re.findall("{{c(\d+)::(.+?)}}", text):
        kanji = ct.split("::")[0]
        # zero-based index
        c2k[int(ci)-1] = kanji
    return c2k

def formatFrameNumber(token):
    kanji = f2kdict[token]
    frame = k2fdict[token]
    if not kanji and not frame:
       return None
    if kanji:
        return kanji + token
    return token + frame

def formatFrameNumbers(nids):
    mw.checkpoint("Format frame numbers")
    mw.progress.start()
    for nid in nids:
        note = mw.col.getNote(nid)
        (c,e) = targetFields(note)
        # does it contain data?
        if not e and not note[e]:
           continue
        extraText = mw.col.media.strip(note[e])
        txt = []
        for token in extraText.split():
            frame = formatFrameNumber(token)
            # don't destroy data
            if not frame:
               txt.append(token)
               continue
            txt.append(frame)
        note[e] = u' '.join(txt)
        note.flush()
    mw.progress.finish()
    mw.reset()

def repositionCards(cids):
    mw.checkpoint("Reposition cards")
    mw.progress.start()
    for cid in cids:
        card = mw.col.getCard(cid)
        note = card.note()
        (c,e) = targetFields(note)
        # does it contain data?
        if not c or not e:
           continue
        clozeText = stripHTML(mw.col.media.strip(note[c]))
        k2f = extractFrameNumbers(note[e])
        c2k = extractClozes(clozeText)
        # only modify new cards
        if card.type != 0:
            continue
        kanji = c2k[card.ord]
        if kanji not in k2f:
            continue
        card.due = k2f[kanji]
        card.flush()
    mw.progress.finish()
    mw.reset()

def regenerateFrameNumbers(nids):
    mw.checkpoint("Regenerate frame numbers")
    mw.progress.start()
    for nid in nids:
        note = mw.col.getNote(nid)
        (c,e) = targetFields(note)
        # right note type?
        if not c:
           continue
        clozeText = stripHTML(mw.col.media.strip(note[c]))
        frames = []
        for c in clozeText:
            if c in k2fdict:
                frames.append(formatFrameNumber(c))
        note[e] = u' '.join(set(frames))
        note.flush()
    mw.progress.finish()
    mw.reset()

def setupMenu(browser):
    menuCloze = QMenu(browser.form.menubar)
    menuCloze.setTitle("&Cloze")
    browser.form.menubar.insertMenu(
        browser.form.menu_Help.menuAction(), menuCloze)
    a = QAction("&Format frame numbers", browser)
    browser.connect(a, SIGNAL("triggered()"), lambda e=browser: onFormat(e))
    menuCloze.addAction(a)
    a = QAction("Re&position cards", menuCloze)
    browser.connect(a, SIGNAL("triggered()"), lambda e=browser: onReposition(e))
    menuCloze.addAction(a)
    menuCloze.addSeparator()
    a = QAction("Re&generate frame numbers", browser)
    browser.connect(a, SIGNAL("triggered()"), lambda e=browser: onRegenerate(e))
    menuCloze.addAction(a)

def onFormat(browser):
    formatFrameNumbers(browser.selectedNotes())

def onReposition(browser):
    repositionCards(browser.selectedCards())

def onRegenerate(browser):
    regenerateFrameNumbers(browser.selectedNotes())

initAddon()
addHook("browser.setupMenus", setupMenu)
