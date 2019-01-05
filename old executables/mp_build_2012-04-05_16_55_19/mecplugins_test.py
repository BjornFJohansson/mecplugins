# -*- coding: utf-8 -*-
##################################################
#  _______       _   _____  _             _
# |__   __|     | | |  __ \| |           (_)
#    | | ___ ___| |_| |__) | |_   _  __ _ _ _ __
#    | |/ _ | __| __|  ___/| | | | |/ _` | | '_ \
#    | |  __|__ \ |_| |    | | |_| | (_| | | | | |
#    |_|\___|___/\__|_|    |_|\__,_|\__, |_|_| |_|
#                                    __/ |
#                                   |___/
##################################################

WIKIDPAD_PLUGIN = (("MenuFunctions",1),)
import mecplugins_ini
import wx
import time

def describeMenuItems(wiki):
    return ((test, _(u"TEST") + u"\tCtrl-Shift-T", _(u"test")),)

def test(wiki,evt):

    #wikiname = wiki.getMainControl().wikiName
    #print wikiname
    #print dir(wiki.getMainControl())
    #bc=wx.BeginBusyCursor(cursor=wx.HOURGLASS_CURSOR)
    #time.sleep(6)
    #bc=wx.EndBusyCursor()

    #import locale
    #print "testplugin: this will be printed to the Error log"

    #if wiki.getCurrentWikiWord() is None:
    #    return

    print wiki.getActiveEditor().GetText().splitlines()[wiki.getActiveEditor().GetCurrentLine()]

    #print locale.getpreferredencoding()

    #print "testplugin: this will be printed to the Error log"






