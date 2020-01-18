#!/usr/bin/python3
'''
Created on Jan 6, 2020

@author: broihier
'''
import getopt
import json
import os
import re
import sys
import time
from datetime import datetime, timedelta

class PythonToJson:
    '''
    Class to convert a python object to JSON
    '''
    def __init__(self, forecastObject, fileName):
        '''
        Constructor
        '''
        self.outputHandle = open(fileName, "w")
        self.forecastObject = forecastObject

    def write(self):
        '''
        Public write method
        '''
        json.dump(self.forecastObject, self.outputHandle)
        self.outputHandle.close()

class CommandInterpreter:
    def __init__(self, commandFileName, category):
        '''
        Constructor
        '''
        self.inputHandle = open(commandFileName, "r")
        self.category = category
        self.testID = ""
        self.title = ""
        self.commandType = ""
        self.parameterText = ""
        self.parameterList = []
        self.results = { "hiLow"    : {},
                         "alertInfo": [],
                         "display" : {} }
        self.allDays = [ "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun" ]
        for day in self.allDays:
            for hour in [ " 00", " 01", " 02", " 03", " 04", " 05", " 06", " 07", " 08", " 09", " 10", " 11",
                          " 12", " 13", " 14", " 15", " 16", " 17", " 18", " 19", " 20", " 21", " 22", " 23" ]:
                self.results['hiLow'][ day + hour + ":00" ] = ""
        self.forecastTemplatePattern = re.compile(r"^forecast template ")
        self.alertsTemplatePattern = re.compile(r"^alerts template ")
        self.incrementTemperaturePattern = re.compile(r"Increment temperature (-*\d+)")
        self.incrementWindPattern = re.compile(r"Increment wind (-*\d+)")
        self.totalPeriodsPattern = re.compile(r"Total periods (\d+)")
        print("Deleting file related to test category:", category)
        if os.path.exists(category + ".testDbExpectedResults"):
            os.remove(category + ".testDbExpectedResults")
        if os.path.exists(category + ".testDbID"):
            os.remove(category + ".testDbID")
        if os.path.exists(category + ".testDbObjective"):
            os.remove(category + ".testDbObjective")
        if os.path.exists(category + ".testDbPost"):
            os.remove(category + ".testDbPost")
        if os.path.exists(category + ".testDbPre"):
            os.remove(category + ".testDbPre")
        if os.path.exists(category + ".testDbProcedures"):
            os.remove(category + ".testDbProcedures")
        if os.path.exists(category + ".testDbResults"):
            os.remove(category + ".testDbResults")
        if os.path.exists(category + "/test.ctl"):
            os.remove(category + "/test.ctl")

    def get(self):
        '''
        Get next command
        '''
        try:
            self.testID = self.inputHandle.readline().strip()
            self.commandType = self.inputHandle.readline().strip()
            if self.commandType == "test" or self.commandType == "setup":
                self.parameterText = ""
                self.parameterList = []
            if self.commandType == "forecast" or self.commandType == "alerts":
                self.parameterText = self.inputHandle.readline().strip()
                self.parameterList = self.parameterText.split("/")
            if self.commandType == "testDbID":
                title = self.inputHandle.readline()
                fileHandle = open(self.category+".testDbID", "a")
                fileHandle.write(self.testID + "\n")
                fileHandle.write(title)
                fileHandle.close()
            if self.commandType == "testDbObjective":
                requirements = self.inputHandle.readline()
                text = self.inputHandle.readline()
                fileHandle = open(self.category+".testDbObjective", "a")
                fileHandle.write(self.testID + ": " + requirements)
                fileHandle.write(text)
                fileHandle.close()
                fileHandle = open(self.category+".testDbPost", "a")
                fileHandle.write(self.testID + "\n")
                fileHandle.write("\n")
                fileHandle.close()
                fileHandle = open(self.category+".testDbPre", "a")
                fileHandle.write(self.testID + "\n")
                fileHandle.write("Read test category description.\n")
                fileHandle.close()
                fileHandle = open(self.category+".testDbProcedures", "a")
                fileHandle.write(self.testID + "\n")
                fileHandle.write("Execute the test driver as described in the test category description.\n")
                fileHandle.close()
                fileHandle = open(self.category+".testDbResults", "a")
                fileHandle.write(self.testID + "\n")
                fileHandle.write("UNTESTED\n")
                fileHandle.close()

        except IOError():
            print('End of file')
            return 0
        return self.commandType

    def getID(self):
        '''
        ID getter
        '''
        return self.testID

    def doForecast(self):
        '''
        Using input control list, create an hourly forecast object, this only defines used entries
        '''
        print("Forecast processing")
        #print("Input Control for test case ID {}".format(self.testID))
        workingObject = {}
        incrementTemperature = 0
        incrementWind = 0
        totalPeriods = 1
        #currentPeriod = 1
        for command in self.parameterList:
            if self.forecastTemplatePattern.match(command):
                workingObject = json.loads(command.replace('forecast template', ''))
            matchObject = self.incrementTemperaturePattern.search(command)
            if matchObject:
                incrementTemperature = int(matchObject.group(1))
                #print("temperature increment", incrementTemperature)
            matchObject = self.incrementWindPattern.search(command)
            if matchObject:
                incrementWind = int(matchObject.group(1))
                #print("wind increment", incrementWind)
            matchObject = self.totalPeriodsPattern.search(command)
            if matchObject:
                totalPeriods = int(matchObject.group(1))
                #print("total periods", totalPeriods)

        emulatorTime = APITimeStringToTime(workingObject['emulatorTime'])
        #print("Emulator time:", timeToAPIString(emulatorTime))
        for currentPeriod in range(2, totalPeriods+1) :
            nextPeriod = { "number" : currentPeriod,
                           "startTime"     : timeToAPIString(APITimeStringToTime(workingObject['properties']['periods'][currentPeriod - 2]['startTime']) + timedelta(hours=1)),
                           "temperature"   : workingObject['properties']['periods'][currentPeriod - 2]['temperature'] + incrementTemperature,
                           "windSpeed"     : workingObject['properties']['periods'][currentPeriod - 2]['windSpeed'] + incrementWind,
                           "windDirection" : workingObject['properties']['periods'][currentPeriod - 2]['windDirection'],
                           "shortForecast" : workingObject['properties']['periods'][currentPeriod - 2]['shortForecast']
                           }
            workingObject['properties']['periods'].append(nextPeriod)
        currentDay = self.allDays[emulatorTime.weekday()]
        high = None
        low = None
        workingOnDay = ""
        dayHiLows = {}
        windSpeed = 0
        direction = ""
        description = ""
        temperature = 0
        sampled = False 
        #print(currentDay)
        #print(emulatorTime)
        for currentPeriod in workingObject['properties']['periods']:
            if not sampled:
                if APITimeStringToTime(currentPeriod['startTime']) >= emulatorTime:
                    sampled = True
                    windSpeed = currentPeriod['windSpeed']
                    direction = currentPeriod['windDirection']
                    temperature = currentPeriod['temperature']
                    description = currentPeriod['shortForecast']
            candidateDay = self.allDays[APITimeStringToTime(currentPeriod['startTime']).weekday()]
            if currentDay == candidateDay:
                #print("Skipping", currentDay)
                continue
            if workingOnDay == "":
                #print("First day to process", candidateDay)
                high = None
                highIndex = 0
                low = None
                lowIndex = 0
                index = 0
                workingOnDay = candidateDay
            else:
                if workingOnDay != candidateDay:
                    if highIndex > lowIndex:
                        dayHiLows[workingOnDay] = str(low) + u'\xc2\xb0' + "/" + str(high) + u'\xc2\xb0'
                    else:
                        dayHiLows[workingOnDay] = str(high) + u'\xc2\xb0' + "/" + str(low) + u'\xc2\xb0'
                    #print("Storing", workingOnDay, dayHiLows[workingOnDay])
                    high = None
                    highIndex = 0
                    low = None
                    lowIndex = 0
                    index = 0
                    workingOnDay = candidateDay

            candidateTemp = currentPeriod['temperature']
            if high == None:
                high = candidateTemp
                low = candidateTemp
            else:
                if high < candidateTemp:
                    high = candidateTemp
                    highIndex = index
                if low > candidateTemp:
                    low = candidateTemp
                    lowIndex = index
            index += 1

        if highIndex > lowIndex:
            dayHiLows[workingOnDay] = str(low) + u'\xc2\xb0' + "/" + str(high) + u'\xc2\xb0'
        else:
            dayHiLows[workingOnDay] = str(high) + u'\xc2\xb0' + "/" + str(low) + u'\xc2\xb0'
            
        #print(dayHiLows)
        for day in self.allDays:
            if day in dayHiLows:
                for hour in [ " 00", " 01", " 02", " 03", " 04", " 05", " 06", " 07", " 08", " 09", " 10", " 11",
                              " 12", " 13", " 14", " 15", " 16", " 17", " 18", " 19", " 20", " 21", " 22", " 23" ]:
                    self.results['hiLow'][ day + hour + ":00" ] = dayHiLows[day]

        self.results['display']['time'] = time.strftime("%a %b %d %Y %H:%M", emulatorTime.timetuple())
        self.results['display']['range'] = self.results['hiLow'][time.strftime("%a %H:00", emulatorTime.timetuple())]
        self.results['display']['wind'] = direction + " @ " + str(windSpeed)
        self.results['display']['description'] = description
        return workingObject

    def doAlerts(self):
        '''
        Using input control list, create an alerts object
        '''
        print("Alert processing")
        #print("Input Control for test case ID {}".format(self.testID))
        workingObject = {}
        for command in self.parameterList:
            if self.alertsTemplatePattern.match(command):
                workingObject = json.loads(command.replace('alerts template', ''))
        #print(workingObject)
        self.results['alertInfo'] = []
        for headline in workingObject['features']:
            self.results['alertInfo'].append(headline['properties']['headline'])
        return workingObject

    def getResults(self):
        '''
        Results getter
        '''
        return self.results

