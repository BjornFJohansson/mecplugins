# -*- coding: utf-8 -*-
WIKIDPAD_PLUGIN = (("MenuFunctions",1),)
from pwiki.StringOps            import strftimeUB
def describeMenuItems(wiki):
    global nextNumber
    return ((rd, _(u"RELOAD"), _(u"RELOAD")),)

def rd(wiki, evt):
    wiki.reloadMenuPlugins()
    print "menu plugins reloaded " #+strftimeUB("%Y-%m-%d|%A %B %d|%H:%M:%S")
    print




