# Cloud Backup v.1.1.filedev - Copyright (C) 2022, TRMSC - https://trmsc1.wordpress.com/ 
# GNU General Public Licence 3.0 - http://www.gnu.de/documents/gpl-3.0.en.html 

import configparser

print ("Welcome to the settings for your cloud-backup (v.1.1)")

def startSettings():
    x = input ("\nDo you want to start the auto (1) or custom (2) settings? Type (3) for exit. ")
    x = int(x)
    if x==1:
        setAuto()
    elif x==2:
        setCustom()
    elif x==3:
        exit()
    else:
        startSettings()

def setAuto():
    print ("Start auto settings...")
    print ("\nGENERAL")

def setCustom():
    print ("Start custom settings...")
    print ("\nGENERAL SETTINGS")
    print ("1 - Change directory")
    print ("2 - Number of stored backups")
    print ("\nACCESS DECLARATIONS")
    print ("3 - Set username")
    print ("4 - Set password")
    print ("\nADRESSBOOK BACKUP")
    print ("6 - Activate adressbook backup")
    print ("5 - Adressbook url")
    print ("\nCALENDAR BACKUP")
    print ("6 - Activate calendar backup")
    print ("7 - Calendar url")
    print ("8 - Calendar list")
    print ("\nDATA BACKUP")
    print ("9 - Activate data backup from desktop client")
    print ("10 - Client path")
    x = input ("\nWhich number do you want to change? ")
    print (x)

startSettings()
