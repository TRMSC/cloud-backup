#!/usr/bin/env python3

# Cloud Backup - Copyright (C) 2022, TRMSC - https://trmsc1.wordpress.com/ 
# GNU General Public Licence 3.0 - http://www.gnu.de/documents/gpl-3.0.en.html 

import configparser
import numbers
import os
import datetime
import getpass
from pickle import TRUE

version = "v.1.2.1"

def initConfig():
    val = readData()
    encr = encryptPwd(val)
    print ("\n- - - - - - - - - - - - - - - - -")
    print ("Last modified: " + val[0] + "\n")
    print (" 1 - GENERAL - Change backup directory (" + val[1] + ")")
    print (" 2 - GENERAL - Number of stored backups (" + val[2] + ")")
    print (" 3 - ACCESS - Set username (" + val[3] + ")")
    print (" 4 - ACCESS - Set password (" + encr + ")")
    print (" 5 - ADRESSBOOK - Activate adressbook backup (" + val[5] + ")")
    print (" 6 - ADRESSBOOK - Adressbook url (" + val[6] + ")")
    print (" 7 - CALENDAR - Activate calendar backup (" + val[7] + ")")
    print (" 8 - CALENDAR - Calendar url (" + val[8] + ")")
    print (" 9 - CALENDAR - Calendar list (" + val[9] + ")")
    print ("10 - DATA - Activate data backup from desktop client (" + val[10] + ")")
    print ("11 - DATA - Client path (" + val[11] + ")")
    print ("")
    check = 0
    while check == 0:
        item = input ("Press enter to start auto settings, type (x) to exit or type in the number you want to change. ")
        if item == "x":
            exit()
        elif item == "":
            startProgress(1, 1)
            check = 1
        else:
            item = int(item)
            if item > 0 and item <= 11:
                startProgress(2, item)
                check = 1
            else:
                check = 0
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

def encryptPwd(val):
    encr = ""
    x = 0
    while x < len(val[4]):
        encr += "*"
        x += 1
    return encr

def startProgress(depart, item):
    val = readData()
    check = 0
    print ("")
    # Print items and values
    if depart == 1 and item < 12:
        percent = (item - 1) * 9
        print ("- - - - - - - - - - - - - - -")
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
        print ("- - - - - - - - - - - - - - -")
        print ("### Setting progress: 100% ###\n")
        input ("Congratulations! Setting ist complete! Press enter to return.")
        initConfig()   
        return
    # Input actions
    if item == 5 or item == 7 or item == 10:
        while check == 0:
            change = input ("Type (0) for deactivate, (1) for activate or press enter to skip: ")
            if change == "0":
                change = "no"
                check = 1
            elif change == "1":
                change = "yes"
                check = 1
            elif change == "":
                check = 1
    elif item == 4:
        change = getpass.getpass ("Type in your password or press enter to skip. Input is hidden: ")
    elif item == 9:
        change = openCallist ()
    else:
        if depart == 1:
            change = input ("Type in a new value, type (x) to abort or press enter to skip: ")
        elif depart == 2:
            change = input ("Type in a new value or press enter to abort: ")
        change = str(change)
    if change == "" and depart == 1:
        item = int(item) + 1
        startProgress(1, item)
        return
    elif change == "x" and depart == 1:
        initConfig()
        return        
    elif change == "" and depart == 2 and item != 9:
        initConfig()
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
            initConfig()
    return

def openCallist ():
    val = readData()
    calendarlist = val[9].replace('\n', "").split(",")
    listcontent = val[9]
    choice = "x"
    empty = 0
    while choice != "":
        items = len(calendarlist)
        itemsDisp = items + 1
        position = 0
        print("")
        if position == items:
            print ("No calendarlists...")
            empty = 1
        else:
            while position < items:
                posDisp = position + 1
                valDisp = calendarlist[position]
                print (str(posDisp) + " - " + valDisp)
                position += 1
        choice = input("Type in a new calendar name, type an item number for deleting or press enter to skip/ finish. ")
        isInt = True
        try:
            int(choice)
        except ValueError:
            isInt = False
        if isInt and int(choice) < itemsDisp:
            choice = int(choice) - 1
            del calendarlist[choice]
            listcontent = ",".join(calendarlist)
            print(listcontent)
        elif isInt and int(choice) >= itemsDisp:
            print ("CALENDAR DOES NOT EXIST.")
        elif choice != "":
            if empty == 1:
                listcontent = choice
                empty = 0
            else:
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
    
config = configparser.ConfigParser()
print ("\nWelcome to cloud-backup configuration " + version)
print ("Feel free to visit trmsc1.wordpress.com")
initConfig()
