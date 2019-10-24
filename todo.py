

from util import *

ITEM_ADDED=1
ITEM_DUPLICATE=2

#debug = 1


def handle(msg):
    chat_id = msg['chat']['id']
    message = msg['text']
    first_name = msg['from']['first_name']
    last_name = msg['from']['last_name']
    person_id = msg['from']['id']

class TodoList:

    def __init__(self, file):

        self.file = file
        self.num_lines = 0
        self.num_tasks = 0
        self.num_comments = 0

        self.comments = []
        self.tasks = []

        self.LoadFile()
        if debug:  print("TodoList:\n" + \
              "  Loaded " + str(self.num_tasks) + " tasks\n" + \
              "  Loaded " + str(self.num_comments) + " comments\n")
    
    def AddComment(self, comment):

        self.comments.append(comment.rstrip("\n"))
        self.num_comments += 1

        with open(self.file,"a") as infile:
            infile.write("C " + comment + "\n")
        return("Todo:  comment added.\n")

    def RemoveItem(self, item):

        if self.num_comments != 0 or self.num_tasks != 0:
            count = 0
            found_task = False
            found_comment = False
            print(self.tasks)
            while count < self.num_tasks and not found_task:
                print("Checking " + self.tasks[count])
                if self.tasks[count] == item:
                    print("Found " + item)
                    self.tasks.remove(item)
                    print(self.tasks)
                    self.num_tasks -= 1
                    found_task = True
                count += 1

            count = 0
            while count < self.num_comments and not found_comment and not found_task:
                if self.comments[count] == item:
                    self.comments.remove(item)
                    self.num_comments -= 1
                    found_comment = True
                count += 1

            if found_task or found_comment:
                self.FileList()
                return("Item removed.\n")
            else:
                return("Item not found.\n")
        else:
            return("Todo list is empty.\n")


    def AddTask(self, task):
        self.tasks.append(task.rstrip("\n"))
        self.num_tasks += 1

        with open(self.file,"a") as infile:
            infile.write(str(self.num_tasks - 1) + " " + task + "\n")
        return("Todo:  task added.\n")

    def Print(self):

        if debug: print("Entering Todo.Print")
        output_string = ""
        tasks_string = ""
        comments_string = ""
        istasks = False
        iscomments = False

        if self.num_tasks > 0 or self.num_comments > 0:
            if self.num_tasks > 0:
                count = 0
                istasks = True
                while count < self.num_tasks:
                    tasks_string += "  " + str(count + 1) + " " + str(self.tasks[count] + "\n")
                    count += 1
            if self.num_comments > 0:
                count = 0
                iscomments = True
                while count < self.num_comments:
                    comments_string += "  " + str(self.comments[count] + "\n")
                    count += 1
        else:
            return("File is empty- no tasks or comments.\n")

        if istasks:
           output_string += "Tasks:\n"
           output_string += tasks_string
        if iscomments:
           output_string += "Comments:\n"
           output_string += comments_string
         
        return(output_string)
        
    def ResetList(self):

        recreate_file = open(self.file, "w")
        recreate_file.close()

    def FileList(self):

        recreate_file = open(self.file, "w")
        recreate_file.truncate(0)
        recreate_file.close()

        temp_string = ""
        if self.num_tasks > 0:
            with open(self.file,"a") as infile:
                count = 0
                while count < self.num_tasks:
                        temp_string = str(count + 1) + " " + self.tasks[count] + "\n"
                        infile.write(temp_string)
                        count += 1
            infile.close()

        temp_string = ""
        if self.num_comments > 0:
            with open(self.file,"a") as infile:
                count = 0
                while count < self.num_comments:
                        temp_string = str(count + 1) + " " + str(self.comments[count] + "\n")
                        infile.write(temp_string)
                        count += 1
            infile.close()

    def LoadFile(self):
        self.num_lines = countLinesInFile(self.file)

        with open(self.file,"r") as infile:

            count = 0           
            line = infile.readline()

            while line != '':   # blank is end of file

                tuple = line.partition(" ")
                if unicode(tuple[0]).isnumeric():  # nice method only available for unicode :(
                    type = "Number"
                else:
                    type = tuple[0]
                content = tuple[2]

                if type == "Number":
                    self.tasks.append(content.rstrip("\n"))
                    self.num_tasks += 1
                elif type == "C":
                    self.comments.append(content.rstrip("\n"))
                    self.num_comments += 1
                else:
                    print("Todo line " + str(count+1) + " ignored: " + str(line))

                count += 1
                line = infile.readline()
        
    def commandReference(self):
        output_string = ""

        output_string = "Todo commands are:\n\n" + \
           "   No command, prints current list\n" + \
           "   ? or help- gives command options\n" + \
           "   print - prints list\n" + \
           "   say or comment blah- adds a comment\n" + \
           "   add or a blah- adds a task\n" + \
           "   del or d blah- deletes a task or comment\n" 
        return(output_string)

    def TodoHandler(self, bot, msg):

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
            return self.Print()
        elif subcommand == 'say' or subcommand == "comment":
            return self.AddComment(item)
        elif subcommand == 'a' or subcommand == "add":
            return self.AddTask(item)
        elif subcommand == 'd' or subcommand == "del" or subcommand == "rm":
            return self.RemoveItem(item)
        else:
            return("Todo:  Unknown subcommand.\n")    

