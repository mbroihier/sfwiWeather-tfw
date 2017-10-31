#!/usr/bin/python
import os
import sys

class UpdateTestStatus(object):
    def __init__(self):
        logFile = open("TEST.LOG", "r")
        line = logFile.readline()
        firstIDLine = True
        testIDToStatus = {}
        processing = "ID"
        while line != "":
            idLine = line.split("ID:")
            if len(idLine) > 1:
                if not firstIDLine:
                    if processing == "ID":
                        id = idLine[1].strip(" ").strip("\n") # get ID
                        processing = "Results"
                    else:
                        print("Error - was expecting to process Results field")
                        sys.exit(-1)
                firstIDLine = False
            statusLine = line.split("Results: ")
            if len(statusLine) > 1:
                if processing == "Results":
                    testIDToStatus[id] = statusLine[1].strip("\n").strip(" ")
                    processing = "ID"
                else:
                    print("Error - was expecting to process ID field")
                    sys.exit(-1)
            line = logFile.readline()
        logFile.close()
        files = os.listdir("./")
        filesToUpdate = {}
        for file in files:
            if ".testDbResults" in file:
                databaseFile = open(file, "r")
                line = databaseFile.readline()
                while line != "":
                    id = line.strip("\n").strip(" ")
                    status = databaseFile.readline().strip("\n").strip(" ")
                    if id in testIDToStatus:
                        if testIDToStatus[id] != status:
                            filesToUpdate[file] = True
                        else:
                            del testIDToStatus[id]
                    line = databaseFile.readline()
                databaseFile.close()
        for file in filesToUpdate:
            databaseFile = open(file, "r")
            newDatabaseFile = open(file + "_", "w")
            line = databaseFile.readline()
            while line != "":
                line = line.strip("\n").strip(" ")
                id = line
                newDatabaseFile.write(line + "\n")
                line = databaseFile.readline().strip("\n").strip(" ")
                if (id in testIDToStatus):
                    line = testIDToStatus[id]
                    del testIDToStatus[id]
                newDatabaseFile.write(line + "\n")
                line = databaseFile.readline()
            databaseFile.close()
            newDatabaseFile.close()
            os.rename(file + "_", file)
        if len(testIDToStatus) > 0:
            for key in testIDToStatus:
                print("Found extra test case ID: " + key)

def main():
    updateTestStatus = UpdateTestStatus()

if __name__ == "__main__":
    main()
