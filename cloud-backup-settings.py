# Cloud Backup v.1.1.filedev - Copyright (C) 2022, TRMSC - https://trmsc1.wordpress.com/ 
# GNU General Public Licence 3.0 - http://www.gnu.de/documents/gpl-3.0.en.html 

import configparser
import numbers
import os

config = configparser.ConfigParser()

print ("Welcome to the settings for your cloud-backup (v.1.1)\n")

def startSettings():
    val = readData()
    printData(val)
    depart = input ("\nDo you want to start the auto (1) or custom (2) settings? Type (3) for exit. ")
    depart = int(depart)
    if depart == 1:
        setAuto(depart)
    elif depart == 2:
        setCustom(depart)
    elif depart == 3:
        exit()
    else:
        startSettings()

def readData():

    data = os.path.dirname(__file__) 
    data = data + "/data.ini"
    print (data)
    config.read (data)
    val = []
    x = 0
    for key in config["GENERAL"]:  
        val.append(config["GENERAL"][key])
    return (val)

def printData(val):
    encr = ""
    x = 0
    while x < len(val[4]):
        encr += "*"
        x += 1

    print ("Last modified: " + val[0])
    print ("Backup directory: " + val[1])
    print ("Stored backup days: " + val[2])
    print ("Username: " + val[3])
    print ("Password: " + encr)
    print ("Adressbook URL: " + val[5])
    print ("Calendar URL: " + val[6])
    print ("Calendar list: " + val[7])
    print ("Local client directory: " + val[8])


def setAuto(depart):
    print ("Start auto settings...")
    print ("\nGENERAL")

def setCustom(depart):
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
