# Cloud Backup v.1.0 - Copyright (C) 2022, TRMSC - https://trmsc1.wordpress.com/ 
# GNU General Public Licence 3.0 - http://www.gnu.de/documents/gpl-3.0.en.html 

# Prepare the backdata.txt and put it in the same directory like this script.
# Then you can backup your calendars and adressbook directly from the cloud.

import requests
import datetime
import os

print ("Cloud Backup v.1.0")
print ("Feel free to visit trmsc1.wordpress.com")
print ("\nChecking data...")

# Check date
datenow=datetime.datetime.now().strftime("%Y-%m-%d")
print ("Date is " + datenow)

# Check data
with open("cloud-backup-data.txt", "r") as backdata:
    content = backdata.readlines ()
    backupdir=content[6]
    backupdir=backupdir + datenow + "/"
    backupdir=backupdir.replace('\n',"")
    print ("Backup directory is " + backupdir + "\n")
    user=content[9]
    user=user.replace('\n',"")
    passwd=content[10]
    passwd=passwd.replace('\n',"")
    urlvcf=content[13] + "?export"
    urlvcf=urlvcf.replace('\n',"")
    url=content[16]
    calendarlist=content[20].replace('\n',"").split(",")

# Check and create directory
if not os.path.exists(backupdir):
    os.makedirs(backupdir)

# Calendar download
for i in calendarlist:
    filename=backupdir + datenow+"-"+i+".ics"
    print ("Downloading " + filename + "...")
    calurl=url+i+"/?export"
    calurl=calurl.replace('\n',"")
    r = requests.get(calurl, auth=(user, passwd),allow_redirects=True)
    with open(filename, 'wb') as k:
        k.write(r.content)
 
# Adressbook download
filename= backupdir + datenow + "-adressbook.vcf"
print ("Downloading " + filename + "...")
r = requests.get(urlvcf, auth=(user, passwd),allow_redirects=True)
with open(filename, 'wb') as a:
    a.write(r.content)

# Finish
print ("Backup finished")
