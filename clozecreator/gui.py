# -*- coding: UTF-8 -*-
# Author: Pauline Gomér <pauline.gomer@gmail.com>
# License: WTF Public License
#
# Bulk-add clozes that are sorted by frequency of use.
#

from anki.hooks import addHook
from anki.utils import stripHTML
from aqt import mw
from aqt.qt import *
from clozecreator.utils import *

# (model, source, destination)
clozeModel = [
    (u'Cloze', u'Text', u'Extra'),
    (u'穴埋め', u'テキスト', u'追加'),
]

def clozeFields(note):
    cloze = None
    extra = None
    for (m,c,e) in clozeModel:
       if m in note.model()['name']:
           cloze = c
           extra = e
           break
    return (cloze,extra)

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
    note[extraField] = u' '.join(formatFrames(extraText.split()))
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
    k2f = extractFrames(note[extraField])
    # cannot handle note with existing clozes
    if c2k:
        return
    text = []
    index = 1
    for c in note[clozeField]:
        # 0: kanji, 1: hint
        if c[0] in k2f:
            text.append(formatCloze(index, c))
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
    k2f = extractFrames(note[extraField])
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
        note[e] = u' '.join([formatFrame(c) for c in extractKanji(clozeText)])
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

addHook("browser.setupMenus", setupMenu)
