#!/usr/bin/python
from xml.dom.minidom import parse
from xml.dom.minidom import Document
import sys
import os

# utility to print the nodes of a document
def printNodes(head):
    for node in head:
        print node
        if node.hasChildNodes():
            children = node.childNodes
            printNodes(children)

# utility to find an element by its id attribute
def findElementById(head,iD):
    for node in head:
        if node.nodeType != node.TEXT_NODE and node.hasAttribute("id"):
            if node.getAttribute("id") == iD:
                return node
        if node.hasChildNodes():
            children = node.childNodes
            returnNode = findElementById(children,iD)
            if returnNode != None :
                return returnNode

# This class handles the requirements that are tested in the test category (section) that is being built
class Requirements:
    # constructor if a requirement list is given
    def __init__ (self, requirementsInThisTest = None):

        self.requirements = {}
    
        if (requirementsInThisTest == None): # if no argument
            return
        
        for r in requirementsInThisTest:
            if not r in self.requirements:
                self.updateRequirements(r)

    
    # add a requirement to the database
    def addRequirement(self,r):
        import codecs
        # note, since the file will be open, all of the requirements in the file will be added in
        # case they are needed in the future (likely)
        requirementPath = "REQ." + r.split("-")[0]
        try:
            requirementFile = codecs.open(requirementPath, "r", encoding="utf-8")
            requirementID = requirementFile.readline().strip().encode('ascii', 'xmlcharrefreplace').replace("&#8220;","\"").replace("&#8221;","\"")
            while requirementID != "":
                requirementText = requirementFile.readline().strip()
                #print(type(requirementText))
                self.requirements[requirementID] = requirementText.encode('ascii', 'xmlcharrefreplace').replace("&#8220;","\"").replace("&#8221;","\"")
                #print(type(self.requirements[requirementID]))
                requirementID = requirementFile.readline().strip().encode('ascii', 'xmlcharrefreplace').replace("&#8220;","\"").replace("&#8221;","\"")
            requirementFile.close()
        except IOError:
            print("Requirement file error - non fatal")

    # add a list of requirements to the database
    def updateRequirements(self,requirementList):
        if isinstance(requirementList, basestring):
            return
        for r in requirementList:
            if not r in self.requirements:
                self.addRequirement(r)

    # get the text associated with a requirement ID
    def getRequirementText(self,requirementID):
        if not requirementID in self.requirements:
            self.updateRequirements(requirementID)
        if requirementID in self.requirements:
            return self.requirements[requirementID]
        else:
            return "requirement ID missing from requirements"

class Document(object):
    def __init__ (self,template):
        self.dom = parse(template)

# Class to handle the creation of the test identification sections        
class Identification (Document):
    def __init__ (self,category):
        super(Identification,self).__init__("tools_configuration/TEST_CASE_TEMPLATE.html")
        testIdentification = category + ".testDbID"
        testIdentificationFile = open(testIdentification,"r")
        line = testIdentificationFile.readline()
        self.identificationIDs = []
        self.identificationText = {}
        while line != "":
            testID = line.strip().replace(" ","")
            self.identificationIDs.append(testID)
            self.identificationText[testID] = testIdentificationFile.readline().strip()
            line = testIdentificationFile.readline()
        testIdentificationFile.close()

    # adds identification information into the test case DOM
    def insertIntoNodeList (self,nodes,testID):
        element = findElementById(nodes,"testCaseId");
        element.appendChild(self.dom.createTextNode(testID))

        element = findElementById(nodes,"title");
        element.appendChild(self.dom.createTextNode(self.identificationText[testID]))

    def getIDList (self):
        return self.identificationIDs

