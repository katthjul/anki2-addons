# -*- coding: UTF-8 -*-
from anki.hooks import addHook
from aqt import mw
from aqt.qt import *
import codecs
from collections import defaultdict
import os

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

def formatFrameNumbers(nids):
    mw.checkpoint("Format frame numbers")
    mw.progress.start()
    for nid in nids:
        note = mw.col.getNote(nid)
        model = None
        cloze = None
        extra = None
        for (m,c,e) in targets:
           if m in note.model()['name'] and note[c] and note[e]:
               model = m
               cloze = c
               extra = e
               break
        # found model? does it contain data?
        if not model or not note[extra]:
           continue
        extraText = mw.col.media.strip(note[extra])
        txt = []
        for frame in extraText.split():
            kanji = f2kdict[frame]
            if not kanji:
               # don't destroy data
               txt.append(frame)
               continue
            txt.append(kanji + frame)
        note[extra] = u' '.join(txt)
        note.flush()
    mw.progress.finish()
    mw.reset()

def setupMenu(browser):
    menuCloze = QMenu(browser.form.menubar)
    menuCloze.setTitle("&Cloze")
    browser.form.menubar.insertMenu(
        browser.form.menu_Help.menuAction(), menuCloze)
    a = QAction("Format frame numbers", browser)
    browser.connect(a, SIGNAL("triggered()"), lambda e=browser: onFormat(e))
    menuCloze.addAction(a)

def onFormat(browser):
    formatFrameNumbers(browser.selectedNotes())

initAddon()
addHook("browser.setupMenus", setupMenu)
