# Cloud Backup v.1.1 - Copyright (C) 2022, TRMSC - https://trmsc1.wordpress.com/ 
# GNU General Public Licence 3.0 - http://www.gnu.de/documents/gpl-3.0.en.html 

# Prepare the backdata.txt and put it in the same directory like this script.
# Then you can backup your calendars and adressbook directly from the cloud.

import requests
import datetime
import os
import shutil
import zipfile

print ("Cloud Backup v.1.1")
print ("Feel free to visit trmsc1.wordpress.com")
print ("\nCheck data...")

# Check date
folderdate = datetime.datetime.now().strftime("%Y-%m-%d")
filedate = folderdate + datetime.datetime.now().strftime("-%H-%M")
print ("Time is " + filedate)

# Check data
with open("cloud-backup-data.txt", "r") as backdata:
    content = backdata.readlines ()
    path = content[6]
    path = path.replace('\n', "")
    backupdir = path + folderdate + "/"
    backupdir = backupdir.replace('\n', "")
    print ("Backup directory is " + backupdir)
    maintain = content[9]
    maintain = maintain.replace('\n', "")
    print (maintain + " older subdirectories will be stored\n")
    maintain = int(maintain)   
    user = content[12]
    user = user.replace('\n', "")
    passwd = content[13]
    passwd = passwd.replace('\n', "")
    urlvcf = content[16] + "?export"
    urlvcf = urlvcf.replace('\n', "")
    url = content[19]
    calendarlist = content[23].replace('\n', "").split(",")
    clientfolder = content[26]
    clientfolder = clientfolder.replace('\n', "")

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
print ("Create " + clientfile + " and ad files...")
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
    print ("[]")
for dfile in del_list:
    print ("Removing " + path + dfile)
    shutil.rmtree(path + dfile)

# Finish
print ("\nBackup finished")
