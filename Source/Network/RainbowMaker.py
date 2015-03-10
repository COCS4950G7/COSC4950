#   RainbowMaker.py

#   A companion to RainbowUser.py, RainbowMaker creates rainbow
#   tables for a time/cost trade-off. Essentially, it will pre-compute
#   a large amount of hashes so that they can be used later to
#   find a key (given a hash), in a manner that is many times
#   faster than a regular brute-force approach.

#   Chris Bugg
#   10/7/14

import hashlib
import random
import time
from multiprocessing import Process, Pipe, Lock, cpu_count
import os
import string

from Chunk import Chunk

class RainbowMaker():

    #Class Variables
    algorithm = 1
    numChars = 1
    alphabet = []
    #alphabetChoice = ""
    fileName = "1"
    file = 1
    width = 1
    height = 1
    hashList = []
    keyList = []
    done = False
    fileLocation = 1
    chunkCount = 0
    numProcesses = cpu_count()

    #Constructor
    def __init__(self):

        x=0

    #Sets the algorithm choice
    def setAlgorithm(self, algo):

        self.algorithm = algo


    #Sets the number of characters of the key
    def setNumChars(self, numChars):

        self.numChars = numChars


    #Get the alphabet and direction to be searched
    def setAlphabet(self, alphabet):

        self.alphabet = alphabet

        '''
        choicesList = list(alphabetChoice)

        self.alphabetChoice = ""

        for x in choicesList:

            self.alphabetChoice += str(x)

        lowerAlphabet = "abcdefghijklmnopqrstuvwxyz_"
        upperAlphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ_"
        digits = "0123456789_"
        punctuation = string.punctuation

        lowerAlphabetList = list(lowerAlphabet)
        upperAlphabetList = list(upperAlphabet)
        digitsList = list(digits)
        punctuationList = list(punctuation)

        self.alphabet = []

        for choice in choicesList:

            if choice == "a":

                self.alphabet += lowerAlphabetList

            elif choice == "A":

                self.alphabet += upperAlphabetList

            elif choice == "p":

                self.alphabet += punctuationList

            elif choice == "d":

                self.alphabet += digitsList

            else:

                return False

        return True
    '''


    #Get file name
    def setFileName(self, fileName):

        self.fileName = fileName


    #Gets the fileName
    def getFileName(self):

        return self.fileName


    #Get dimensions of the table
    def setDimensions(self, chainLength, numRows):

        self.width = int(chainLength)

        self.height = int(numRows)


    #Returns whether or not we're done creating
    def isDone(self):

        return self.done


    #Hashes key
    def hashThis(self, key):

        return hashlib.new(self.algorithm, key).hexdigest()


    #Produces seeded key (Reduction Function)
    def getSeededKey(self, seed):

        random.seed(seed)

        seedKey = ""

        characters = int(self.numChars)

        for x in range(characters):

            seedKey = seedKey + random.choice(self.alphabet)

        return seedKey


    #Produces a random key to start
    def getRandKey(self):

        random.seed()

        randKey = ""

        characters = int(self.numChars)

        for x in range(characters):

            randKey = randKey + random.choice(self.alphabet)

        return randKey


    #Finds collisions so the user can determine if they want to run collisionFixer()
    def collisionFinder(self):

        #Open file for reading
        self.file = open(self.fileName, 'r')

        #Make every line an element in a list
        allLinesList = list(self.file)

        #Close the dang file
        self.file.close()

        #Number of offending hashes (duplicates)
        offenderCount = 0

        #For every line (x) in the list (of all the lines)
        for x in allLinesList:

            #Split the line into a list of two (key and hash)
            lineListX = x.split()

            #Store hash value in temp var
            hashX = lineListX[1]

            #How many times have we seen this hash
            hashCount = 0

            #For every other line in the list (of all the lines)
            for y in allLinesList:

                #Split the line into a list of two (key and hash)
                lineListY = y.split()

                #Store hash value in temp var
                hashY = lineListY[1]

                if hashX == hashY:

                    hashCount += 1

            #If this hash has duplicates, increment offenderCount
            if hashCount > 1:

                offenderCount += 1

        #Returns the number of duplicate hashes
        return offenderCount


    #Finds and fixes collisions in the final hash list
    def collisionFixer(self):

        #Create/open file
        self.file = open(self.fileName, 'r')

        #Make every line an element in a list
        allLinesList = list(self.file)

        self.file.close()

        #Counter to keep track of how many duplicates
        offenderCount = 0

        #For every line (x) in the list (of all the lines)
        for x in allLinesList:

            #Split the line into a list of two (key and hash)
            lineListX = x.split()

            #Store hash value in temp var
            hashX = lineListX[1]

            #How many times have we seen this hash
            hashCount = 0

            #For every other line in the list (of all the lines)
            for y in allLinesList:

                #Split the line into a list of two (key and hash)
                lineListY = y.split()

                #Store hash value in temp var
                hashY = lineListY[1]

                if hashX == hashY:

                    hashCount += 1

            #If this hash has duplicates, increment offenderCount
            if hashCount > 1:

                #remove that line (since it's a duplicate)
                allLinesList.remove(x)

                offenderCount += 1

        #for every line that was a duplicate, make a new one
        for x in range(offenderCount):

            #Get a new key for this row
            randKey = self.getRandKey()

            reduced = randKey

            #Do the iteration for this row
            for y in range(self.width):

                hash = self.hashThis(reduced)

                reduced = self.getSeededKey(hash)

            hash = self.hashThis(reduced)

            line = randKey + " " + hash + "\n"

            allLinesList.append(line)

        #Create/open file
        self.file = open(self.fileName, 'r+')

        for z in allLinesList:

            self.file.write("%s" % z)

        self.file.close()


    #Sets up the file initially (put info in first line)
    def setupFile(self):

        #Open the file for writing
        self.file = open(self.fileName, 'w')

        self.file.write(self.algorithm + " " + str(self.numChars) + " " + str(self.alphabet) + " " + str(self.width) + "\n")

        self.fileLocation = self.file.tell()

        self.file.close()


    #Puts a done chunk (already processed by a node) into the table (file)
    def putChunkInFile(self, chunkOfDone):

        #Split chunkOfDone's data into a list
        linesList = chunkOfDone.data.splitlines()

        #Open the file for writing
        self.file = open(self.fileName, 'r+')

        #Seek to where we left off in the file
        self.file.seek(self.fileLocation)

        for x in linesList:

            #print to file
            self.file.write(x + "\n")

            #And increment count
            self.chunkCount += 1

        #Save where we are in file
        self.fileLocation = self.file.tell()

        #Close the file
        self.file.close()

        #Check if we've gotten all the chunks we need
        if self.chunkCount >= self.height:

            #Chunk count will now represent the true height (since we're done adding to it)
            self.height = self.chunkCount

            self.done = True


    #Create (and return) a chunk of the table, and do all that sub-process stuff
    def create(self, paramsChunk):

        #Set variables to that of server, get from parameter(-bearing) chunk
        self.setVariables(paramsChunk.params)

        #big list containing all the lines from the nodes
        bigChunk = ""

        subChunkSize = 100

        #Create lock
        lock = Lock()

        #Create the pipes
        parentPipe, childPipe = Pipe()

        children = []

        for i in range(0, self.numProcesses):
            children.append(Process(target=self.subProcess, args=(childPipe, lock, subChunkSize, )))
            children[i].start()

        #Count our iterations of responses
        count = 0

        #Are we done yet?
        done = False

        rec = 0

        while not done:

            #If all the nodes have given us their lists
            if count > (self.numProcesses - 1):

                for i in range(0, self.numProcesses):

                    children[i].join()

                    self.found = False

                    self.done = True

                    done = True

            else:

                #Get a sub-chunk from a node
                rec = parentPipe.recv()

                bigChunk += rec

                count += 1

        returnChunk = Chunk()

        returnChunk.data = bigChunk

        return returnChunk


    #The sub-process function
    def subProcess(self, pipe, lock, chunkSize):

        #The list to return with strings to be the lines of the file
        daList = ""

        for x in range(chunkSize):

            randKey = self.getRandKey()

            reduced = randKey

            #hash = self.hashThis(reduced)

            for y in range(self.width):

                hash = self.hashThis(reduced)

                reduced = self.getSeededKey(hash)

            hash = self.hashThis(reduced)

            daList += randKey + " " + hash + "\n"

        lock.acquire()

        pipe.send(daList)

        pipe.close()

        lock.release()


    #Returns number of rows in table
    def numRows(self):

        return self.height


    #Returns number of columns (chains) in table
    def getLength(self):

        return self.width


    #Returns number of rows in table
    def getHeight(self):

        return self.height


    #Resets all class variables to default
    def reset(self):

        self.algorithm = 1
        self.numChars = 1
        self.alphabet = 1
        #self.alphabetChoice = 1
        self.fileName = "1"
        self.file = 1
        self.width = 1
        self.height = 1
        self.hashList = []
        self.keyList = []
        self.done = False
        self.fileLocation = 1
        self.chunkCount = 0


    #Sets all class variables to ones given from server (params)
    def setVariables(self, paramsString):

        paramsList = paramsString.split()

        self.algorithm = paramsList[1]

        self.alphabet = paramsList[3]

        self.setAlphabet(self.alphabet)

        self.numChars = int(paramsList[4])

        self.width = int(paramsList[8])

        self.height = int(paramsList[9])


    #Returns a chunk with all variables needed by nodes
    def makeParamsChunk(self):

        tempChunk = Chunk()

        tempChunk.params = "rainbowmaker " + self.algorithm + " 0 " + str(self.alphabet) + " " + str(self.numChars)
        tempChunk.params += " " + str(self.numChars) + " 0 0 " + str(self.width) + " " + str(self.height)

        return tempChunk