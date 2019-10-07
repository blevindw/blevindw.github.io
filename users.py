

import sys
import time
import telepot

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


# *********************************************************

class UserList:


    def __init__(self):
        self.count = 0
        self.current_users = []

    def Add(self, msg):
        if self.count == 0:
            self.current_users.append(User(msg))
            self.count += 1
        else:
            count = 0
            found = False
            while count < self.count and not found:
                if self.current_users[count].person_id == msg['from']['id']:
                    found = True
                else:
                    count += 1
            if not found:
                self.current_users.append(User(msg))
                self.count += 1
            

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
        print("Got string:\n" + string)

        if self.count == 0:
            print("TellAllUsers called with no one connected.")
        else:
            print("User count is " + str(self.count))
            while count < self.count:
                print("Made it.")
                print("Sending to: " + self.current_users[count].first_name)
                chat_id = self.current_users[count].chat_id
                bot.sendMessage(chat_id, string)
                count += 1
            
        
