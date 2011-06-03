########################################
#  _      _     _   _    _ _   _ _
# | |    (_)   | | | |  | | | (_) |
# | |     _ ___| |_| |  | | |_ _| |___
# | |    | / __| __| |  | | __| | / __|
# | |____| \__ \ |_| |__| | |_| | \__ \
# |______|_|___/\__|\____/ \__|_|_|___/
########################################
# -*- coding: latin-1 -*-
WIKIDPAD_PLUGIN = (("MenuFunctions",1),)

import string
import itertools
from os import linesep

def describeMenuItems(wiki):
    return (	(sortSelection,		    _(u"MECplugins|List utils|Sort selected lines")	                   , _(u"sort selection")),
		        (invertSelection,	    _(u"MECplugins|List utils|Invert selected lines")	                   , _(u"invert selection")),
                (remove_duplicates,     _(u"MECplugins|List utils|Remove duplicate lines")	           , _(u"remove_duplicates")),
                (ziplists,	            _(u"MECplugins|List utils|Zip lists")	                           , _(u"ziplists")),
                (unziplists,	        _(u"MECplugins|List utils|Unzip lists")	                           , _(u"unziplists")),
                (table,	                _(u"MECplugins|List utils|ReST simple table from lists")	           , _(u"table")),
                (untable,	            _(u"MECplugins|List utils|Row lists from ReST simple table")	   , _(u"untable")),
                (untable,	            _(u"MECplugins|List utils|Column lists from ReST simple table")       , _(u"untable")),
                )

def describeToolbarItems(wiki):
    return (	)

def remove_duplicates(wiki, evt):
    start, end = wiki.getActiveEditor().GetSelection()
    if wiki.getCurrentWikiWord() is None:
        return
    content = wiki.getActiveEditor().GetSelectedText()
    if not content:
        content = wiki.getActiveEditor().GetText()
    rows = content.split('\n')
    rows = list(set(rows))
    wiki.getActiveEditor().ReplaceSelection(str('\n'.join(rows)))
    wiki.getActiveEditor().SetSelection(start, end)


def sortSelection(wiki, evt):
    start, end = wiki.getActiveEditor().GetSelection()
    if wiki.getCurrentWikiWord() is None:
        return
    content = wiki.getActiveEditor().GetSelectedText()
    if not content:
        content = wiki.getActiveEditor().GetText()
    rows = content.split('\n')
    rows.sort()
    wiki.getActiveEditor().ReplaceSelection(str('\n'.join(rows)))
    wiki.getActiveEditor().SetSelection(start, end)

def invertSelection(wiki, evt):
    start, end = wiki.getActiveEditor().GetSelection()
    if wiki.getCurrentWikiWord() is None:
        return
    content = wiki.getActiveEditor().GetSelectedText()
    if not content:
        content = wiki.getActiveEditor().GetText()
    rows = content.split('\n')
    rows.reverse()
    wiki.getActiveEditor().ReplaceSelection(str('\n'.join(rows)))
    wiki.getActiveEditor().SetSelection(start, end)

def ziplists(wiki, evt):
    pass

def unziplists(wiki, evt):
    start, end = wiki.getActiveEditor().GetSelection()
    if wiki.getCurrentWikiWord() is None:
        return
    content = wiki.getActiveEditor().GetSelectedText()
    if not content:
        content = wiki.getActiveEditor().GetText()
    rows = content.split(linesep)

    odd  = rows[::2]
    even = rows[1::2]

    wiki.getActiveEditor().ReplaceSelection(str(linesep.join(odd) + linesep*2 + str(linesep.join(even))))
    wiki.getActiveEditor().SetSelectionByCharPos(start, end+2)

def pad_strings_in_list_to_maxlength(testlist):
    maxlen = len(max(testlist, key=len))
    out=[]
    out.append('='*maxlen+' ')
    out.extend([item.ljust(maxlen+1," ") for item in testlist])
    return out

def table(wiki, evt):
    start, end = wiki.getActiveEditor().GetSelection()
    if wiki.getCurrentWikiWord() is None:
        return
    content = wiki.getActiveEditor().GetSelectedText()
    if not content:
        content = wiki.getActiveEditor().GetText

    content = linesep.join( [a.strip() for a in content.splitlines()] )
    content = content.replace("\n\n", "\n..\n")

    if content.count("|||\n"):
        texts=content.split("|||\n")
        lists=[]
        for lt in texts:
            lists.append(lt.splitlines())

        maxlength=len(max(lists, key=len))

        print [a.extend([".."]*(maxlength-len(a))) for a in lists]

    elif content.count("---\n"):
        texts=content.split("---\n")
        lists=[]
        for lt in texts:
            lists.append(lt.splitlines())

        lists = list(itertools.izip_longest(*lists, fillvalue = ".."))
    else:
        return

    paddedlists=[]
    for lt in lists:
        paddedlists.append(pad_strings_in_list_to_maxlength(lt))

    rows=zip(*paddedlists)

    separator = "".join(rows[0])
    combinedlist=[separator]
    combinedlist.append("Table:")
    combinedlist.append("-"*(len(separator)-1))
    combinedlist.append("".join(rows[1]))
    combinedlist.append(separator)

    for row in rows[2:]:
        combinedlist.append("".join(row))
    combinedlist.append(separator)

    #print combinedlist
    new_text='\n'.join(combinedlist)
    wiki.getActiveEditor().ReplaceSelection(new_text)
    wiki.getActiveEditor().SetSelection(start, start+len(new_text))

def untable(wiki, evt):
    start, end = wiki.getActiveEditor().GetSelection()
    if wiki.getCurrentWikiWord() is None:
        return
    content = wiki.getActiveEditor().GetSelectedText()
    if not content:
        content = wiki.getActiveEditor().GetText

    rows = content.splitlines()

    #rows = [a for a in rows if a.strip(" =")]

    number_of_rows = len(rows)

    content = linesep.join( ["".join(a) for a in zip(*rows)] )

    columns = [a.strip() for a in content.split(' '*number_of_rows)]

    #print columns

    lists=[]

    for a in columns:
        lists.append([''.join(b) for b in (zip(*a.splitlines()))])

    #print lists


    result ='\n--\n'.join( ["\n".join(a) for a in zip(*lists) ] )

    new_text=result
    wiki.getActiveEditor().ReplaceSelection(new_text)
    wiki.getActiveEditor().SetSelection(start, start+len(new_text))
