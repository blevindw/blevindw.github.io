
import sys
import time
import telepot

from gpiozero import CPUTemperature

from util import *
from grocerylist import *
from users import *
from todo import *

#debug=0

GROCERY_LIST_FILE="grocerylist.txt"
ITEM_LOCATION_FILE="itemlocationlist.txt"

grocerylist = GroceryList(GROCERY_LIST_FILE)
grocerylocationlist = GroceryItemLocationList(ITEM_LOCATION_FILE)
user_list = UserList()

grocery_list_updated=False
grocery_list_version=1

def CPUTooHot():
    
    cpu = CPUTemperature()

    if cpu.temperature > 75:
        return True
    else:
        return False

def handle(msg):
    chat_id = msg['chat']['id']
    message = msg['text']
    first_name = msg['from']['first_name']
    last_name = msg['from']['last_name']
    person_id = msg['from']['id']

    person = CheckBro(first_name, last_name)  # see users.py

    if person == HOMIE:

        current_user = user_list.Add(msg)        # add if a new user joined 
        todo_list = current_user.todo_list

        if debug: print(msg)
        part = message.partition(" ")
        if debug: print(part)

        command = part[0].lower()
        item = part[2].lower()
        if debug: print('Got command: %s' % command)
        if debug: print('Got item: %s' % item)

# ****** General commands begin here

        if command == "?" or command == "help":
           SendHelpMessage(chat_id)
        elif command == 'hello' or command == 'hi':
           greeting = "Hello, " + first_name
           bot.sendMessage(chat_id,greeting) 
        elif command == 'temp' or command == 'hot':
           cpu = CPUTemperature()
           cel = round(cpu.temperature)
           fahr = round((cpu.temperature * 9 / 5) + 32, 1)
           output_string = "Current temp is a balmy "
           output_string += str(cel) + u'\u00b0' + "C "
           output_string += "or " + str(fahr) + u'\u00b0' + "F"
           bot.sendMessage(chat_id, output_string)
        elif command == 'who':
           output_string = user_list.Print()
           bot.sendMessage(chat_id, output_string)
        elif command == 'push':
           user_list.TellAllUsers(bot, item)
        elif command == 'todo':
           output_string = todo_list.TodoHandler(bot, msg)
           bot.sendMessage(chat_id, output_string)
        

# ****** Grocery commands begin here

        elif command == 'say' or command == "comment":
           grocerylist.AddComment(item)
           user_list.TellAllUsers(bot, "Comment added.")
        elif command =='store':
           subcommand = part[2].partition(" ")
           if subcommand[0].lower() == "add":
               temp_tuple = subcommand[2].partition(" ")
               location = temp_tuple[0]
               item = temp_tuple[2]
               bot.sendMessage(chat_id, grocerylocationlist.AddItem(location, item))
           else:
               bot.sendMessage(chat_id,"Store has the following: \n")
               bot.sendMessage(chat_id,grocerylocationlist.PrintStoreList())
        elif command == 'list':
           bot.sendMessage(chat_id,grocerylist.PrintList(grocerylocationlist))
        elif command == 'areas' or command == 'locations':
           bot.sendMessage(chat_id,"The current areas in use are: \n")
           bot.sendMessage(chat_id,grocerylocationlist.PrintLocationList())
        elif command == 'add':
           grocerylist.AddItem(item)
           user_list.TellAllUsers(bot, "Adding " + item)
        elif command == 'reset':
           grocerylist.ClearList()
           user_list.TellAllUsers(bot, "List cleared.")

# ******

        else:
           bot.sendMessage(chat_id,"Unknown command.")
    else:
        print("A stranger has called... name is " + first_name + " " + last_name)

       
def SendHelpMessage(chat_id):
   output_string = "Valid commands are:\n\
       ? or Help \n\n\
Grocery List Commands:\n\n\
       Say or Comment phrase - adds a comment to the list \n\
       Add item - for adding an item to the list\n\
       List - gives the current list\n\
       Store - gives shopping options\n\
       Store add location item - adds the location info for an item\n\
       Areas or Locations - tells currently used store areas\n\
       Reset - deletes the whole list\n\n\
Other commands:\n\n"
   output_string += '       Todo- manages a family todo list\n'\
       + "              Use Todo ? for a list of options\n"\
       + "       Hi or Hello \n"\
       + "       Who - lists all current users\n"\
       + "       Temp or Hot - give current CPU temp\n\n"

   output_string += "Case is ignored.\n"

   bot.sendMessage(chat_id, output_string)


#******************* MAIN LOOP ********************************


# Get your Bot key from BotFather and put it here.
bot=telepot.Bot('YOUR_BOT_KEY_HERE')
bot.message_loop(handle)
print('I am ' + '\033[1m' + 'listening...' + '\033[0m')

while 1:
    try:
       
        time.sleep(10)
    
    except KeyboardInterrupt:
        print('\n Program interrupted')
        exit()
    
    except:
        print('Other error or exception occured!')