def findAll(string, substring):
    foundAt = []
    index = string.find(substring, 0)
    while index >= 0:
        foundAt.append(index)
        index = string.find(substring, index+1)
    return foundAt
    
def timeToAPIString(timeObject):
    asciiString = str(timeObject)
    spaceLocations = findAll(asciiString, " ")
    modificationLocation = spaceLocations.pop(0)
    return asciiString[0:modificationLocation] + "T" + asciiString[modificationLocation+1:]

def APITimeStringToTime (APITimeString):
    colonLocations = findAll(APITimeString, ":")
    if colonLocations:
        lastColon = colonLocations.pop()
        modifiedTimeString = APITimeString[0:lastColon] + APITimeString[lastColon+1:]
        emulatorTime = datetime.strptime(modifiedTimeString, '%Y-%m-%dT%H:%M:%S%z')
        return emulatorTime
    else:
        return None
    
def main():
    '''
    main program
    '''
    controlFileName = ""
    outputDirectory = ""
    helpString = "python3 api_emulatory.py <control file> <test directory>"
    try:
        opts, args = getopt.getopt(sys.argv[1:], "", [""])
        for opt, arg in opts:
            print(helpString)
            sys.exit(-1)
        for arg in args:
            if controlFileName == "":
                controlFileName = arg
                continue
            if outputDirectory == "":
                outputDirectory = arg
                continue
            else:
                print(helpString)
                sys.exit(-1)
            print("argument={}".format(arg))
        if controlFileName == "":
            print(helpString)
            sys.exit(-1)
    except getopt.GetoptError:
        print(helpString)
        sys.exit(-1)

    if outputDirectory == "":
        print(helpString)
        sys.exit(-1)
        
    ci = CommandInterpreter(controlFileName, outputDirectory)
    command = ci.get()
    while command:
        print("Processing command:", command)
        if command == "forecast":
            hourly = ci.doForecast()
            hourlyFile = PythonToJson(hourly, outputDirectory + "/hourly." + ci.getID())
            hourlyFile.write()
        if command == "alerts":
            alerts = ci.doAlerts()
            alertFile = PythonToJson(alerts, outputDirectory + "/alerts." + ci.getID())
            alertFile.write()
        if command == "setup":
            expectedResultsFile = PythonToJson({}, outputDirectory + "/expectedResults." + ci.getID())
            expectedResultsFile.write()
            fileHandle = open(outputDirectory + "/test.ctl", "a")
            fileHandle.write(ci.getID() + "\n")
            fileHandle.close()
        if command == "test":
            expectedResultsFile = PythonToJson(ci.getResults(), outputDirectory + "/expectedResults." + ci.getID())
            expectedResultsFile.write()
            fileHandle = open(outputDirectory + "/test.ctl", "a")
            fileHandle.write(ci.getID() + "\n")
            fileHandle.close()
        command = ci.get()

if __name__ == '__main__':
    main()
    
