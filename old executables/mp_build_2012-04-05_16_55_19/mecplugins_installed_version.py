# -*- coding: utf-8 -*-

WIKIDPAD_PLUGIN = (("MenuFunctions",1),)


def describeMenuItems(wiki):
    return ((version, _(u"mecplugins|about mec plugins"), _(u"about mec plugins")),)

def version(wiki, evt):
    from WikidPadStarter import VERSION_STRING
    message ='mecplugins installer file:\n\n'
    import os
    import mecplugins_ini

    try:

        f=open(os.path.join(mecplugins_ini.mecplugins_dir,"mecplugins_licenses","mecplugins_installation_log.txt"),'r')
        lines = f.read().splitlines()
        message += lines[-1]+"\n\n"
        f.close()

    except IOError:
        pass

    message += "wikidPad version: "+VERSION_STRING+"\n\n"

    import sys
    message += "Python version: "+sys.version+"\n\n"
    import Bio
    message +="BioPython version: "+Bio.__version__+"\n\n"
    import platform
    message +="Platform: "+platform.platform()+"\n\n"
    del Bio,sys, mecplugins_ini,os,platform, VERSION_STRING

    slask = wiki.stdDialog("text", "Installed version of mec plugins",message,message)