# Class to handle the creation of the test case objection        
class Objective (Document):
    def __init__ (self,category,requirements):
        super(Objective,self).__init__("tools_configuration/TEST_CASE_TEMPLATE.html")
        testApproach = category + ".testDbObjective"
        testApproachFile = open(testApproach,"r")
        line = testApproachFile.readline()
        self.requirementsInThisTest = {}
        self.objectiveText = {}
        while line != "":
            testID = line.strip().split(":")[0].replace(" ","")
            self.requirementsInThisTest[testID] = line.strip().split(":")[1].replace(" ","").split(",")
            self.objectiveText[testID] = testApproachFile.readline().strip()
            requirements.updateRequirements(self.requirementsInThisTest[testID])
            line = testApproachFile.readline()
        testApproachFile.close()

    # adds objective information into the test case DOM
    def insertIntoNodeList (self,nodes,testID,requirements):
        # add text form of the requirements
        element = findElementById(nodes,"requirementsList")
        for r in self.requirementsInThisTest[testID]:
            listItemTag = self.dom.createElement("li")
            textNode = self.dom.createTextNode(requirements.getRequirementText(r))
            listItemTag.appendChild(textNode)
            element.appendChild(listItemTag)

        # insert objective statement into the objectives paragraph of the table
        paragraphTag = self.dom.createElement("p")
        paragraphTag.appendChild(self.dom.createTextNode("This test case is intended to verify the following implied or specified requirements:"))
        element = findElementById(nodes,"objective")
        element.insertBefore(paragraphTag,element.firstChild)
        paragraphTag = self.dom.createElement("p")
        paragraphTag.appendChild(self.dom.createTextNode(self.objectiveText[testID]))
        element.appendChild(paragraphTag)
        
    # provides the test requirement IDs for the current test case being processed
    def getTestRequirementIDs (self,testID):
        return self.requirementsInThisTest[testID]

# Class to handle the creation of the test case setup        
class Setup (Document):
    def __init__ (self,category):
        super(Setup,self).__init__("tools_configuration/TEST_CASE_TEMPLATE.html")
        testSetup = category + ".testDbPre"
        testSetupFile = open(testSetup,"r")
        line = testSetupFile.readline()
        self.setupText = {}
        while line != "":
            testID = line.strip().replace(" ","")
            self.setupText[testID] = testSetupFile.readline().strip()
            line = testSetupFile.readline()
        testSetupFile.close()

    # adds objective information into the test case DOM
    def insertIntoNodeList (self,nodes,testID):
        setupSteps = self.setupText[testID].split("/hr")

        # put setup steps in the DOM
        element = findElementById(nodes,"setup")
        for step in setupSteps:
            listItemTag = self.dom.createElement("li")
            listItemTag.appendChild(self.dom.createTextNode(step))
            element.appendChild(listItemTag)

# Class to handle the creation of the test case procedure steps/actions        
class Procedures (Document):
    def __init__ (self,category):
        super(Procedures,self).__init__("tools_configuration/TEST_CASE_TEMPLATE.html")
        testProcedures = category + ".testDbProcedures"
        testProceduresFile = open(testProcedures,"r")
        line = testProceduresFile.readline()
        self.procedureStepsText = {}
        while line != "":
            testID = line.strip().replace(" ","")
            self.procedureStepsText[testID] = testProceduresFile.readline().strip()
            line = testProceduresFile.readline()
        testProceduresFile.close()

    # adds action information into the test case DOM
    def insertIntoNodeList (self,nodes,testID):
        procedureSteps = self.procedureStepsText[testID].split("/step")
        procedureSteps.pop(0)

        element = findElementById(nodes,"actions")

        # put procedure steps in the DOM

        for p in procedureSteps:
            bullets = p.split("/bullet")
            step = bullets.pop(0)
            listItemTag = self.dom.createElement("li")
            listItemTag.appendChild(self.dom.createTextNode(step.replace("\step","")))
            if len(bullets) > 0:
                unorderedListTag = self.dom.createElement("ul")
                for b in bullets:
                    bulletListItemTag = self.dom.createElement("li")
                    bulletListItemTag.setAttribute("type","square")
                    bulletListItemTag.appendChild(self.dom.createTextNode(b.replace("\bullet","")))
                    unorderedListTag.appendChild(bulletListItemTag)
                listItemTag.appendChild(unorderedListTag)
            element.appendChild(listItemTag)

