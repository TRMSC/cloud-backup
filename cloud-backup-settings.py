#!/usr/bin/env python

# Cloud Backup v.1.1.filedev - Copyright (C) 2022, TRMSC - https://trmsc1.wordpress.com/ 
# GNU General Public Licence 3.0 - http://www.gnu.de/documents/gpl-3.0.en.html 

import configparser
import numbers
import os
import datetime
import getpass
from pickle import TRUE

config = configparser.ConfigParser()

print ("\nWelcome to cloud-backup configuration (v.1.1)\n")

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
    config.read (data)
    val = []
    x = 0
    for key in config["GENERAL"]:  
        val.append(config["GENERAL"][key])
    return (val)

def printData(val):
    encr = encryptPwd(val)
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

def encryptPwd(val):
    encr = ""
    x = 0
    while x < len(val[4]):
        encr += "*"
        x += 1
    return encr

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
    item = input ("\nWhich number do you want to change? Press (x) for abort. ")
    if item == "x":
        startMain()
    else:
        item = int(item)
        startProgress(depart, item)
    return

def startProgress(depart, item):
    val = readData()
    print ("")
    if depart == 1 and item < 12:
        percent = (item - 1) * 9
        print ("### Setting progress: " + str(percent) + "% ###\n")
    if item == 1:
        place = "directory"
        print ("Backup directory is: " + str(val[item]))
    if item == 2:
        place = "number"
        print ("Number of stored backup days: " + str(val[item]))
    if item == 3:
        place = "user"
        print ("Username is: " + str(val[item]))
    if item == 4:
        encr = encryptPwd(val)
        place = "pwd"
        print ("Password is: " + encr)
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
        print ("Calendarlist is: " + str(val[item]))
    if item == 10:
        place = "clientAct"
        print ("Client storage activated: " + str(val[item]))
    if item == 11:
        place = "client"
        print ("Client path is: " + str(val[item]))
    if item == 12 and depart == 1:
        print ("### Setting progress: 90% ###\n")
        input ("Congratulations! Setting ist complete! Press enter to return.")
        startMain()   
        return

    if item == 5 or item == 7 or item == 10:
        change = input ("Type (0) for deactivate, (1) for activate or press (x) for abort: ")
        if change == "0":
            change = "no"
        elif change == "1":
            change = "yes"
    elif item == 4:
        change = getpass.getpass ("Type in your password or press (x) for abort. Input is hidden: ")
    elif item == 9:
        # ONLY CHECK AND EDIT VALUES, THEN COME BACK
        change = openList ()
    else:
        change = input ("Type in a new value or press (x) for abort: ")
        change = str(change)

    if change == "x" and depart == 1:
        startMain()
        return
    elif change == "x" and depart == 2:
        setCustom(depart)
        return
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

def openList ():
    val = readData()
    calendarlist = val[9].replace('\n', "").split(",")
    listcontent = val[9]
    choice = "x"
    while choice != "":
        items = len(calendarlist)
        itemsDisp = items + 1
        position = 0
        print("")
        if position == items:
            print ("No calendarlists...")
        else:
            while position < items:
                posDisp = position + 1
                valDisp = calendarlist[position]
                print (str(posDisp) + " - " + valDisp)
                position += 1
        choice = input("Type in a new calendar name, type an item number for deleting or press enter to finish. ")
        isInt = True
        try:
            int(choice)
        except ValueError:
            isInt = False
        if isInt and int(choice) < itemsDisp:
            print ("YES")
            choice = int(choice) - 1
            del calendarlist[choice]
            listcontent = ",".join(calendarlist)
            print(listcontent)
        elif isInt and int(choice) >= itemsDisp:
            print ("CALENDAR DOES NOT EXIST.")
        elif choice != "":
            listcontent = listcontent + "," +  choice
            calendarlist = listcontent.replace('\n', "").split(",")
            print (listcontent)
    print ("\nOld version: " + val[9])
    print ("New version: " + listcontent)
    choice = input ("Press (x) to discard changes or press enter to save. ")
    if choice == "x":
        return val[9]
    else:
        return listcontent
    
startMain()
