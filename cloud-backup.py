# Cloud Backup v.1.1 - Copyright (C) 2022, TRMSC - https://trmsc1.wordpress.com/ 
# GNU General Public Licence 3.0 - http://www.gnu.de/documents/gpl-3.0.en.html 

# Prepare the backdata.txt and put it in the same directory like this script.
# Then you can backup your calendars and adressbook directly from the cloud.

import configparser
import requests
import datetime
import os
import shutil
import zipfile

def checkSlash(check, variant):
    last = check[-1]
    if last != "/" and last != "\u005C":
        if variant == 0:
            return check
        else:
            check = check + "/"
            return check
    elif variant == 0:
        check = check[:-1]
    return check

print ("Cloud Backup v.1.1filedev")
print ("Feel free to visit trmsc1.wordpress.com")
print ("\nCheck data...")

# Check date
starttime = datetime.datetime.now()
folderdate = datetime.datetime.now().strftime("%Y-%m-%d")
filedate = folderdate + datetime.datetime.now().strftime("-%H-%M")
print ("Time is " + filedate)

# Check data
config = configparser.ConfigParser()
data = os.path.dirname(__file__) 
data = data + "/data.ini"
config.read (data)
val = []
x = 0
for key in config["GENERAL"]:  
    val.append(config["GENERAL"][key])
path = checkSlash(val[1])
path = os.path.normpath(path, 1)
backupdir = path + folderdate + "/"
backupdir = os.path.normpath(backupdir, 1)
print ("Backup directory is " + backupdir)
maintain = val[2]
print (maintain + " older subdirectories will be stored\n")
maintain = int(maintain) 
user = val[3]
passwd = val[4]
urlvcf = checkSlash(val[6])
url = checkSlash(val[8])
calendarlist = val[9].replace('\n', "").split(",")
clientfolder = val[11]
clientfolder = os.path.normpath(clientfolder, 0)

# Check and create storage directory
if not os.path.exists(path):
    os.makedirs(path)
    
# Check older versions
print ("\nCheck older versions for cleaning...")
if os.path.exists(backupdir):
    maintain = maintain + 1
def sorted_ls(path):
    mtime = lambda f: os.stat(os.path.join(path, f)).st_ctime
    return list(sorted(os.listdir(path), key = mtime))
del_list = sorted_ls(path)[0:(len(sorted_ls(path)) - maintain)]
print (del_list)

# Check and create todays subfolder
if not os.path.exists(backupdir):
    os.makedirs(backupdir)

# Start backup progress
print ("\nStart backup progress...")

# Calendar download
for i in calendarlist:
    filename = backupdir + filedate + "-" + i + ".ics"
    print ("Downloading " + filename)
    calurl = url + i + "/?export"
    calurl = calurl.replace('\n', "")
    r = requests.get(calurl, auth = (user, passwd), allow_redirects = True)
    with open(filename, 'wb') as k:
        k.write(r.content)
 
# Adressbook download
filename = backupdir + filedate + "-adressbook.vcf"
print ("Downloading " + filename)
r = requests.get(urlvcf, auth=(user, passwd),allow_redirects=True)
with open(filename, 'wb') as a:
    a.write(r.content)
    
# Copy and zip local client files
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

# Remove older versions
print ("\nClean older versions...")
if del_list == []:
    print ("none")
for dfile in del_list:
    print ("Removing " + path + dfile)
    shutil.rmtree(path + dfile)

# Finish
endtime = datetime.datetime.now()
duration = endtime - starttime
print ("\nBackup finished after a duration of " + str(duration))