# Class to handle the creation of the expected results section        
class ExpectedResults (Document):
    def __init__ (self,category):
        super(ExpectedResults,self).__init__("tools_configuration/TEST_CASE_TEMPLATE.html")
        testExpectedResults = category + ".testDbExpectedResults"
        testExpectedResultsFile = open(testExpectedResults,"r")
        line = testExpectedResultsFile.readline()
        self.expectedResultsText = {}
        while line != "":
            testID = line.strip().replace(" ","")
            self.expectedResultsText[testID] = testExpectedResultsFile.readline().strip()
            line = testExpectedResultsFile.readline()
        testExpectedResultsFile.close()

    # adds expected results information into the test case DOM
    def insertIntoNodeList (self,nodes,testID):
        element = findElementById(nodes,"expected")
        element.appendChild(self.dom.createTextNode(self.expectedResultsText[testID]))

# Class to handle the creation of the results section        
class Results (Document):
    def __init__ (self,category):
        super(Results,self).__init__("tools_configuration/TEST_CASE_TEMPLATE.html")
        testResults = category + ".testDbResults"
        testResultsFile = open(testResults,"r")
        line = testResultsFile.readline()
        self.resultsText = {}
        while line != "":
            testID = line.strip().replace(" ","")
            self.resultsText[testID] = testResultsFile.readline().strip()
            line = testResultsFile.readline()
        testResultsFile.close()

    # adds results information into the test case DOM
    def insertIntoNodeList (self,nodes,testID):
        element = findElementById(nodes,"results")
        element.appendChild(self.dom.createTextNode(self.resultsText[testID]))
        return self.resultsText[testID]


# Class to handle the creation of the test case clean section
class Cleanup (Document):
    def __init__ (self,category):
        super(Cleanup,self).__init__("tools_configuration/TEST_CASE_TEMPLATE.html")
        testCleanup = category + ".testDbPost"
        testCleanupFile = open(testCleanup,"r")
        line = testCleanupFile.readline()
        self.cleanupText = {}
        while line != "":
            testID = line.strip().replace(" ","")
            self.cleanupText[testID] = testCleanupFile.readline().strip()
            line = testCleanupFile.readline()
        testCleanupFile.close()

    # adds cleanup information into the test case DOM
    def insertIntoNodeList (self,nodes,testID):
        cleanupSteps = self.cleanupText[testID].split("/hr")

        # put cleanup steps in the DOM
        element = findElementById(nodes,"cleanup")
        for step in cleanupSteps:
            listItemTag = self.dom.createElement("li")
            listItemTag.appendChild(self.dom.createTextNode(step))
            element.appendChild(listItemTag)

# Class to handle the creation of the test requirements section
class RequirementList (Document):
    def __init__ (self,category):
        super(RequirementList,self).__init__("tools_configuration/TEST_CASE_TEMPLATE.html")

    # adds requirement list information into the test case DOM
    def insertIntoNodeList (self,nodes,testID,objectiveObject):
        element = findElementById(nodes,"requirements")
        line = ", ".join(objectiveObject.getTestRequirementIDs(testID))
        element.appendChild(self.dom.createTextNode(line))

# Class to handle the creation of the test project section
class Project (Document):
    def __init__ (self):
        super(Project,self).__init__("tools_configuration/TEST_CASE_TEMPLATE.html")
        projectFile = open("PROJECT.testDb")
        self.projectName = projectFile.readline().strip()

    # adds requirement list information into the test case DOM
    def insertIntoNodeList (self,nodes):
        element = findElementById(nodes,"project")
        if element != None:
            element.appendChild(self.dom.createTextNode(self.projectName))

