from anki.hooks import addHook
from aqt import mw
from aqt.utils import showInfo

models = ['japanese', 'rtk']
srcFields = ['Expression', 'Word']

# Execute method when leaving the field
def onFocusLost(flag, n, fidx):
    for m in models:
        if m not in n.model()['name'].lower():
            return flag
    src = None
    for c, name in enumerate(mw.col.models.fieldNames(n.model())):
        for f in srcFields:
            if name == f:
                src = f
                srcIdx = c
    if not src:
        return flag
    if fidx != srcIdx:
        return flag
    if n.dupeOrEmpty():
        return flag
    srcTxt = mw.col.media.strip(n[src])
    if not srcTxt:
        return flag
    showInfo("Length of '%s' is %i" % (src, len(srcTxt)))
    return True

addHook('editFocusLost', onFocusLost)
