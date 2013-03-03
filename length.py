from anki.hooks import addHook
from anki.utils import ids2str, stripHTML
from aqt import mw

# List of (model, field)
# OBS: If model is 'Japanese' it will match any model name with that word,
#      i.e. 'RTK Japanese', 'Japanese Core', etc..
targetFields = [('Japanese', 'Expression')]

def onSearch(cmds):
    cmds['max'] = findByMaxLength

def findByMaxLength((val, args)):
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
            if len(text) <= int(val):
                nids.append(nid)
    return "n.id in %s" % ids2str(nids)

def isTargetField((model, field)):
    for (m, f) in targetFields:
        if m.lower() in model['name'].lower() and f == field['name']:
            return True
    return False

addHook('search', onSearch)
