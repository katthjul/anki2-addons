# -*- coding: UTF-8 -*-
from anki.hooks import addHook
from aqt import mw
from aqt.qt import *
from collections import defaultdict
import os

default_file = os.path.join(os.path.dirname(__file__), 
                            'cloze_creator', 'frame-list.txt')
# Initialize our dictionaries
k2fdict = defaultdict(int)
f2kdict = defaultdict(str)

def initAddon():
    for ln in open(default_file):
        a,b = ln.split()
        k2fdict[a] = b
        f2kdict[b] = a

def regenerateFrameNumbers(nids):
    print "Hello"

def setupMenu(browser):
    menuFormat = QMenu(browser.form.menubar)
    menuFormat.setTitle("&Cloze")
    browser.form.menubar.addAction(menuFormat.menuAction())
    #menuFormat.setTitle("Format")
    #menuFormat.setObjectName("Format")
    #menuFormat.addAction(a)
    #browser.form.menubar.addAction(menuFormat.menuAction())
    a = QAction("Bulk-add Frame Numbers", browser)
    browser.connect(a, SIGNAL("triggered()"), lambda e=browser: onRegenerate(e))
    browser.form.menuEdit.addAction(a)

def onRegenerate(browser):
    regenerateFrameNumbers(browser.selectedNotes())

initAddon()
addHook("browser.setupMenus", setupMenu)
