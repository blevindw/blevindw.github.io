
from util import *

#debug=1


class GroceryList:

    def __init__(self, file):

        self.file = file

    
    def AddComment(self,comment):

        with open(self.file,"a") as infile:
            infile.write("Comment " + comment + "\n")

    def AddItem(self,item):

        with open(self.file,"a") as infile:
            infile.write(item + "\n")

    def DeleteItem(self, item):

        with open(self.file,"r") as infile:
            test = infile.read()
    
        if test == "":

           return("Grocery list is currently empty\n")

        else:

            with open(self.file,"r") as infile:
                line = infile.readline()
                temp_list = []
                count = 0           
                while line != '':   # blank is end of file
                    temp_item = line.rstrip("\n")

                    # Skip over item if it matches
                    found = 0
                    if temp_item != item:
                        temp_list.append(line.rstrip("\n"))
                    else:
                        found = 1

                    count += 1
                    line = infile.readline()

            item_count = count

            if found:
                self.ClearList()
                self.WriteList(temp_list,item_count)
                output_string = item + " deleted."
                return(output_string)
            else:
                return("Item not found.")


    def PrintList(self, locationlist):

        with open(self.file,"r") as infile:
            test = infile.read()
    
        if test == "":

           return("Grocery list is currently empty\n")

        else:


            with open(self.file,"r") as infile:
                line = infile.readline()
                temp_list = []
                count = 0           
                while line != '':   # blank is end of file
                    temp_list.append(line.rstrip("\n"))
                    count += 1
                    line = infile.readline()

            item_count = count

            output_string = "Current Grocery List:\n\n"

           
            for location in locationlist.locations:

                found = 0
                temp_string = ""

                for i in range(item_count):
                    if locationlist.IsItemInLocation(location, temp_list[i].capitalize()):
                        found = 1
                        temp_string += "   " + temp_list[i] + "\n"
                if found:
                    output_string += location + "\n" + temp_string + "\n"
                    found = 0
                        
            # Check for items that have no location data and print them too
            found = 0
            temp_string = ""
            comments = ""

            for i in range(item_count):
                part = temp_list[i].partition(" ")
                if part[0] == "Comment":
                    comments += "* " + part[2] +"\n"
                else:
                    item_loc = locationlist.FindItem(temp_list[i].capitalize())
                    if item_loc == "":
                        found = 1
                        temp_string += "   " + temp_list[i] + "\n"
            if found:
                output_string += "No Category" + "\n" + temp_string + "\n"
                found = 0
            
            if comments: output_string += "COMMENTS:\n" + comments
        
            return(output_string)
                
        
    def ClearList(self):

        recreate_file = open(self.file, "w")
        recreate_file.close()

    def WriteList(self, list, item_count):

        with open(self.file,"a") as infile:
            for i in range(item_count - 1):
                infile.write(list[i] + "\n")


class GroceryItemLocationList:

    def __init__(self, file):

        self.file = file
        self.locations = []
        self.location_count = 0
        self.line_count = 0

        self.CreateList()

    def AddItem(self,location_in,item_in):

        exact_match = 0
        location_found = 0
        location = location_in.capitalize()
        item = item_in.capitalize()
        
        for row in range(self.line_count):
            if  self.currentlist[row][0] == location:
                location_found = 1
            if  self.currentlist[row][0] == location and self.currentlist[row][1] == item:
                exact_match = 1

        if exact_match:
            output_string = "Item already on the list."
            return(output_string)
        else:
            self.line_count += 1
            self.currentlist.append([location,item])
            self.currentlist.sort(key=lambda x:x[1])
            self.currentlist.sort(key=lambda x:x[0])
            self.SaveList()

            output_string = "Adding " + item + " to " + location + "\n"
            if location_found == 0:
                output_string += "Location " + location + " is new and also added" + "\n"
                self.location_count += 1

            return(output_string)

    def IsItemInLocation(self, location, item):
        
        found = 0
        string = ""
        for row in range(self.line_count):
            if self.currentlist[row][0] == location and self.currentlist[row][1] == item:
                found = 1

        return found
        

    def FindItem(self, item):
        
        location = ""
        
        temp_items = [i[1] for i in self.currentlist] 

        if item in temp_items:
            spot = temp_items.index(item)  
            location = self.currentlist[spot][0]
        else:
            location = ""
        
        return(location)

    def CreateList(self):

        self.line_count = countLinesInFile(self.file)

        self.currentlist = make2dlist(self.line_count,2)

        with open(self.file,"r") as infile:
            line = infile.readline()

            count = 0           
            while line != '':   # blank is end of file
                tuple = line.partition(" ")
                self.currentlist[count][0] = tuple[0]
                self.currentlist[count][1] = tuple[2].rstrip("\n")
                count += 1
                line = infile.readline()
        
        self.currentlist.sort(key=lambda x:x[1])
        self.currentlist.sort(key=lambda x:x[0])

        if debug: self.PrintItemList()
        self.LoadLocations()

    def LoadLocations(self):
        count = 0
        if debug: print("Entering LoadLocations")
        self.location_count = 0
        self.locations = []
        while count < self.line_count:
            if self.location_count > 0:
                if self.currentlist[count][0] in self.locations:
                    count += 1
                else:
                    self.locations.append(self.currentlist[count][0])
                    self.location_count += 1
                    count += 1
            else:
                self.locations.append(self.currentlist[0][0])
                self.location_count = 1
                count += 1

        self.locations.sort()

        if debug: print(self.location_count)
        if debug: self.PrintLocations()

    def PrintStoreList(self):
        string = ""
        for row in range(self.line_count):
            string += self.currentlist[row][0] + " " + self.currentlist[row][1] + "\n"
        return(string)

    def PrintLocationList(self):
        string = '\n'.join([str(loc) for loc in self.locations])
        return(string)

    def PrintStoreLocationList(self, location_in):

        if location_in:
            location = location_in.capitalize()
        else:
            location = "store"
        
        if location in self.locations:
            string = location + " has the following items available:\n"
            for row in range(self.line_count):
                if self.currentlist[row][0] == location:
                    string += self.currentlist[row][1] + "\n"
        elif location == "store":
            string = self.PrintStoreList()
        else:
            string = "Location not found. Use command Store Areas to see current locations.\n"

        return(string)

    def SaveList(self):

        recreate_file = open(self.file, "w")
        recreate_file.close()
        
        with open(self.file,"a") as infile:
            count = 0
            while count < self.line_count:
                infile.write(self.currentlist[count][0] + " " + self.currentlist[count][1] + "\n")
                count += 1

        
# These are used for debugging.

    def PrintItemList(self):
        count = 0
        print("*** Currently loaded item list has " + str(self.line_count) + " items:\n")
        while count < self.line_count:
            print(self.currentlist[count][0] + " " + self.currentlist[count][1])
            count += 1

    def PrintLocations(self):
        count = 0
        print("*** Currently loaded location list has " + str(self.location_count) + " locations:\n")
        while count < self.location_count:
            print(self.locations[count])
            count += 1

