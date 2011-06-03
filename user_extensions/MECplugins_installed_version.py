# -*- coding: utf-8 -*-

WIKIDPAD_PLUGIN = (("MenuFunctions",1),)


def describeMenuItems(wiki):
    return ((version, _(u"MECplugins|about MEC plugins"), _(u"about MEC plugins")),)

def version(wiki, evt):
    from WikidPadStarter import VERSION_STRING
    message ='MECplugins installer file:\n\n'
    import os
    import MECplugins_ini

    try:

        f=open(os.path.join(MECplugins_ini.MECplugins_dir,"MECplugins_licenses","MECplugins_installation_log.txt"),'r')
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
    del Bio,sys, MECplugins_ini,os,platform, VERSION_STRING

    slask = wiki.stdDialog("text", "Installed version of MEC plugins",message,message)

