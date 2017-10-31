#!/usr/bin/python
from buildHTMLSection import Document
from buildHTMLSection import Requirements
from buildHTMLSection import Objective
from buildHTMLSection import findElementById
import sys
import os

class TraceTable(Document):
    def __init__ (self,template,target,information):
        super(TraceTable,self).__init__(template)
        nodes = self.dom.childNodes

        element = findElementById(nodes,"traceTable")


        for key in sorted(information):
            rowElement = self.dom.createElement("tr")

            cellElement = self.dom.createElement("td")
            cellElement.appendChild(self.dom.createTextNode(key))
            rowElement.appendChild(cellElement)

            cellElement = self.dom.createElement("td")

            informationString = information[key].replace(" ","")
            informationList = informationString.split(",")
            if len(informationList) > 1:
                informationList.pop(0)
            informationString = ", ".join(sorted(informationList))
            cellElement.appendChild(self.dom.createTextNode(informationString))
            rowElement.appendChild(cellElement)

            element.appendChild(rowElement)



        # write table of contents

        targetFile = open(target,"w")
        targetFile.write(self.dom.toxml());
        targetFile.close()


def main():

    bookName = str(sys.argv[1]) 

    bookFile = open(bookName,"r")

    line = bookFile.readline()

    sections = []
    objectives = {}

    requirements = Requirements();
    while line != "":
        line = line.strip()
        sections.append(line)
        objectives[line] = Objective(line,requirements)
        line = bookFile.readline()

    requirementsToTestCase = {}
    for requirement in requirements.requirements:
        requirementsToTestCase[requirement] = "  "

    testCaseToRequirements = {}

    for category in objectives:
        for testID in objectives[category].requirementsInThisTest:
            requirementList = objectives[category].getTestRequirementIDs(testID)
            for requirementID in requirementList:
                if not requirementID in requirementsToTestCase:
                    requirementsToTestCase[requirementID] = testID
                else:
                    requirementsToTestCase[requirementID] = requirementsToTestCase[requirementID] + ", " + testID
                if not testID in testCaseToRequirements:
                    testCaseToRequirements[testID] = requirementID
                else:
                    testCaseToRequirements[testID] = testCaseToRequirements[testID] + ", " + requirementID
 

    TraceTable("tools_configuration/REQ_TEST_ID_TEMPLATE.html","req_test_id.html",requirementsToTestCase)
    TraceTable("tools_configuration/TEST_ID_REQ_TEMPLATE.html","test_id_req.html",testCaseToRequirements)

if __name__ == "__main__":
    main()



