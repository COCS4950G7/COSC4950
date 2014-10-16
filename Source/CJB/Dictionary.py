#   Dictonary.py

#   Uses a dictionary file to attempt to crack the hash.
#   Simply reads through the file line by line, and tries each entry.
#   Possible source for passwords are 'top most used passwords' lists

# Updated on 10/12/2014:
#   Chris Hamm is working on this section.
#   added in comments and some thoughts
    #need to create constructor
        #create flags for local variables
            #possible flags (RECOMMEND USING SWITCH-CASE STATEMENTS HERE)
                #a-z (contain in array)
                #A-Z (contain in array)
                #0-9 (contain in array)
                #special symbols !@#$%^&*()_+-=\|/ etc (contain in array)
                #All ASCII characters (includes all of the above) (contains all of the arrays listed above in one big array)
    #need to correct import file based on set flag values
    #need to use password read from file and try to get the matching hash until found or end of file
    #needs to output progress also

#   Updated on 10/15/14:
#   Chris Bugg is working on this class now

#Imports
import hashlib

class Dictionary():

    #class variables
    done = False
    algorithm = ""
    fileName = ""
    hash = ""
    status = ""
    found = False
    file = 0
    key = ""

    #Constructor
    def __init__(self):

        x=1

    #Sets algorithm to be used
    def setAlgorithm(self, algorithm):

        self.algorithm = algorithm

    #Sets the dictionary file's name
    def setFileName(self, fileName):

        self.fileName = fileName

    #Sets the original hash we're looking for
    def setHash(self, hash):

        self.hash = hash

    #Actually finds the hash in the file (hopefully)
    def find(self):

        #Open the file for reading
        self.file = open(self.fileName, 'r')

        #Put all the lines of the file in a list
        allLinesList = list(self.file)

        self.file.close()

        listSize = len(allLinesList)
        countey = 0
        #self.status = "Searching"

        #for every item in the allLinesList list
        for x in allLinesList:

            self.status = (countey / listSize), " %"
            countey += 1

            #Split the string into a list
            xLineToList = x.split()

            #Check if it's empty (or eof)
            if xLineToList:

                #If it's not, extract the word (leaving an '/n')
                newX = xLineToList.pop()

            else:

                #Otherwise give it an empty value that doesn't crash the program
                newX = ""

            #if the hashes match, YAY, return to get out of function
            if self.hashThis(newX) == self.hash:

                self.key = newX

                self.done = True

                self.found = True

                return 0

        #Otherwise...
        self.found = False

        self.done = True

    #Returns T/F if done searching or not
    def isDone(self):

        return self.done

    #Returns status summary of searching so far
    def getStatus(self):

        return self.status

    #Returns T/F if found or not
    def isFound(self):

        return self.found

    #Hashes a key
    def hashThis(self, key):

        thisHash = hashlib.md5(key).hexdigest()

        return thisHash

    #Returns key
    def showKey(self):

        return self.key

    #Returns hash
    def getHash(self):

        return self.hash