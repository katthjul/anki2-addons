# -*- coding: UTF-8 -*-
from collections import defaultdict

k2fdict = defaultdict(int)
f2kdict = defaultdict(str)

for ln in open("frame-list.txt"):
  a,b = ln.split()
  k2fdict[a] = b
  f2kdict[b] = a

print k2fdict['一'], f2kdict['1']
