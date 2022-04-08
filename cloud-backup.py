# Cloud Backup v.1.1filedev - Copyright (C) 2022, TRMSC - https://trmsc1.wordpress.com/ 
# GNU General Public Licence 3.0 - http://www.gnu.de/documents/gpl-3.0.en.html 

# Prepare the backdata.txt and put it in the same directory like this script.
# Then you can backup your calendars and adressbook directly from the cloud.

import configparser
import requests
import datetime
import os
import shutil
import zipfile

def getData():
    config = configparser.ConfigParser()
    data = os.path.dirname(__file__) 
    data = data + "/data.ini"
    config.read (data)
    val = []
    for key in config["GENERAL"]:  
        val.append(config["GENERAL"][key])
    return val

def checkSlash(check, variant):
    if variant == 1:
        check = os.path.normpath(check)
        if not check.endswith(os.path.sep):
            check += os.path.sep
    elif variant == 2 and check[-1] != "/":
        check = check + "/"
    return check

print ("Cloud Backup v.1.1filedev")
print ("Feel free to visit trmsc1.wordpress.com")

val = getData()

# Make Functions:
# PREPARE
# START (CARD, CALENDAR, DATA)
# FINISH

print ("\nPreparing backup...")
starttime = datetime.datetime.now()
folderdate = datetime.datetime.now().strftime("%Y-%m-%d")
filedate = folderdate + datetime.datetime.now().strftime("-%H-%M")
print ("Time: " + filedate)
path = checkSlash(val[1], 1)
backupdir = path + folderdate
backupdir = checkSlash(backupdir, 1)
print ("Backup directory: " + backupdir)
maintain = val[2]
print ("Number of older stored subdirectories: " + maintain)
maintain = int(maintain) 
user = val[3]
passwd = val[4]
card = val[5]
print ("Adressbook backup: " + card)
urlvcf = checkSlash(val[6], 2)
urlvcf = urlvcf + "?export"
calendar = val[7]
print ("Calendar backup: " + calendar)
url = checkSlash(val[8], 2)
calendarlist = val[9].replace('\n', "").split(",")
clouddata = val[10]
print ("Data backup: " + clouddata)
clientfolder = checkSlash(val[11], 1)

# PREPARE
if not os.path.exists(path):
    os.makedirs(path)

print ("\nCheck older versions for cleaning...")
if os.path.exists(backupdir):
    maintain = maintain + 1
def sorted_ls(path):
    mtime = lambda f: os.stat(os.path.join(path, f)).st_ctime
    return list(sorted(os.listdir(path), key = mtime))
del_list = sorted_ls(path)[0:(len(sorted_ls(path)) - maintain)]
printDel = ",".join(del_list)
if printDel == "":
    print ("none")
else:
    print (printDel)

if not os.path.exists(backupdir):
    os.makedirs(backupdir)

# START
print ("\nStart backup progress...")

# CALENDAR
for i in calendarlist:
    filename = backupdir + filedate + "-" + i + ".ics"
    print ("Downloading " + filename)
    calurl = url + i + "/?export"
    calurl = calurl.replace('\n', "")
    r = requests.get(calurl, auth = (user, passwd), allow_redirects = True)
    with open(filename, 'wb') as k:
        k.write(r.content)
 
# ADRESSBOOK
filename = backupdir + filedate + "-adressbook.vcf"
print ("Downloading " + filename)
r = requests.get(urlvcf, auth=(user, passwd),allow_redirects=True)
with open(filename, 'wb') as a:
    a.write(r.content)
    
# DATA
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

# FINISH
print ("\nClean older versions...")
if del_list == []:
    print ("none")
for dfile in del_list:
    print ("Removing " + path + dfile)
    shutil.rmtree(path + dfile)

endtime = datetime.datetime.now()
duration = endtime - starttime
print ("\nBackup finished after a duration of " + str(duration))
