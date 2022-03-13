#!/usr/bin/env python

# Cloud Backup v.1.1.filedev - Copyright (C) 2022, TRMSC - https://trmsc1.wordpress.com/ 
# GNU General Public Licence 3.0 - http://www.gnu.de/documents/gpl-3.0.en.html 

import configparser
import numbers
import os
import datetime

config = configparser.ConfigParser()

print ("Welcome to the settings for your cloud-backup (v.1.1)\n")

def startMain():
    val = readData()
    printData(val)
    depart = input ("\nDo you want to start auto (1) or custom (2) settings? Type (x) for exit. ")
    if depart == "x":
        exit()
    depart = int(depart)
    if depart == 1:
        startProgress(depart, 1)
    elif depart == 2:
        setCustom(depart)
    elif depart == 0:
        exit()
    else:
        startMain()
    return

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
    return

def setCustom(depart):
    val = readData()
    print ("Last modified: " + val[0])
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
    item = input ("\nWhich number do you want to change? Press (x) for exit. ")
    if item == "x":
        startMain()
    else:
        item = int(item)
        startProgress(depart, item)
    return

def startProgress(depart, item):
    val = readData()
    print ("")
    if depart == 1:
        percent = (item - 1) * 10
        print ("Setting progress: " + str(percent) + "%\n")
    if item == 1:
        place = "directory"
        print ("Backup directory is " + str(val[item]))
    if item == 2:
        place = "number"
        print ("Number of stored backup days: " + str(val[item]))
    if item == 11 and depart == 1:
        input ("Congratulations! Setting ist complete! Press enter to return.")
        startMain()   
    change = input ("Type in a new value or press (x) for exit: ")
    if change == "x":
        startMain()
    else:
        config["GENERAL"][place] = change
        config["GENERAL"]["date"] = datetime.datetime.now().strftime("%Y-%m-%d / %H-%M")
        data = os.path.dirname(__file__) 
        data = data + "/data.ini"
        with open(data, 'w') as configfile:
            config.write(configfile)
        if depart == 1:
            item +=1
            startProgress(depart, item)
        elif depart == 2:
            startMain()
    return

startMain()
