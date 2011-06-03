# -*- coding: utf-8 -*-
WIKIDPAD_PLUGIN = (("MenuFunctions",1), ("ToolbarFunctions",1))
#WIKIDPAD_PLUGIN = (("MenuFunctions",1),)

def describeMenuItems(wiki):
    return((close_open_tabs,_(u"MECplugins|close open tabs"), _(u"close open tabs")),
          )

def describeToolbarItems(wiki):
    return ((close_open_tabs, _(u"close open tabs"), _(u"close open tabs"), "cross"),)

def close_open_tabs(wiki,evt):
    here = wiki.getCurrentWikiWord()
    openpages =  wiki.getMainAreaPanel().getDocPagePresenters()    
    for page in openpages:
        if page.getWikiWord()!=here:
            wiki.getMainAreaPanel().closePresenterTab(page)
    return





















































def test3(wiki, evt):

    if wiki.getCurrentWikiWord() is None:
        return

    content = wiki.getActiveEditor().GetSelectedText().upper()

    if not content:

        cursorline = wiki.getActiveEditor().GetCurrentLine()
        textlines  = wiki.getActiveEditor().GetText().splitlines()

        line = cursorline
        foundstart = True

        while not (textlines[line].startswith("LOCUS") or textlines[line].startswith(">")):
            if line == 0:
                foundstart = False  
                break               
            line=line-1
       
        if foundstart: 
            content = "\n".join(textlines[line:])
            seq = parse_text_into_list_of_seqs(content)[0]      
            contentrecord = seq.record

    if not content:
        return

    checksum  = seguid(contentrecord.seq)
    timestamp = strftimeUB("%Y-%m-%d_%H:%M:%S")    
    stamp = string.Template("\nSEGUID:$checksum calculated $date. ").safe_substitute({'checksum':checksum, 'date': timestamp} )
    slask = wiki.stdDialog("text", "SEGUID checksum", checksum, checksum)

    if contentrecord.description.find(checksum) ==-1:
        contentrecord.description+=stamp
    
    result = contentrecord.format(seq.format)

    #wiki.SetSelectionByCharPos(start, end):

    #print result

'''

I need a way to know the position of the parsed sequence 
in the text so that I can set the selection.


'''

