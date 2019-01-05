WIKIDPAD_PLUGIN = (("hooks", 1),)

def openedWiki(wikidPad, wikiName, wikiConfig):
    """
    Called when an existing wiki was opened successfully

    wikidPad -- PersonalWikiFrameObject
    wikiName -- name of the wiki
    wikiConfig -- path to the .wiki config file
    """

    if wikiName == "WikidPadHelp": 
        return

    import os
    import mecplugins_ini

    path_to_folder      = mecplugins_ini.mecplugins_settings_folder
    settings_files      = os.listdir(path_to_folder)

    for settings_file in settings_files:
        wikipagename, extension = os.path.splitext(settings_file.replace("%2F","/"))
        if extension ==".wiki":
            if not wikidPad.wikiDataManager.isDefinedWikiWord(wikipagename):
                f = open(os.path.join(path_to_folder, settings_file),'r')
                pagetext = f.read()
                f.close()
                wikidPad.getWikiDocument().getWikiPageNoError(wikipagename).replaceLiveText(pagetext)
                #wikidPad.getWikiDocument().getWikiPageNoError(wikipagename).replaceLiveText(unicode(pagetext,'utf-8'))
    return

