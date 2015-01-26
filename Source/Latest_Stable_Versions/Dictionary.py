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

#   Updated 10/18/14:
#       Should be functioning? Tested on many lists of many sizes and it works just fine...--Latest_Stable_Versions

#   Updated 10/30/14:
#       Can now deal with filenotfound, multiple hash functions, and work with new console-UI --Latest_Stable_Versions

#Imports
import hashlib
import time
from multiprocessing import Process, Pipe, Lock, cpu_count, Queue, Value
import os
from Chunk import Chunk
import random

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
    allLinesList = []
    fileLocation = 0
    eof = False
    numProcesses = cpu_count()
    #queue = Queue(numProcesses * 5)

    #Constructor
    def __init__(self):

        x=1

    #Sets algorithm to be used
    def setAlgorithm(self, algorithm):

        self.algorithm = algorithm

    #Sets the dictionary file's name
    def setFileName(self, fileName):

        self.fileName = fileName

        #Checks for filenotfound and returns code to caller class
        try:
            file = open(fileName, "r")
            file.close()

        except (OSError, IOError):
            return "Fail"

        return "Good"

    #Sets the original hash we're looking for
    def setHash(self, hash):

        self.hash = hash

    #Actually finds the hash in the file (hopefully)
    def find(self, chunk):

        #Turns data from string to list
        chunkList = chunk.data.split()

        #turns params from string to list
        paramsList = chunk.params.split()

        #set some class params with new info
        self.algorithm = paramsList[1]

        self.hash = paramsList[2]

        #Sub chunk chunkList and call processes
        chunky = self.chunkIt(chunkList, self.numProcesses)

        lock = Lock()

        parentPipe, childPipe = Pipe()

        children = []

        for i in range(0, self.numProcesses):
            children.append(Process(target=self.subProcess, args=(childPipe, lock, )))
            children[i].start()

        for chunk in chunky:

            parentPipe.send(chunk)

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
    def subProcess(self, pipe, lock):

        lock.acquire()

        chunkList = pipe.recv()

        lock.release()

        #for every item in the allLinesList list
        for x in chunkList:

            #Split the string ['able\r\n'] into a list ['able','\r','\n']
            xLineToList = x.split()

            #Check if it's NOT empty (or eof)
            if xLineToList:

                #If it's not, extract the word (leaving an '/n')
                newX = xLineToList.pop()

            else:

                #Otherwise give it an empty value that doesn't crash the program
                newX = ""

            #if the hashes match, YAY, return to get out of function
            if self.hashThis(newX) == self.hash:

                lock.acquire()

                pipe.send("found")

                pipe.send(newX)

                pipe.close()

                lock.release()

                return 0

        lock.acquire()

        pipe.send("not found")

        pipe.close()

        lock.release()

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

        thisHash = hashlib.new(self.algorithm, key).hexdigest()

        return thisHash

    #Returns key
    def showKey(self):

        return self.key

    #Returns hash
    def getHash(self):

        return self.hash

    #Convers all lines of file into global list
    def makeListOfFile(self):

        #Open the file for reading
        self.file = open(self.fileName, 'r')

        #Put all the lines of the file in a list
        self.allLinesList = list(self.file)

        self.file.close()

    #Returns list of lines in file
    def getList(self):

        return self.allLinesList

    #Chunks up a list
    def chunkIt(self, list, pieces):

        chunky = [list[i::pieces] for i in range(pieces)]

        return chunky

    #Gets next chunk of file as list
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
            if lineCounter >= 10000:

                line = ""

                eof = False

        #update class on where we are in the file
        self.fileLocation = self.file.tell()

        self.file.close()

        self.eof = eof

        chunk = Chunk()

        chunk.data = data

        chunk.params = "dictionary " + self.algorithm + " " + self.hash + " 0 0 0 0 " + str(self.fileLocation) + " 0 0 "

        return chunk

    #Returns if eof
    def isEof(self):

        return self.eof

    #Resets class object to default values
    def reset(self):

        self.done = False
        self.algorithm = ""
        self.fileName = ""
        self.hash = ""
        self.status = ""
        self.found = False
        self.file = 0
        self.key = ""
        self.allLinesList = []
        self.fileLocation = 0
        self.eof = False

    #Sets key
    def setKey(self, key):

        self.key = key

    #Gets next chunk of file as list
    def getThisChunk(self, params):

        #Open the file for reading
        self.file = open(self.fileName, 'r')

        #Get the chunk's fileLocation from params
        #turns params from string to list
        paramsList = params.split()

        #set fileLocation to equivalent params value
        fileLocation = paramsList[7]

        #Seek to where we left off in the file
        self.file.seek(fileLocation)

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
            if lineCounter >= 10000:

                line = ""

                eof = False

        #update class on where we are in the file
        fileLocation = self.file.tell()

        self.file.close()

        self.eof = eof

        chunk = Chunk()

        chunk.data = data

        chunk.params = "dictionary " + self.algorithm + " " + self.hash + " 0 0 0 0 " + str(fileLocation) + " 0 0 "

        return chunk