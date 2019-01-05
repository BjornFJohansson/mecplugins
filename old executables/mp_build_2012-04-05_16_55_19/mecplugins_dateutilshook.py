# -*- coding: utf-8 -*-
WIKIDPAD_PLUGIN = (("hooks", 1),)
def newWikiWord(docPagePresenter, wikiWord):
    import time
    from   pwiki.StringOps import strftimeUB
    try:
        timestamp = time.mktime(time.strptime(wikiWord, "%Y-%m-%d"))
    except ValueError:
        return
    docPagePresenter.getWikiDocument().createWikiPage(wikiWord, suggNewPageTitle=strftimeUB("%Y-%m-%d|%A %B %d|Week %W\n[alias: %d %B %Y]", timestamp))
    return


