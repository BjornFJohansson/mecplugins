# -*- coding: utf-8 -*-
import os,sys

wikiAppDir                      = os.path.dirname(os.path.abspath(sys.argv[0]))
MECplugins_dir                  = os.path.join(wikiAppDir, "user_extensions", "MECplugins")
MECplugins_settings_folder      = os.path.join(MECplugins_dir,"MECplugins_settings_pages")

# for all platforms:
sys.path.append(MECplugins_dir)

if sys.platform == 'win32':
    # only for windows using directories added by MEC plugins installers
    sys.setdefaultencoding('utf-8') #'iso-8859-1'
    lib_dirs = []
    lib_dirs.append(os.path.join(MECplugins_dir,"lib"))
    lib_dirs.append(os.path.join(MECplugins_dir,"lib","dist-packages"))
    lib_dirs.append(os.path.join(MECplugins_dir,"lib","email"))
    sys.path = lib_dirs+sys.path

