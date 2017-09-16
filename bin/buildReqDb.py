#!/usr/bin/python
#Created on Apr 23, 2017
#
#@author: broihier

import sys
import re

def main ():
    requirementsTextFile = str(sys.argv[1])
    
    requirementsDbFileName = ""
    
    fileObject = open(requirementsTextFile,"r")
    
    line = fileObject.readline()
    while line != "" :
        if line.find("ID::") >= 0:
            line = line.replace("ID::","")
            idMatch = re.search("[^ ]+",line)
            if idMatch:
                if requirementsDbFileName == "":
                    prefixMatch = re.search("[^-]+",idMatch.group(0))
                    if prefixMatch:
                        requirementsDbFileName ="REQ."+prefixMatch.group(0)
                        outputFileObject = open (requirementsDbFileName,"w")
                        prefix = prefixMatch.group(0)
                    else:
                        sys.stdout.write("No prefix found to name requirements file\n")
                        exit(-1)
                else:
                    prefixMatch = re.search("[^-]+",idMatch.group(0))
                    if prefixMatch:
                        if prefixMatch.group(0) != prefix:
                            sys.stdout.write("Error - requirement prefix unexpectedly changed\n"+line+
                                             "\nlooking for: "+prefix+"\nfound: "+idMatch.group(0))
                            exit(-1)
                    else:
                        sys.stdout.write("Error - requirement prefix unexpectedly changed to null\n"+line)
                        exit(-1)
                        
                outputFileObject.write(idMatch.group(0)+"\n")
                line = line.replace(idMatch.group(0)+" ","")
                outputFileObject.write(line)
        line = fileObject.readline()
        
    outputFileObject.close()    

if __name__ == '__main__':
    main()