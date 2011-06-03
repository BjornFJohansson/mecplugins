# -*- coding: utf-8 -*-
WIKIDPAD_PLUGIN = (("hooks", 1),)
def newWikiWord(docPagePresenter, wikiWord):
    import time
    import datetime
    from   pwiki.StringOps import strftimeUB  #, formatWxDate
    try:
        pagedate = datetime.date(*time.strptime(wikiWord, "%Y-%m-%d")[0:3])
    except ValueError:
        return
    docPagePresenter.getWikiDocument().createWikiPage(wikiWord,
                                                      suggNewPageTitle=wikiWord+"|"+ strftimeUB("%A %B %d|Week %W", 
                                                      time.mktime( time.strptime(wikiWord, "%Y-%m-%d")))+"\n\n++---\n")
    return
