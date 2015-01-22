#   RainbowMaker.py

#   DESCRIPTION HERE

#   Chris Bugg
#   10/7/14

import hashlib
import random
import time
from multiprocessing import Process, Pipe, Lock
import os
import string

from Chunk import Chunk

class RainbowMaker():

    #Class Variables
    algorithm = 1
    numChars = 1
    alphabet = 1
    alphabetChoice = 1
    fileName = "1"
    file = 1
    width = 1
    height = 1
    hashList = []
    keyList = []
    done = False
    fileLocation = 1
    chunkCount = 0

    #Constructor
    def __init__(self):
        '''
        #Make the table
        self.makeTable()

        #Start the timer
        start = time.clock()

        #Import Table
        self.importTable()

        #Check for collisions
        while self.collisionFixer() == 1:

            #Import Table
            self.importTable()

        #Check on timer
        elapsed = (time.clock() - start)
        print("That took: ", elapsed, " seconds.")

        exit = input("Done! Hit (Enter/Return) to quit ")
        '''
        x=0

    #Sets the algorithm choice
    def setAlgorithm(self, algo):

        self.algorithm = algo


    #Sets the number of characters of the key
    def setNumChars(self, numChars):

        self.numChars = numChars


    #Get the alphabet and direction to be searched
    def setAlphabet(self, alphabetChoice):

        self.alphabetChoice = alphabetChoice

        #Setup the lookup alphabet
        mixedAlphaNumeric = "abcdefghijklmnopqrstuvwxyz_0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        mixedAlphabet = "abcdefghijklmnopqrstuvwxyz_ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        lowerAlphabet = "abcdefghijklmnopqrstuvwxyz_"
        upperAlphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ_"
        digits = "0123456789_"

        mixedAlphaNumericList = list(mixedAlphaNumeric)
        mixedAlphabetList = list(mixedAlphabet)
        lowerAlphabetList = list(lowerAlphabet)
        upperAlphabetList = list(upperAlphabet)
        digitsList = list(digits)

        #set alphabet
        if self.alphabetChoice == "a":

            self.alphabet = lowerAlphabetList

        elif self.alphabetChoice == "A":

            self.alphabet = upperAlphabetList

        elif self.alphabetChoice == "m":

            self.alphabet = mixedAlphabetList

        elif self.alphabetChoice == "M":

            self.alphabet = mixedAlphaNumericList

        elif self.alphabetChoice == "d":

            self.alphabet = digitsList


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

    '''
    #Make the table
    def makeTable(self):

        #Start the timer
        start = time.clock()

        print("Working...")

        #Create/open file
        self.file = open(self.fileName, 'w')

        #Put useful info in first line
        self.file.write(self.algorithm
                        + " " + self.numChars
                        + " " + self.alphabetChoice
                        + " " + str(self.width) + "\n")

        for x in range(self.height):

            randKey = self.getRandKey()

            reduced = randKey

            #hash = self.hashThis(reduced)

            for y in range(self.width):

                hash = self.hashThis(reduced)

                reduced = self.getSeededKey(hash)

            hash = self.hashThis(reduced)

            #Print to file
            self.file.write(randKey + " " + hash + "\n")

        #Check on timer
        elapsed = (time.clock() - start)
        print("That took: ", elapsed, " seconds.")

        #Close the file
        self.file.close()
        '''

    #Hashes key
    def hashThis(self, key):

        return hashlib.new(self.algorithm, key).hexdigest()


    #Produces seeded key
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

    '''
    #Finds and fixes collisions in the final hash list
    def collisionFixer(self):

        print("Collision Detector Running...")

        #Create/open file
        self.file = open(self.fileName, 'r+')

        #List of duplicate hashes
        offenderList = []

        #Counter to keep track of how many duplicates
        offenderCount = 0

        #Get all the duplicates and put them in offenderList
        for x in self.hashList:

            count = 0

            for y in self.hashList:

                if x == y:

                    count += 1

            if count > 1:

                offenderList.append(x)

                offenderCount += 1

        #if there are any duplicates, deal with them
        if offenderCount > 0:

            print((offenderCount // 2), " Collisions Detected!")

            #NOT MY CODE
            # Read in the file once and build a list of line offsets
            line_offset = []

            offset = 0

            for line in self.file:

                line_offset.append(offset)

                offset += len(line)

            self.file.seek(line_offset[1])

            #Get rid of duplicates in offenderList
            offenderList = list(set(offenderList)) ################
            #print(offenderList)#######################

            #for every hash in duplicate list
            for x in offenderList:

                #Get the location in the file of the duplicate
                position = (self.hashList.index(x) + 1)
                #print("Position: ", position)#################
                #Get a new key for this row
                randKey = self.getRandKey()

                reduced = randKey

                #hash = self.hashThis(reduced)

                #Do the iteration for this row
                for y in range(self.width):

                    hash = self.hashThis(reduced)

                    reduced = self.getSeededKey(hash)

                hash = self.hashThis(reduced)

                #seek to the correct line
                self.file.seek(line_offset[position])

                #Print to file
                self.file.write(randKey + " " + hash + "\n")

            print("Collisions Fixed!")

            #Close the file
            self.file.close()

            return 1

        else:

            print("No Collisions found!")

            #Close the file
            self.file.close()

            return 0
    '''
    '''
    #Import table
    def importTable(self):

        #Create/open file
        self.file = open(self.fileName, 'r')

        #Put all lines into a list
        allLinesList = list(self.file)

        #Take out the first line since it's junk to us
        allLinesList.pop(0)

        #Clear these values
        self.hashList = []

        self.keyList = []

        for x in allLinesList:

            #Split line from string to list
            lineList = x.split()

            #add hash to hashList
            self.hashList.append(lineList.pop())

            #add key to keyList
            self.keyList.append(lineList.pop())

        #Close the file
        self.file.close()
    '''

    #Sets up the file initially (put info in first line)
    def setupFile(self):

        #Open the file for writing
        self.file = open(self.fileName, 'w')

        self.file.write(self.algorithm + " " + str(self.numChars) + " " + self.alphabetChoice + " " + str(self.width) + "\n")

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

            self.done = True


    #Create (and return) a chunk of the table, and do all that sub-process stuff
    def create(self, paramsChunk):

        #Set variables to that of server, get from parameter(-bearing) chunk
        self.setVariables(paramsChunk.params)

        #ChunkSize is the number of rows in the file that we're creating in this, 'chunk'

        #return chunkSize

        #We're creating the children
        #Then setting them up with an equal sub-chunksize
        #IE: chunksize/numSubprocesses = sub-chunksize

        #Then we listen for them to get done and send us a list
        #Then we're done once they've sent their lists (return)

        #big list containing all the lines from the nodes
        bigChunk = ""

        #sub-process's chunk size (num rows to calculate)
        #subChunkSize = chunkSize / 8
        subChunkSize = 10

        #Create lock
        lock = Lock()

        #Create the pipes
        parentPipe, childPipe = Pipe()

        #Create the children
        child1 = Process(target=self.subProcess, args=(childPipe, lock, subChunkSize, ))

        child2 = Process(target=self.subProcess, args=(childPipe, lock, subChunkSize, ))

        child3 = Process(target=self.subProcess, args=(childPipe, lock, subChunkSize, ))

        child4 = Process(target=self.subProcess, args=(childPipe, lock, subChunkSize, ))

        child5 = Process(target=self.subProcess, args=(childPipe, lock, subChunkSize, ))

        child6 = Process(target=self.subProcess, args=(childPipe, lock, subChunkSize, ))

        child7 = Process(target=self.subProcess, args=(childPipe, lock, subChunkSize, ))

        child8 = Process(target=self.subProcess, args=(childPipe, lock, subChunkSize, ))

        #start the children
        child1.start()

        child2.start()

        child3.start()

        child4.start()

        child5.start()

        child6.start()

        child7.start()

        child8.start()

        #Count our iterations of responses
        count = 0

        #Are we done yet?
        done = False

        rec = 0

        while not done:

            #If all the nodes have given us their lists
            if count > 7:

                child1.join()

                child2.join()

                child3.join()

                child4.join()

                child5.join()

                child6.join()

                child7.join()

                child8.join()

                #self.done = True

                done = True

            else:

                #Get a sub-chunk from a node
                rec = parentPipe.recv()

                #while the list(sub-chunk) from node is not empty
                #while rec:

                    #Put a line of the list in our bigChunk

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


    #Resets all class variables to default
    def reset(self):

        self.algorithm = 1
        self.numChars = 1
        self.alphabet = 1
        self.alphabetChoice = 1
        self.fileName = "1"
        self.file = 1
        self.width = 1
        self.height = 1
        self.hashList = []
        self.keyList = []
        self.done = False


    #Sets all class variables to ones given from server (params)
    def setVariables(self, paramsString):

        paramsList = paramsString.split()

        self.algorithm = paramsList[1]

        self.alphabetChoice = paramsList[3]

        self.setAlphabet(self.alphabetChoice)

        self.numChars = int(paramsList[4])

        self.width = int(paramsList[8])

        self.height = int(paramsList[9])


    #Returns a chunk with all variables needed by nodes
    def makeParamsChunk(self):

        tempChunk = Chunk()

        tempChunk.params = "rainbowmaker " + self.algorithm + " 0 " + str(self.alphabetChoice) + " " + str(self.numChars)
        tempChunk.params += " " + str(self.numChars) + " 0 0 " + str(self.width) + " " + str(self.height)

        return tempChunk