

import sys
import time
import telepot
import csv

from todo import *
from grocerylist import *

debug = 1

HOMIE=1
STRANGER=0

# separate function used here just for speed.

def CheckBro(first, last, file):

    found = False
    with open(file,"r") as infile:
        reader = csv.reader(infile)
        for line in reader:
            temp_tuple = line[0].partition(" ")
            if (first == temp_tuple[0] and last == temp_tuple[2]):
                found = True

    if found:
        return HOMIE
    else:
        return STRANGER







# *********************************************************

class User:

    def __init__(self, msg, file):
        self.file = file
        self.chat_id = msg['chat']['id']
        self.first_name = msg['from']['first_name']
        self.last_name = msg['from']['last_name']
        self.person_id = msg['from']['id']
        self.todo_filename = self.first_name + "." + "todo.txt"
        self.todo_list = TodoList(self.todo_filename)

        with open(self.file,"r") as infile:
            reader = csv.reader(infile)
            count = 0
            for line in reader:
                found = False
                temp_tuple = line[0].partition(" ")
                if (self.first_name == temp_tuple[0] and self.last_name == temp_tuple[2]):
                    found = True
                    self.default_house_address = line[1]
                    count += 1

        self.house_address = self.default_house_address

        if debug:
            print("\nUser is " + self.first_name + " " + self.last_name)
            print(str(self.chat_id) + ", " + str(self.house_address))
           
    def PrintSelf(self):
        print(self.first_name + " " + self.last_name)
        print(str(self.chat_id) + ", " + self.house_address)
        print(self.todo_filename)






# *********************************************************

class UserList:


    def __init__(self):
        self.count = 0
        self.current_users = []

    def Add(self, msg, file):
        if self.count == 0:
            self.current_users.append(User(msg,file))
            self.count += 1
            current_user = self.current_users[0]
        else:
            count = 0
            found = False
            while count < self.count and not found:
                if self.current_users[count].person_id == msg['from']['id']:
                    found = True
                else:
                    count += 1
            if found:
                current_user = self.current_users[count]
            else:
                self.current_users.append(User(msg,file))
                current_user = self.current_users[self.count]
                self.count += 1

        return current_user
                
            

    def Print(self):
        count = 0
        user_string = "User Name, House Address\n"

        if self.count == 0:
            return("No users.\n")
        else:
            while count < self.count:
                user_string += self.current_users[count].first_name + " "
                user_string += self.current_users[count].last_name + ", "
                user_string += str(self.current_users[count].house_address) + "\n"

                count += 1
            
            output_string = "Current users are:\n"
            output_string += user_string
            return(output_string)

    def TellAllUsers(self, bot, string):
        count = 0
        user_string = ""

        if self.count == 0:
            print("TellAllUsers called with no one connected.")
        else:
            while count < self.count:
                chat_id = self.current_users[count].chat_id
                bot.sendMessage(chat_id, string)
                count += 1

    def TellAllRoommates(self, bot, string, housenum):
        count = 0
        user_string = ""

        if self.count == 0:
            print("TellAllRoommates called with no one connected.")
        else:
            while count < self.count:
                if self.current_users[count].house_address == housenum:
                    chat_id = self.current_users[count].chat_id
                    bot.sendMessage(chat_id, string)
                count += 1
            
        
        
class House:

    def __init__(self,info):
        self.name = info[1]
        self.address = info[0]

        self.grocerylistfile = "house" + str(self.address) + "." + "grocerylist.txt"
        self.grocerylist = GroceryList(self.grocerylistfile)



class HouseList:
    def __init__(self,file):
        self.file = file
        self.num_houses = 0
        self.current_houses = []


        with open(self.file,"r") as infile:
            reader = csv.reader(infile)
            count = 0
            for line in reader:
                self.current_houses.append(House(line))
                self.current_houses[count].address = count + 1
                count += 1

            self.num_houses = count


    def PrintList(self):

        output_string = "House Name, Number\n"
        for house in range(self.num_houses):
            output_string += self.current_houses[house].name + ", " + str(self.current_houses[house].address) + "\n"

        return output_string

    def isHouseAddress(self, item):
        
        found = False

        for i in range(self.num_houses):
            if item == str(self.current_houses[i].address):
                found = True
        return found
        

    def MsgHandler(self, bot, msg, current_user):

        chat_id = msg['chat']['id']
        message = msg['text']

        part = message.partition(" ")

        command = part[0].lower()
        tuple = part[2].partition(" ")
        subcommand = tuple[0].lower()
        item = tuple[2]

        if subcommand == "?" or subcommand == "help":
            output_string = self.commandReference()
            return(output_string) 
        elif subcommand == "" or subcommand == 'print' or subcommand == 'p':
            output_string = current_user.first_name + " currently using House " + str(current_user.house_address) + "\n"
            output_string += self.PrintList()
            return(output_string) 
        elif self.isHouseAddress(subcommand):
            current_user.house_address = subcommand
            output_string = current_user.first_name + " now using house: "
            for i in range(self.num_houses):
                if subcommand == str(self.current_houses[i].address):
                    output_string += self.current_houses[i].name
            return(output_string)
        else:
            return("House:  Unknown subcommand.\n")    


    def commandReference(self):

        output_string = "House commands are:\n\n" + \
           "   No command, prints current list\n" + \
           "   ? or help- gives command options\n" + \
           "   print - prints list\n" + \
           "   #- sets your default house to the number\n"
        return(output_string)


