#!/usr/bin/python
from buildHTMLSection import TestCategory
from buildHTMLSection import Document
from buildHTMLSection import Project
from buildHTMLSection import findElementById
import sys

class BookTOC(Document):
    def __init__ (self,sections,categoryStatus,categoryTitles):
        super(BookTOC,self).__init__("tools_configuration/BOOK_TOC_TEMPLATE.html")
        nodes = self.dom.childNodes

        project = Project()

        toc = project.projectName + "_toc.html"

        element = findElementById(nodes,"bookTitle")
        element.appendChild(self.dom.createTextNode(project.projectName + " - System Level Test Procedures"))

        orderedListNode = findElementById(nodes,"sectionList")
        firstListElement = orderedListNode.firstChild

        for category in sections:
            status = categoryStatus[category]
            listItemTag = self.dom.createElement("li");
            anchorTag = self.dom.createElement("a")
            titleLine = category + " - " + categoryTitles[category]

            anchorTag.setAttribute("href",category+"_toc.html")

            if status == "PASSED":
                anchorTag.setAttribute("style","color: 00F000")
            else:
                if status == "FAILED":
                    anchorTag.setAttribute("style","color: FF0000")

            anchorTag.appendChild(self.dom.createTextNode(titleLine))
            listItemTag.appendChild(anchorTag)
            orderedListNode.insertBefore(listItemTag,firstListElement)


        # write table of contents

        tocFile = open(toc,"w")
        tocFile.write(self.dom.toxml());
        tocFile.close()


def main():

    bookName = str(sys.argv[1]) 

    bookFile = open(bookName,"r")

    line = bookFile.readline()

    sections = []
    categoryStatus = {}
    categoryTitles = {}

    while line != "":
        line = line.strip()
        sections.append(line)
        testCategory = TestCategory(line)
        categoryStatus[line] = testCategory.status
        categoryTitles[line] = testCategory.title
        line = bookFile.readline()

    BookTOC(sections,categoryStatus,categoryTitles)

if __name__ == "__main__":
    main()



