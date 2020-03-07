

import sys
import time
import telepot

from todo import *

#debug = 1

HOMIE=1
STRANGER=0

# separate function used here just for speed.

def CheckBro(first, last):

    if (last == "Blevins" and (first == "Don" or first == "Jacob")): 
        return HOMIE
    else:
        return STRANGER


# *********************************************************

class User:

    def __init__(self, msg):
        self.chat_id = msg['chat']['id']
        self.first_name = msg['from']['first_name']
        self.last_name = msg['from']['last_name']
        self.person_id = msg['from']['id']
        self.todo_filename = self.first_name + "." + "todo.txt"
        self.todo_list = TodoList(self.todo_filename)
        if debug:
            print("\nUser is " + self.first_name)
            print("Filename is " + self.todo_filename + "\n")


# *********************************************************

class UserList:


    def __init__(self):
        self.count = 0
        self.current_users = []

    def Add(self, msg):
        if self.count == 0:
            self.current_users.append(User(msg))
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
                self.current_users.append(User(msg))
                current_user = self.current_users[self.count]
                self.count += 1

        return current_user
                
            

    def Print(self):
        count = 0
        user_string = ""

        if self.count == 0:
            return("No users.\n")
        else:
            while count < self.count:
                user_string += self.current_users[count].first_name + " "
                user_string += self.current_users[count].last_name + "\n"
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
            
        
