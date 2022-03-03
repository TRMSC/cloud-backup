# Cloud Backup v.1.0.1.rmdev - Copyright (C) 2022, TRMSC - https://trmsc1.wordpress.com/ 
# GNU General Public Licence 3.0 - http://www.gnu.de/documents/gpl-3.0.en.html 

# Prepare the backdata.txt and put it in the same directory like this script.
# Then you can backup your calendars and adressbook directly from the cloud.

import requests
import datetime
import os
import shutil

print ("Cloud Backup v.1.0")
print ("Feel free to visit trmsc1.wordpress.com")
print ("\nChecking data...")

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
    maintain = int(maintain) + 1   
    user = content[12]
    user = user.replace('\n', "")
    passwd = content[13]
    passwd = passwd.replace('\n', "")
    urlvcf = content[16] + "?export"
    urlvcf = urlvcf.replace('\n', "")
    url = content[19]
    calendarlist = content[23].replace('\n', "").split(",")
    print ("Start backup progress...")

# Check and create directory
if not os.path.exists(backupdir):
    os.makedirs(backupdir)

# Calendar download
for i in calendarlist:
    filename = backupdir + filedate + "-" + i + ".ics"
    print ("Downloading " + filename + "...")
    calurl = url + i + "/?export"
    calurl = calurl.replace('\n', "")
    r = requests.get(calurl, auth = (user, passwd), allow_redirects = True)
    with open(filename, 'wb') as k:
        k.write(r.content)
 
# Adressbook download
filename = backupdir + filedate + "-adressbook.vcf"
print ("Downloading " + filename + "...")
r = requests.get(urlvcf, auth=(user, passwd),allow_redirects=True)
with open(filename, 'wb') as a:
    a.write(r.content)

# Remove older versions
print ("\nRemove older versions...")
def sorted_ls(path):
    mtime = lambda f: os.stat(os.path.join(path, f)).st_ctime
    return list(sorted(os.listdir(path), key = mtime))
del_list = sorted_ls(path)[0:(len(sorted_ls(path)) - maintain)]
for dfile in del_list:
    shutil.rmtree(path + dfile)

# Finish
print ("\nBackup finished")
