#   RainbowUser.py

#   A companion to RainbowMaker.py, RainbowUser uses a pre-computed
#   rainbow table to search for a given hash, attempting to find the
#   associated key.

#   Chris Bugg
#   10/7/14


import hashlib
import random
import time
from multiprocessing import Process, Pipe, Lock, cpu_count
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
    numProcesses = cpu_count()

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
        #self.alphabetChoice = 1
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

        self.hash = paramsList[2]

        self.alphabet = paramsList[3]

        self.setAlphabet(self.alphabet)

        self.numChars = int(paramsList[4])

        self.width = int(paramsList[8])

        self.iteration = self.width * 2


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
            if lineCounter >= 1000:

                line = ""

                eof = False

        #update class on where we are in the file
        self.fileLocation = self.file.tell()

        self.file.close()

        self.eof = eof

        chunk = Chunk()

        chunk.data = data

        chunk.params = "rainbowuser " + self.algorithm + " " + self.hash + " " + str(self.alphabet)
        chunk.params += " " + str(self.numChars) + " 0 0 0 " + str(self.width) + " 0 " + str(eof)

        return chunk

    #Searches the chunk for the key (given the hash in the chunk.params)
    def find(self, chunk):

        #Set class variables based on parameters from the chunk
        self.setVariables(chunk.params)

        #Split the data (as a string) into a list of lines
        linesList = chunk.data.splitlines()

        #
        # First, we'll take the data and put it into two lists for searching

        #Make two lists, one for each key and one for each hash of the lines
        keyList = []
        hashList = []

        tempCounter = 0

        #For every line in the list
        for x in linesList:

            #Split the line into a list of the two elements
            lineList = x.split()

            #Put the key in the key list
            keyList.append(lineList[0])

            #put the hash in the hash list
            hashList.append(lineList[1])

        #divides up list into smaller lists, that we will feed the sub-processes
        keySubList = self.chunkIt(keyList, self.numProcesses)
        hashSubList = self.chunkIt(hashList, self.numProcesses)

        #
        # Second, we'll actually do the searching

        lock = Lock()

        parentPipe, childPipe = Pipe()

        children = []

        for i in range(0, self.numProcesses):
            children.append(Process(target=self.subProcess, args=(childPipe, lock, keySubList[i], hashSubList[i], )))
            children[i].start()

        count = 0

        done = False

        rec = 0

        while not done:

            if count > (self.numProcesses - 1):

                for i in range(0, self.numProcesses):

                    children[i].join()

                    self.found = False

                    self.done = True

                    done = True

            else:

                rec = parentPipe.recv()

                if rec == "found":

                    self.key = parentPipe.recv()

                    for i in range(0, self.numProcesses):

                        children[i].terminate()

                    done = True

                    self.found = True

                    self.done = True

                count += 1


    #The sub-process function
    def subProcess(self, pipe, lock, keyList, hashList):

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

                    signal = 1

                    #Which line we found the hash on (index location)
                    where = hashList.index(x)

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

            #For as wide as our table is plus one
            for y in range(self.width + 1):

                #hash our tempKey
                tempHash = self.hashThis(tempKey)

                #And compare to original key
                if self.hash == tempHash:

                    #FOUND THE KEY!

                    self.found = True

                    self.done = True

                    lock.acquire()

                    pipe.send("found")

                    pipe.send(tempKey)

                    pipe.close()

                    lock.release()

                else:

                    #If not, reduce the hash and try again
                    tempKey = self.getSeededKey(tempHash)

            if self.found == False:

                self.done = True

                lock.acquire()

                pipe.send("collisionDetected")

                pipe.close()

                lock.release()

        else:

            #No matching line found
            self.done = True

            lock.acquire()

            pipe.send("notFound")

            pipe.close()

            lock.release()


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

        self.alphabet = varsList[2]

        self.alphabet = self.setAlphabet(self.alphabet)

        self.width = int(varsList[3])
        #print self.width

    #Returns the original hash
    def getHash(self):

        return self.hash


    #Divides up a list, and stores those sub-lists in a big list
    def chunkIt(self, list, pieces):

        chunky = [list[i::pieces] for i in range(pieces)]

        return chunky