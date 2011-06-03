# -*- coding: latin-1 -*-
WIKIDPAD_PLUGIN = (("ToolbarFunctions",2), ("ToolbarFunctions",1), ("MenuFunctions",1))
#WIKIDPAD_PLUGIN = (("MenuFunctions",1),)

import MECplugins_ini

def describeMenuItems(wiki):
    return ((openToDo, _(u"MECplugins|Shortcuts|ToDo"), _(u"ToDo")),)

def describeToolbarItemsV02(wiki):
    return ((openToDo, _(u"open ToDo page"), _(u"ToDo page"), ("spanner",)   ,None,   None, ToDorightclick),)


def openToDo(wiki, evt):
    wiki.openWikiPage("ToDoCalendar")
    return

def ToDorightclick(wiki, evt):
    presenter = wiki.createNewDocPagePresenterTab()    
    presenter.openWikiPage("ToDoCalendar")
    wiki.getMainAreaPanel().showPresenter(presenter)
    return
