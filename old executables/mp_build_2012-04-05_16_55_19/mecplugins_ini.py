# -*- coding: utf-8 -*-

import sys
import os

wikiAppDir                 = os.path.dirname(os.path.abspath(sys.argv[0]))
mecplugins_dir             = os.path.join(wikiAppDir,"user_extensions", "mecplugins")
mecplugins_settings_folder = os.path.join(mecplugins_dir,"mecplugins_settings_pages")

# for all platforms:
sys.path.append(mecplugins_dir)

if sys.platform == 'win32':
    # only for windows using directories added by mec plugins installers
    reload(sys)
    sys.setdefaultencoding('utf-8') #'iso-8859-1'
    # http://blog.doughellmann.com/2008/02/pymotw-imp.html
    import imp
    #print sys.path_hooks
    slabb = sys.path_importer_cache
    sys.path_importer_cache = {}

    pth = os.path.join(mecplugins_dir,"lib","Lib","site-packages","wx-2.8-msw-unicode")
    fp, pathname, description = imp.find_module("wx", [pth])
    try:
        imp.load_module("wx", fp, pathname, description)
    finally:
        if fp:
            fp.close()
    #import wx
    #print wx.__file__
    #import wx.stc
    #print wx.stc.__file__


    pth = os.path.join(mecplugins_dir,"lib","Lib","xml")
    fp, pathname, description = imp.find_module("etree", [pth])
    try:
        imp.load_module("xml.etree",fp , pathname, description)
    finally:
        if fp:
            fp.close()
    #from xml.etree import ElementTree as ElementTree

    pth = os.path.join(mecplugins_dir,"lib","Lib")
    fp, pathname, description = imp.find_module("email", [pth])
    try:
        imp.load_module("email",fp , pathname, description)
    finally:
        if fp:
            fp.close()

    pth = os.path.join(mecplugins_dir,"lib","Lib","email")
    fp, pathname, description = imp.find_module("mime", [pth])
    try:
        imp.load_module("email.mime",fp , pathname, description)
    finally:
        if fp:
            fp.close()

    sys.path.append(os.path.join(mecplugins_dir,"lib"))
    sys.path.append(os.path.join(mecplugins_dir,"lib","Lib"))
    sys.path.append(os.path.join(mecplugins_dir,"lib","Lib","email"))
    sys.path.append(os.path.join(mecplugins_dir,"lib","Lib","site-packages"))
    sys.path.append(os.path.join(mecplugins_dir,"lib","Lib","site-packages","Bio"))

    sys.path_importer_cache = slabb