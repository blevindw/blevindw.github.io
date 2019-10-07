
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
TODO_LIST_FILE="todo.txt"

grocerylist = GroceryList(GROCERY_LIST_FILE)
grocerylocationlist = GroceryItemLocationList(ITEM_LOCATION_FILE)
user_list = UserList()
todo_list = TodoList(TODO_LIST_FILE)

def CPUTooHot():
    
    cpu = CPUTemperature()

    if cpu.temperature > 80:
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

        user_list.Add(msg)        # add if a new user joined 

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
           output_string += str(cel) + "C "
           output_string += "or " + str(fahr) + "F"
           bot.sendMessage(chat_id, output_string)
        elif command == 'who':
           output_string = user_list.Print()
           bot.sendMessage(chat_id, output_string)
        elif command == 'todo':
           output_string = todo_list.TodoHandler(bot, msg)
           bot.sendMessage(chat_id, output_string)
        

# ****** Grocery commands begin here

        elif command == 'say' or command == "comment":
           grocerylist.AddComment(item)
           bot.sendMessage(chat_id,"Added your comment:\n" + item + "\n")
        elif command =='store':
           subcommand = part[2].partition(" ")
           if subcommand[0].lower() == "add":
               temp_tuple = subcommand[2].partition(" ")
               location = temp_tuple[0]
               item = temp_tuple[2]
               status = grocerylocationlist.AddItem(location, item)
               if status == ITEM_ADDED:
                   bot.sendMessage(chat_id,"Added "+ item + " to the list.\n")
               elif status == ITEM_DUPLICATE:
                   bot.sendMessage(chat_id,"Already on the list, thanks tho!\n")
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
           bot.sendMessage(chat_id,"Adding " + item)
        elif command == 'reset':
           grocerylist.ClearList()
           bot.sendMessage(chat_id,"List cleared.")

# ******

        else:
           bot.sendMessage(chat_id,"Unknown command.")
    else:
        print("A stranger has called... name is " + first_name + " " + last_name)

       
def SendHelpMessage(chat_id):
   bot.sendMessage(chat_id, "Valid commands are:\n\
       Hi or Hello \n\
       ? or Help \n\
       Say or Comment phrase - adds a comment to the list \n\
       Add item - for adding an item to the list\n\
       List - gives the current list\n\
       Store - gives shopping options\n\
       Store add location item - adds the location info for an item\n\
       Areas or Locations - tells currently used store areas\n\
       Reset - deletes the whole list\n\n\
Case is ignored.\n\n\
Other commands:\n\n\
       Who - lists all current users\n\
       Temp or Hot - give current CPU temp\n")


#******************* MAIN LOOP ********************************


# Get your Bot key from BotFather and put it here.
bot=telepot.Bot('YOUR_BOT_KEY')
bot.message_loop(handle)
print('I am listening...')

count = 0

while 1:
    try:

        time.sleep(10)

        if CPUTooHot():
            cpu = CPUTemperature()
            cel = round(cpu.temperature)
            fahr = round((cpu.temperature * 9 / 5) + 32, 1)
            output_string = "Current temp is too HOT:\n"
            output_string += str(cel) + "C "
            output_string += "or " + str(fahr) + "F" + "\n"
            output_string += "Please check on me.\n"

            user_list.TellAllUsers(bot, output_string)

    
    except KeyboardInterrupt:
        print('\n Program interrupted')
        exit()
    
    except:
        print('Other error or exception occured!')

