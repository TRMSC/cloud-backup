#!/usr/bin/env python3

# Cloud Backup - Copyright (C) 2022, TRMSC - https://trmsc1.wordpress.com/ 
# GNU General Public Licence 3.0 - http://www.gnu.de/documents/gpl-3.0.en.html 

# Prepare the backdata.txt and put it in the same directory like this script.
# Then you can backup your calendars and adressbook directly from the cloud.

import configparser
import requests
import datetime
import os
import shutil
import zipfile

version = "v.1.2.1"

def getData():
    config = configparser.ConfigParser()
    data = os.path.dirname(__file__) 
    data = data + "/data.ini"
    config.read (data)
    for key in config["GENERAL"]:  
        val.append(config["GENERAL"][key])
    return val

def stampTime():
    starttime = datetime.datetime.now()
    folderdate = datetime.datetime.now().strftime("%Y-%m-%d")
    filedate = folderdate + datetime.datetime.now().strftime("-%H-%M")
    return starttime, folderdate, filedate

def checkSlash(check, variant):
    if variant == 1:
        check = os.path.normpath(check)
        if not check.endswith(os.path.sep):
            check += os.path.sep
    elif variant == 2 and check[-1] != "/":
        check = check + "/"
    return check

def prepareOverarching():
    path = checkSlash(val[1], 1)
    backupdir = path + folderdate
    backupdir = checkSlash(backupdir, 1)
    print ("Backup directory: " + backupdir)
    maintain = val[2]
    print ("Number of older stored subdirectories: " + maintain)
    maintain = int(maintain) 
    user = val[3]
    passwd = val[4]
    return path, backupdir, maintain, user, passwd

def backupCheck():
    card = val[5]
    print ("Adressbook backup: " + card)
    calendar = val[7]
    print ("Calendar backup: " + calendar)
    clouddata = val[10]
    print ("Data backup: " + clouddata)
    if not os.path.exists(path):
        os.makedirs(path)
    return

def prepareFolders(maintain):
    print ("\nCheck older versions for cleaning...")
    if os.path.exists(backupdir):
        maintain = maintain + 1
    def makeList(path):
        mtime = lambda f: os.stat(os.path.join(path, f)).st_ctime
        return list(sorted(os.listdir(path), key = mtime))
    removeDir = makeList(path)[0:(len(makeList(path)) - maintain)]
    printDir = ",".join(removeDir)
    if printDir == "":
        print ("none")
    else:
        print (printDir)
    if not os.path.exists(backupdir):
        os.makedirs(backupdir)
    return removeDir

def storeAdressbook():
    urlvcf = checkSlash(val[6], 2)
    urlvcf = urlvcf + "?export"
    filename = backupdir + filedate + "-adressbook.vcf"
    print ("Downloading " + filename)
    r = requests.get(urlvcf, auth=(user, passwd),allow_redirects=True)
    with open(filename, 'wb') as a:
        a.write(r.content)
    return

def storeCalendar():
    url = checkSlash(val[8], 2)
    calendarlist = val[9].replace('\n', "").split(",")
    for i in calendarlist:
        filename = backupdir + filedate + "-" + i + ".ics"
        print ("Downloading " + filename)
        calurl = url + i + "/?export"
        calurl = calurl.replace('\n', "")
        r = requests.get(calurl, auth = (user, passwd), allow_redirects = True)
        with open(filename, 'wb') as k:
            k.write(r.content)
    return

def storeData():
    clientfolder = checkSlash(val[11], 1)
    clientfile = backupdir + filedate + "-localfiles.zip"
    countfiles = 0
    print ("\nCreate " + clientfile + " and add files...")
    with zipfile.ZipFile(clientfile, 'w', zipfile.ZIP_DEFLATED) as target:
        for root, dirs, files in os.walk(clientfolder):
            for file in files:
                add = os.path.join(root, file)
                target.write(add)
                print("Add " + add)
                countfiles +=1
    print (str(countfiles) + " files were added to " + clientfile)
    return

def finishBackup():
    print ("\nClean older versions...")
    if removeDir == []:
        print ("none")
    for dfile in removeDir:
        print ("Removing " + path + dfile)
        shutil.rmtree(path + dfile)
    endtime = datetime.datetime.now()
    duration = endtime - starttime
    print ("\nBackup finished after a duration of " + str(duration))
    return

print ("Cloud Backup " + version)
print ("Feel free to visit trmsc1.wordpress.com")
val = []
val = getData()
print ("\nPreparing backup...")
starttime, folderdate, filedate = stampTime()
print ("Time: " + filedate)
path, backupdir, maintain, user, passwd = prepareOverarching()
backupCheck()
removeDir = prepareFolders(maintain)
print ("\nStart backup progress...")
if val[5] == "yes":
    storeAdressbook()
if val[7] == "yes":
    storeCalendar()
if val[10] == "yes":
    storeData()
finishBackup()
