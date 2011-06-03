##########################################################################
#   ____                              _ _   _                      ______
#  / __ \                            (_) | | |         /\         |  ____|
# | |  | |_ __   ___ _ __   __      ___| |_| |__      /  \   _ __ | |__
# | |  | | '_ \ / _ \ '_ \  \ \ /\ / / | __| '_ \    / /\ \ | '_ \|  __|
# | |__| | |_) |  __/ | | |  \ V  V /| | |_| | | |  / ____ \| |_) | |____
#  \____/| .__/ \___|_| |_|   \_/\_/ |_|\__|_| |_| /_/    \_\ .__/|______|
#        | |                                                | |
#        |_|                                                |_|
##########################################################################
# -*- coding: latin-1 -*-
## http://209.85.135.132/search?q=cache:kIj5Feoa3o0J:docs.python.org/library/tempfile.html+python+make+temp+file&cd=1&hl=en&ct=clnk&gl=pt
## http://blog.doughellmann.com/2008/02/pymotw-tempfile.html

#WIKIDPAD_PLUGIN = (("MenuFunctions",1),)
WIKIDPAD_PLUGIN = (("MenuFunctions",1), ("ToolbarFunctions",1))
import MECplugins_ini
import codecs
import tempfile
import sys
import os
import subprocess

from parse_string2 import parse_text_into_list_of_seqs, parse_raw_sequence_into_fasta

def describeMenuItems(wiki):
    return((openwithape,       _(u"MECplugins|DNA Sequence Tools|Open selection with ApE") + u"\tCtrl-D", _(u"ApE")),
          )

def describeToolbarItems(wiki):
    return ((openwithape, _(u"open selection with ApE"), _(u"ApE"), "ape"),)

def openwithape(wiki, evt):
    if wiki.getCurrentWikiWord() is None:
        return

    content = wiki.getActiveEditor().GetSelectedText()

    if not content:

        cursorline = wiki.getActiveEditor().GetCurrentLine()
        textlines  = wiki.getActiveEditor().GetText().split("\n")

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
            content = seq.record.format(seq.format)

    #print content
 

    # get settings
    exec(wiki.getWikiDocument().getWikiPage("WikiSettings/MECplugins/open with ape").getContent().encode())

    if sys.platform == 'linux2':
        path_to_ape = path_to_ape_lin

    if sys.platform == 'win32':
        path_to_ape = path_to_ape_win

    if sys.platform == 'darwin':
        path_to_ape = path_to_ape_mac

    if content:
        path = os.path.join(tempfile.gettempdir(),"WikidPad","sequences")
        try:
            os.makedirs(path)
        except OSError:
            pass
        path = tempfile.mkdtemp(dir=path)
        seqs = parse_text_into_list_of_seqs(content)

        if not seqs:
            seqs = parse_raw_sequence_into_fasta(content)
        
        pathstofiles=[]
        for seq in seqs:
            filename = seq.record.id+"."+seq.format
            pathtofile = os.path.join(path,filename) 
            f = open(pathtofile,"w")
            f.write(seq.raw)
            f.close()
            pathstofiles.append(pathtofile)
        p = subprocess.Popen(path_to_ape + ' ' + ' '.join(pathstofiles), shell=True)

    else: # no selection, open empty window
        p = subprocess.Popen(path_to_ape, shell=True)


