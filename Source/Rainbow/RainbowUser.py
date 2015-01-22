#   RainbowUser.py

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


class RainbowUser():

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
    hash = 0
    eof = False
    found = False
    key = ""
    iteration = 100000

    #Constructor
    def __init__(self):

        x=0


    #Sets the hash we're looking for
    def setHash(self, hash):

        self.hash = hash


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

        #Checks for filenotfound and returns code to caller class
        try:
            file = open(fileName, "r")
            file.close()

        except (OSError, IOError):
            return "Fail"

        return "Good"


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
        subChunkSize = 1

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
        #print paramsString
        paramsList = paramsString.split()
        #print paramsList
        self.algorithm = paramsList[1]

        self.hash = paramsList[2]

        self.alphabetChoice = paramsList[3]

        self.setAlphabet(self.alphabetChoice)

        self.numChars = int(paramsList[4])

        self.width = int(paramsList[8])

        self.iteration = self.width * 2

    '''
    #Returns a chunk with all variables needed by nodes
    def makeParamsChunk(self):

        tempChunk = Chunk()

        tempChunk.params = "rainbowuser " + self.algorithm + " 0 " + str(self.alphabetChoice) + " " + str(self.numChars)
        tempChunk.params += " " + str(self.numChars) + " 0 0 " + str(self.width) + " " + str(self.height)

        return tempChunk
    '''

    #Returns if eof
    def isEof(self):

        return self.eof


    #Returns T/F if found or not
    def isFound(self):

        return self.found

    #Returns key
    def getKey(self):

        return self.key

    #Gets the next chunk from the file to process
    def getNextChunk(self):

        #Open the file for reading
        self.file = open(self.fileName, 'r')

        #Seek to where we left off in the file
        self.file.seek(self.fileLocation)

        line = self.file.readline()

        data = ""

        #keeps count of how many lines we've pu in currentChunk[]
        lineCounter = 0

        #to send to controller to say we're not done yet
        eof = False

        while not line == "":

            data += line

            line = self.file.readline()

            if line == "":

                eof = True

            lineCounter += 1

            #If our chunk is at least 1000 lines, stop adding to it
            if lineCounter >= 100:

                line = ""

                eof = False

        #update class on where we are in the file
        self.fileLocation = self.file.tell()

        self.file.close()

        self.eof = eof

        chunk = Chunk()

        chunk.data = data

        chunk.params = "rainbowuser " + self.algorithm + " " + self.hash + " " + str(self.alphabetChoice)
        chunk.params += " " + str(self.numChars) + " 0 0 0 " + str(self.width) + " 0 "

        return chunk


    #Searches the chunk for the key (given the hash in the chunk.params)
    def find(self, chunk):

        x=1

        #Set class variables based on parameters from the chunk
        self.setVariables(chunk.params)

        #Split the data (as a string) into a list of lines
        linesList = chunk.data.splitlines()

        #First, we'll take the data and put it into two lists for searching

        #Make two lists, one for each key and one for each hash of the lines
        keyList = []
        hashList = []

        tempCounter = 0

        #For every line in the list
        for x in linesList:

            #Split the line into a list of the two elements
            lineList = x.split()

            #Put the key in the key list
            #keyList[tempCounter] = lineList[0]

            keyList.append(lineList[0])

            #put the hash in the hash list
            #hashList[tempCounter] = lineList[1]
            hashList.append(lineList[1])

        #Second, we'll actually do the searching
        #print keyList
        #print
        #print hashList
        #print

        done = False

        tempHash = self.hash

        #Which line we found the hash on
        where = 0

        timeout = 0

        #Did we find a matching line? (Y=1/N=0)
        signal = 0

        while not done:

            #For every hash in the list
            for x in hashList:

                #If our hash matches the one in the list
                if tempHash == x:

                    #We found the line that matches, now just search the line for the key
                    done = True
                    #print "Found 1"
                    #print tempHash
                    #print x
                    signal = 1

                    #Which line we found the hash on (index location)
                    where = hashList.index(x)
                    #print where

            if not done:

                tempReduced = self.getSeededKey(tempHash)

                tempHash = self.hashThis(tempReduced)

            timeout += 1

            #If we've searched farther than we're supposed to, stop
            if timeout > self.iteration:

                done = True

        #If we found a matching line
        if signal == 1:

            #Set our key to the starting key of that line
            tempKey = keyList[where]
            #print tempKey
            #print self.width
            #For as wide as our table is plus one
            for y in range(self.width + 1):

                #hash our tempKey
                tempHash = self.hashThis(tempKey)

                #print "tempHash: " + tempHash
                #print "tempKey:  " + tempKey

                #And compare to original key
                if self.hash == tempHash:

                    #FOUND THE KEY!
                    print "Key found!"

                    self.key = tempKey

                    self.found = True

                    self.done = True

                else:

                    #If not, reduce the hash and try again
                    tempKey = self.getSeededKey(tempHash)

            if self.found == False:

                #If we got this far,
                print "Collision Detected!"

        else:

            #No matching line found
            self.done = True

            print "No key found!"


    #Reads the first line of file to setup variables
    def gatherInfo(self):

        #Open the file for reading
        self.file = open(self.fileName, 'r')

        #Read the first line
        line = self.file.readline()

        #Update class on where we are in the file (hopefully, second line)
        self.fileLocation = self.file.tell()

        #Close the file, since we're done with it
        self.file.close()
        #print line
        #Split the line into a list, and assign list elements to variables
        varsList = line.split()
        #print varsList
        self.algorithm = varsList[0]

        self.numChars = int(varsList[1])

        self.alphabetChoice = varsList[2]

        self.width = int(varsList[3])
        #print self.width

    #Returns the original hash
    def getHash(self):

        return self.hash