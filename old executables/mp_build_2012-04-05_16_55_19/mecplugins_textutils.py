# -*- coding: latin-1 -*-
###########################################
#  _______         _   _    _ _   _ _
# |__   __|       | | | |  | | | (_) |
#    | | _____  __| |_| |  | | |_ _| |___
#    | |/ _ \ \/ /| __| |  | | __| | / __|
#    | |  __/>  < | |_| |__| | |_| | \__ \
#    |_|\___/_/\_\ \__|\____/ \__|_|_|___/
###########################################
WIKIDPAD_PLUGIN = (("MenuFunctions",1),("ToolbarFunctions",1))
#WIKIDPAD_PLUGIN = (("MenuFunctions",1),)

import mecplugins_ini

import  codecs
import  string
import  time
import  os
import  sys
from    string import split,count
from    os import linesep

from    pwiki.StringOps            import mbcsEnc, strftimeUB
from    pwiki.WikiExceptions       import WikiFileNotFoundException
from    pwiki.PersonalWikiFrame    import PersonalWikiFrame

import  tempfile
import  sys
import  subprocess

def describeMenuItems(wiki):
    return (	(dewrap, 		_(u"mecplugins|Text utils|Dewrap selected text")	                , _(u"dewrap selection")),
                (expandtabs, 		_(u"mecplugins|Text utils|Expand tabs to spaces for selected text")     , _(u"expand tabs")),
                (togglecase, 	        _(u"mecplugins|Text utils|Toggle case\tCtrl-U")	                        , _(u"toggle case")),
                (wordcount, 	        _(u"mecplugins|Text utils|Count words in page")	                        , _(u"count words")),
                (rest_to_doc, 		_(u"mecplugins|Text utils|Open in word processor")	                , _(u"word processor")),
                )

def describeToolbarItems(wiki):
    return (    #(wordcount, 		_(u"Count words in page"), 	_(u"Count words in page"),	u"count"),
                #(togglecase, 		_(u"toggle case"), 		_(u"toggle case"), 		u"swap_case"),
		 (dewrap, 		_(u"dewrap"), 			_(u"dewrap"), 			u"dewrap"),
                #(rest_to_doc, 		_(u"word processor"),	        _(u"word processor"),           u"wordprocessor"),
                )

def rest_to_doc(wiki, evt):
    if wiki.getCurrentWikiWord() is None:
        return
    content = wiki.getActiveEditor().GetSelectedText()
    if not content:
        content = wiki.getActiveEditor().GetText()

    f = tempfile.NamedTemporaryFile(suffix=".rst",mode='w+t',delete=False)
    f.write(content)
    f.close()
    file=str(f.name)

    # get settings
    exec(wiki.getWikiDocument().getWikiPage("WikiSettings/mecplugins/word processor").getContent().encode())

    try:
        retcode=subprocess.check_call(command_line_for_rst2odt, shell=True)
        if retcode < 0:
            print >>sys.stderr, "Child was terminated by signal", -retcode
        else:
            print >>sys.stderr, "Child returned", retcode
    except OSError, e:
        print >>sys.stderr, "Execution failed:", e

    os.system(command_line_for_word_processor)

def expandtabs(wiki, evt):
    if wiki.getCurrentWikiWord() is None:
        return
    content = wiki.getActiveEditor().GetSelectedText()
    if not content:
        content = wiki.getActiveEditor().GetText()
    defaulttabsize=4
    tabsize=int(wiki.stdDialog("text", "Expand tabs", "use tab size:", additional=str(defaulttabsize)))
    #print tabsize
    expanded_content=content.expandtabs(tabsize)
    wiki.getActiveEditor().ReplaceSelection(expanded_content)

def dewrap(wiki, evt):
    start, end = wiki.getActiveEditor().GetSelection()
    if wiki.getCurrentWikiWord() is None:
        return
    content = wiki.getActiveEditor().GetSelectedText()
    if not content:
        content = wiki.getActiveEditor().GetText()
    if content.lstrip().rstrip().find(" ")!=-1:
        dewrapped_content = content.replace("\n"," ")
    else:
        dewrapped_content = content.replace("\n","")
    dewrapped_content = " ".join(dewrapped_content.split())
    wiki.getActiveEditor().ReplaceSelection(dewrapped_content)
    wiki.getActiveEditor().GotoPos(start)
    return

def togglecase(wiki, evt):
    start, end = wiki.getActiveEditor().GetSelection()
    if wiki.getCurrentWikiWord() is None:
        return
    content = wiki.getActiveEditor().GetSelectedText()
    if not content:
        content = wiki.getActiveEditor().GetText()

    if content.isupper():
        content=content.title()

    elif content.istitle():
        content=content.lower()

    elif content.islower():
        content=content.upper()

    else:
        content=content.lower()
    wiki.getActiveEditor().ReplaceSelection(content)
    wiki.getActiveEditor().SetSelection(start, end)
    return

def getCount(data):
    """
    Counts lines, words, chars in data
    """
    # count some stuff
    lines = len(data.split("\n"))
    words = len(data.split())
    chars = len(data)-lines+1
    blanks = data.count(" ")

    return lines, words, chars, blanks

def wordcount(wiki, evt):
    if wiki.getCurrentWikiWord() is None:
        return

    content = wiki.getActiveEditor().GetSelectedText()

    if not content:
        content = wiki.getActiveEditor().GetText()

    lines, words, chars, blanks = getCount(content)

    wiki.displayMessage("Wordcount",
                        "Lines\t\t\t\t: %s\n"
                        "Words\t\t\t\t: %s\n"
                        "Chars inc blanks\t\t: %s\n"
                        "Chars w/o blanks\t\t: %s\n" % (lines, words, chars, chars-blanks))
