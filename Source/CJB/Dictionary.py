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

    #Constructor
    def __init__(self):

        x=1

    #Sets algorithm to be used
    def setAlgorithm(self, algorithm):

        x=1

    #Sets the dictionary file's name
    def setFileName(self, fileName):

        x=1

    #Sets the original hash we're looking for
    def setHash(self, hash):

        x=1

    #Actually finds the hash in the file (hopefully)
    def find(self):

        x=1

    #Returns T/F if done searching or not
    def done(self):

        x=1

    #Returns status summary of searching so far
    def status(self):

        x=1

    #
    def found(self):

        x=1