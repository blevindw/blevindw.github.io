
debug = 0

def make2dlist(rows, cols):
    a=[]
    for row in range(rows): a += [[0]*cols]
    return a

def countLinesInFile(file):

    with open(file,"r") as infile:
        line = infile.readline()
        count = 0
        while line != '':   # blank is end of file
            count += 1
            line = infile.readline()
        return(count)
