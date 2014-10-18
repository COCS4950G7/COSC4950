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
import time
from multiprocessing import Process, Pipe, Lock
import os

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
    def find(self, chunkList):

        #Open the file for reading
        #self.file = open(self.fileName, 'r')

        #Put all the lines of the file in a list
        #allLinesList = list(self.file)

        #self.file.close()

        #Sub chunk chunkList and call processes
        #chunky = self.chunkIt(chunkList, 4)
        chunky = chunkList

        chunk1 = chunky.pop()

        chunk2 = chunky.pop()

        chunk3 = chunky.pop()

        chunk4 = chunky.pop()

        lock = Lock()

        parentPipe, childPipe = Pipe()

        child1 = Process(target=self.subProcess, args=(childPipe, lock, ))

        child2 = Process(target=self.subProcess, args=(childPipe, lock, ))

        child3 = Process(target=self.subProcess, args=(childPipe, lock, ))

        child4 = Process(target=self.subProcess, args=(childPipe, lock, ))

        child1.start()

        child2.start()

        child3.start()

        child4.start()

        parentPipe.send(chunk1)

        parentPipe.send(chunk2)

        parentPipe.send(chunk3)

        parentPipe.send(chunk4)

        count = 0

        done = False

        rec = 0

        while not done:

            if count > 3:

                child1.join()

                child2.join()

                child3.join()

                child4.join()

                self.found = False

                self.done = True

                done = True

            else:

                rec = parentPipe.recv()

                if rec == "found":

                    self.key = parentPipe.recv()

                    child1.terminate()

                    child2.terminate()

                    child3.terminate()

                    child4.terminate()

                    done = True

                    self.found = True

                    self.done = True

                count += 1

        #listSize = len(chunkList)
        #countey = 0
        #self.status = "Searching"

    #The sub-process function
    def subProcess(self, pipe, lock):

        lock.acquire()

        chunkList = pipe.recv()

        lock.release()

        #if self.looper6(alphabet, lock ) == True:

        #Do Work here

        #listSize = len(chunkList)
        #countey = 0
        #self.status = "Searching"
        #print "chunkList @ subprocess: ", chunkList
        #for every item in the allLinesList list
        for x in chunkList:

            #self.status = (countey / listSize), " %"
            #countey += 1

            #Split the string into a list
            #print xLineToList
            #print "x: ", x
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

                #self.key = newX

                #self.done = True

                #self.found = True

                lock.acquire()

                pipe.send("found")

                pipe.send(newX)

                pipe.close()

                lock. release()

                return 0

        #Otherwise...
        #self.found = False

        #self.done = True

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

        thisHash = hashlib.md5(key).hexdigest()

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

        #print "chunkIt gets ", list
        #print "and gives ", chunky

        return chunky