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
    print ("\nBackup directory: " + val[1])
    print ("Stored backup days: " + val[2])
    print ("\nUsername: " + val[3])
    print ("Password: " + encr)
    print ("\nAdressbook storage activated: " + val[5])
    print ("Adressbook URL: " + val[6])
    print ("\nCalendar storage activated: " + val[7])
    print ("Calendar URL: " + val[8])
    print ("Calendar list: " + val[9])
    print ("\nClient storage activated: " + val[10])
    print ("Local client directory: " + val[11])
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
    print ("5 - Activate adressbook backup")
    print ("6 - Adressbook url")
    print ("\nCALENDAR BACKUP")
    print ("7 - Activate calendar backup")
    print ("8 - Calendar url")
    print ("9 - Calendar list")
    print ("\nDATA BACKUP")
    print ("10 - Activate data backup from desktop client")
    print ("11 - Client path")
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
    if item == 3:
        place = "user"
        print ("Username is: " + str(val[item]))
    if item == 4:
        place = "pwd"
        print ("Password is: " + str(val[item]))
    if item == 5:
        place = "cardAct"
        print ("Adressbook storage activated: " + str(val[item]))
    if item == 6:
        place = "card"
        print ("Adressbook URL is: " + str(val[item]))
    if item == 7:
        place = "calAct"
        print ("Calendar storage activated: " + str(val[item]))
    if item == 8:
        place = "cal"
        print ("Calendar URL is: " + str(val[item]))
    if item == 9:
        place = "callist"
        print ("Calendar URL is: " + str(val[item]))
    if item == 10:
        place = "clientAct"
        print ("Client storage activated: " + str(val[item]))
    if item == 11:
        place = "client"
        print ("Client path is: " + str(val[item]))
    if item == 11 and depart == 1:
        input ("Congratulations! Setting ist complete! Press enter to return.")
        startMain()   

    if item == 5 or item == 7 or item == 10:
        change = input ("Type (0) for deactivate, (1) for activate or press (x) for exit: ")
        if change == "0":
            change = "false"
        elif change == "1":
            change = "true"
    # remaining: encrypt password input
    # remaining: calendarlist
    else:
        change = input ("Type in a new value or press (x) for exit: ")

    if change == "x" and depart == 1:
        startMain()
    elif change == "x" and depart == 2:
        setCustom(depart)
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
            setCustom(depart)
    return

startMain()