class TestCategory(Document):
    def __init__ (self,categoryName):
        super(TestCategory,self).__init__("tools_configuration/TOC_TEMPLATE.html")
        nodes = self.dom.childNodes

        if not os.path.exists(categoryName):
            os.makedirs(categoryName)

        titleFileName = categoryName + ".testDbCategoryTitle"
        titleDescription = categoryName + ".testDbCategoryDescription"

        toc = categoryName + "_toc.html"

        titleFile = open(titleFileName,"r")
        self.title = titleFile.read()
        titleFile.close()
        titleDescriptionFile = open(titleDescription,"r")
        description = titleDescriptionFile.read()
        titleDescriptionFile.close

        element = findElementById(nodes,"title")
        element.appendChild(self.dom.createTextNode(self.title))

        element = findElementById(nodes,"description")
        element.appendChild(self.dom.createTextNode(description))

        orderedListNode = findElementById(nodes,"list")

        testCases = TestCase(categoryName)
        identificationInformation = Identification(categoryName)

        self.status = "UNTESTED"

        for testID in testCases.getIDList():
            status = testCases.buildTestCase(testID)
            listItemTag = self.dom.createElement("li");
            anchorTag = self.dom.createElement("a")
            titleLine = testID + " - " + identificationInformation.identificationText[testID]

            anchorTag.setAttribute("href",categoryName+"/"+testID+".html")

            if status == "PASSED":
                anchorTag.setAttribute("style","color: 00F000")
                if self.status == "UNTESTED":
                    self.status = "PASSED"
            else:
                if status == "FAILED":
                    anchorTag.setAttribute("style","color: FF0000")
                    self.status = "FAILED"

            anchorTag.appendChild(self.dom.createTextNode(titleLine))
            listItemTag.appendChild(anchorTag)
            orderedListNode.appendChild(listItemTag)


        # write table of contents

        tocFile = open(toc,"w");
        tocFile.write(self.dom.toxml());
        tocFile.close()


class TestCase (Document):
    def __init__ (self,categoryName):
        super(TestCase,self).__init__("tools_configuration/TEST_CASE_TEMPLATE.html")
        self.categoryName = categoryName
        self.requirementsTestedInThisCategory = Requirements()
        self.objectiveSection = Objective(categoryName,self.requirementsTestedInThisCategory)
        self.setupSection = Setup(categoryName)
        self.procedureSection = Procedures(categoryName)
        self.expectedResultsSection = ExpectedResults(categoryName)
        self.resultsSection = Results(categoryName)
        self.cleanupSection = Cleanup(categoryName)
        self.requirementListSection = RequirementList(categoryName)
        self.identificationSections = Identification(categoryName)
        self.projectSection = Project()
        self.status = {}

    def getIDList (self) :
        return self.identificationSections.getIDList()

    def buildTestCase (self,testID) :
        self.dom = parse("tools_configuration/TEST_CASE_TEMPLATE.html")
        nodes = self.dom.childNodes

        testCaseFile = open(self.categoryName + "/" + testID + ".html","w");

        self.identificationSections.insertIntoNodeList(nodes,testID)
        self.projectSection.insertIntoNodeList(nodes)
        self.objectiveSection.insertIntoNodeList(nodes,testID,self.requirementsTestedInThisCategory)
        self.setupSection.insertIntoNodeList(nodes,testID)
        self.procedureSection.insertIntoNodeList(nodes,testID)
        self.expectedResultsSection.insertIntoNodeList(nodes,testID)
        self.status[testID] = self.resultsSection.insertIntoNodeList(nodes,testID)
        self.cleanupSection.insertIntoNodeList(nodes,testID)
        self.requirementListSection.insertIntoNodeList(nodes,testID,self.objectiveSection)
                        
        #write out the updated DOM which is now a test case in HTML
        testCaseFile.write(self.dom.toxml());
        testCaseFile.close();

        return self.status[testID]

def main():
    categoryName = str(sys.argv[1]) 

    TestCategory(categoryName)

if __name__ == "__main__":
    main()



