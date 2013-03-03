from anki.hooks import addHook
from anki.utils import ids2str, stripHTML
from aqt import mw

# List of (model, field)
targets = [('Japanese', 'Expression')]

def onSearch(cmds):
    cmds['len'] = findByExactLength
    cmds['max'] = findByMaxLength
    cmds['min'] = findByMinLength

def findByExactLength((val, args)):
    return findBy(lambda x, y: len(x) == int(y), val)

def findByMaxLength((val, args)):
    return findBy(lambda x, y: len(x) <= int(y), val)

def findByMinLength((val, args)):
    return findBy(lambda x, y: len(x) >= int(y), val)

def findBy(fn, val):
    mods = {}
    for m in mw.col.models.all():
        for f in m['flds']:
            if isTargetField((m, f)):
                mods[str(m['id'])] = f
    nids = []
    for mid in mods:
        for nid in mw.col.findNotes("mid:%s" % mid):
            note = mw.col.getNote(nid)
            text = stripHTML(note[mods[mid]['name']])
            if fn(text, val):
                nids.append(nid)
    return "n.id in %s" % ids2str(nids)

def isTargetField((model, field)):
    for (m, f) in targets:
        if m in model['name'] and f == field['name']:
            return True
    return False

addHook('search', onSearch)
