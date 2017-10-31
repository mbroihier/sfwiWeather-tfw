#!/usr/bin/python
import sys
import os

class DatabaseSet(object):
    def __init__ (self, category):
        suffixList = [ ".testDbCategoryDescription", 
                       ".testDbCategoryTitle",
                       ".testDbExpectedResults",
                       ".testDbID",
                       ".testDbObjective",
                       ".testDbPost",
                       ".testDbPre",
                       ".testDbProcedures",
                       ".testDbResults" ]

        for suffix in suffixList:
            dbFile = open(category + suffix, "w")
            #dbFile.write(category + "-0010\n\n");
            dbFile.close()


def main():

    if len(sys.argv) != 3:
        print("stpsInitializae <book name> <\"title of project\">")
        sys.exit(-1)

    acronym = ""
    for file in os.listdir("./"):
        if file.find("REQ.") == 0:
            acronym = file[4:]

    if acronym == "":
        sys.exit(-2)

    bookName = str(sys.argv[1])

    projectTitle = str(sys.argv[2])

    projectFile = open("PROJECT.testDb", "w")
    projectFile.write(projectTitle + "(" + acronym + ")")
    projectFile.close()

    bookFile = open(bookName,"r")

    line = bookFile.readline()

    while line != "":
        line = line.strip()
        DatabaseSet(line); # make a set of databases associated with the category name
        line = bookFile.readline()

    
if __name__ == "__main__":
    main()



