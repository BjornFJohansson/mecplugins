########################################
# |  \/  |     (_) | |  | | | (_) |
# | \  / | __ _ _| | |  | | |_ _| |___
# | |\/| |/ _` | | | |  | | __| | / __|
# | |  | | (_| | | | |__| | |_| | \__ \
# |_|  |_|\__,_|_|_|\____/ \__|_|_|___/
########################################
# -*- coding: utf-8 -*-
WIKIDPAD_PLUGIN = (("MenuFunctions",1),("ToolbarFunctions",1))
#WIKIDPAD_PLUGIN = (("MenuFunctions",1),)

import MECplugins_ini

import codecs
import tempfile
import zipfile
import smtplib
import os
import sys
import string

from pwiki.StringOps            import pathnameFromUrl
from pwiki.StringOps            import mbcsEnc, strftimeUB
from pwiki.WikiExceptions       import WikiFileNotFoundException
from pwiki.PersonalWikiFrame    import PersonalWikiFrame

from email                      import encoders
from email.mime.multipart       import MIMEMultipart
from email.mime.base            import MIMEBase
from email.mime.text            import MIMEText

def describeMenuItems(wiki):
    return ((sendbymail, _(u"mecplugins|Send selected text by mail"), _(u"mail selection")),)

def describeToolbarItems(wiki):
    return ((sendbymail, _(u"mail selection"), _(u"mail selection"), "mail"),)

def recursive_zip(zipf, directory):
    list = os.listdir(directory)
    for file in list:
        fullpath = os.path.join(directory, file)
        if os.path.isfile(fullpath):
            zipf.write(fullpath, fullpath)
        elif os.path.isdir(file):
            recursive_zip(zipf, os.path.join(directory, file))
            
def sendbymail(wiki, evt):
    CurrentWikiWord=wiki.getCurrentWikiWord()
    if CurrentWikiWord is None:
        return
    content = wiki.getActiveEditor().GetSelectedText()
    if not content:
        return

    docPage = wiki.getCurrentDocPage()
    pageAst = docPage.parseTextInContext(content)
    urlNodes = pageAst.iterDeepByName("urlLink")
    paths=[]
    recipients_in_text=[]
    themsg = MIMEMultipart()

    for node in urlNodes:
        if node.url.startswith("rel") or node.url.startswith("file"):
            paths.append(pathnameFromUrl(wiki.makeRelUrlAbsolute(node.url)))
        if node.url.startswith("mailto:"):
            recipients_in_text.append(node.url[7:])
            content = "".join(content.split(node.url))

    if paths:
        response = wiki.stdDialog("ync", "Mail selected text", "Zip linked files and send as attachment?")
    else:
        response = "not set"
        
    if response == "cancel":
        return

    if response == "yes":

        filelist = []
        path_not_found = []
        
        for path in paths:
            if os.path.isfile(path):
                filelist.append(path)
            elif os.path.isdir(path):
                for root, subFolders, files in os.walk(path):
                    for file in files:
                        filelist.append(os.path.join(root,file))
            else:
                path_not_found.append(path)
        
        filelist = list(set(filelist))

        if path_not_found:
            no_of_missing_paths = len(path_not_found)
            missing_paths = "\n".join(path_not_found[0:5])
            response = wiki.stdDialog("o","Mail selected text", string.Template("$no_of_missing_paths files or directories are missing\n\n $missing_paths\n\nOperation was canceled!").substitute(vars()))
            return
            
        zipfilename = strftimeUB("%Y-%m-%d|%A %B %d|%H:%M:%S")+'.zip'
        zf = tempfile.TemporaryFile()
        zip = zipfile.ZipFile(zf, 'w',zipfile.ZIP_DEFLATED)

        if len(filelist)>1:
            commonprefix = os.path.commonprefix(filelist)
        else:
            commonprefix = os.path.split(filelist[0])[0]

        for path in filelist:
            zip.write(path,path.split(commonprefix)[-1])       
        
#        for path in paths:
#            if os.path.isfile(path):
#                zip.write(path,path)
#            elif os.path.isdir(path):
#                recursive_zip(zip, path)
                
        zip.close()
 
        zf.seek(0)
        attached_zip = zf.read()
        if attached_zip:
            msg = MIMEBase('application', 'zip')
            msg.set_payload(attached_zip)
            encoders.encode_base64(msg)
            msg.add_header('Content-Disposition', 'attachment', filename=zipfilename)
            themsg.attach(msg)

    exec(wiki.getWikiDocument().getWikiPage("WikiSettings/MECplugins/mail-settings").getContent().encode())

    recipients_from_settings_page = wiki.getWikiDocument().getWikiPage("WikiSettings/MECplugins/mail-contacts").getContent().encode().splitlines()
    selected_recipients=[]
    selected_recipients=wiki.stdDialog("listmcstr", "Mail selected text", "Choose one or more recipients:", recipients_from_settings_page)
    
    recipients = recipients_in_text + selected_recipients

    if not recipients:
        wiki.stdDialog("o", "Mail selected text","No recipients selected")
        return

    content = content.encode()

    themsg['From']         = sentfrom
    themsg['To']           = ", ".join(recipients)
    themsg['Bcc']          = extra_recipient
    themsg['Subject']      = subject
    themsg.preamble = 'I am not using a MIME-aware mail reader.\n'
    themsg.attach(MIMEText(content))

    if extra_recipient and not extra_recipient.isspace():
        recipients.append(extra_recipient.encode())

    session = smtplib.SMTP(smtpserver,smtpport,smtphostname,smtptimeout)
    session.ehlo()
    session.starttls()
    session.ehlo()
    session.login(smtpuser, smtppass)

    smtpresult = session.sendmail(sender, recipients, themsg.as_string())

    if smtpresult:
        report = "Mail(s) could not be sent!\n"
        for recip in smtpresult.keys():
            report = """Could not deliver mail to: %s

    Server said: %s
    %s

    %s""" % (recip, smtpresult[recip][0], smtpresult[recip][1], report)

        #raise smtplib.SMTPException, report
    else:
        report = "mail sent "+now + " to \n" + "\n".join(recipients)

    print report

    wiki.stdDialog("o", "Mail selected text", report)

    return




'''
import smtplib

FROMADDR = "padwikid@gmail.com"
LOGIN    = FROMADDR
PASSWORD = "ch2p9AQuR8tHaSp76egeDRUWu"
TOADDRS  = ["bjornjobb@gmail.com"]
SUBJECT  = "Test"

msg = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n"
       % (FROMADDR, ", ".join(TOADDRS), SUBJECT) )
msg += "some text\r\n"

server = smtplib.SMTP('smtp.gmail.com', 587)
server.set_debuglevel(1)
server.ehlo()
server.starttls()
server.login(LOGIN, PASSWORD)
server.sendmail(FROMADDR, TOADDRS, msg)
server.quit()
'''
