__author__ = 'ChrisBugg'

#   Chris Bugg
#   10/1/14

#   NOTE: Runs on Python 2.7.6

#   UPDATE:
#   10/10/14
#       -> Now runs with 8 sub-processes using
#          the [a-z] alphabet

import hashlib
from time import time
from multiprocessing import Process, Pipe, Lock
import os

class DemoCrack():

    algorithm = "sha256"
    origHash = ''
    #alphabet = list("0123456789")
    alphabet = list("abcdefghijklmnopqrstuvwxyz")
    chunk1 = 1
    chunk2 = 1
    key = ''
    alphaChoice = "abcdefghijklmnopqrstuvwxyz"
    countey = 0


    def __init__(self):

        os.system('cls' if os.name == 'nt' else 'clear')
        self.whatWeGot()

        self.getHash()

        os.system('cls' if os.name == 'nt' else 'clear')
        self.whatWeGot()

        self.chunkIt()

        start = time()

        self.countey += 1

        lock = Lock()

        parentPipe, childPipe = Pipe()

        child1 = Process(target=self.subProcess, args=(childPipe, lock, ))

        child2 = Process(target=self.subProcess, args=(childPipe, lock, ))

        child3 = Process(target=self.subProcess, args=(childPipe, lock, ))

        child4 = Process(target=self.subProcess, args=(childPipe, lock, ))

        child5 = Process(target=self.subProcess, args=(childPipe, lock, ))

        child6 = Process(target=self.subProcess, args=(childPipe, lock, ))

        child7 = Process(target=self.subProcess, args=(childPipe, lock, ))

        child8 = Process(target=self.subProcess, args=(childPipe, lock, ))

        child1.start()

        child2.start()

        child3.start()

        child4.start()

        child5.start()

        child6.start()

        child7.start()

        child8.start()

        parentPipe.send("6")
        parentPipe.send(self.chunk1)

        parentPipe.send("6")
        parentPipe.send(self.chunk2)

        parentPipe.send("6")
        parentPipe.send(self.chunk3)

        parentPipe.send("6")
        parentPipe.send(self.chunk4)

        parentPipe.send("6")
        parentPipe.send(self.chunk5)

        parentPipe.send("6")
        parentPipe.send(self.chunk6)

        parentPipe.send("6")
        parentPipe.send(self.chunk7)

        parentPipe.send("6")
        parentPipe.send(self.chunk8)

        count = 0

        done = False

        rec = 0

        while not done:

            if count > 7:

                child1.join()

                child2.join()

                child3.join()

                child4.join()

                child5.join()

                child6.join()

                child7.join()

                child8.join()

                print "No Dice!"

                done = True

            else:

                rec = parentPipe.recv()

                if rec == "found":

                    self.countey = parentPipe.recv()

                    child1.terminate()

                    child2.terminate()

                    child3.terminate()

                    child4.terminate()

                    child5.terminate()

                    child6.terminate()

                    child7.terminate()

                    child8.terminate()

                    done = True

                count += 1

        elapsed = (time() - start)
        print "That took: ", elapsed, " seconds."

        speed = (8 * int(self.countey)) / elapsed

        if rec == "found":

            print "At about: ", speed, " hashes per second."

        exit = raw_input("Hit (Enter/Return) to quit ")


    def subProcess(self, pipe, lock):

        lock.acquire()

        loops = pipe.recv()

        alphabet = pipe.recv()

        lock.release()

        if self.looper6(alphabet) == True:

            lock.acquire()

            pipe.send("found")

            pipe.send(self.countey)

            pipe.close()

            lock. release()

        else:

            lock.acquire()

            pipe.send("not found")

            pipe.close()

            lock. release()


    def chunkIt(self):

        chunky = [self.alphabet[i::8] for i in range(8)]

        self.chunk1 = chunky.pop()

        self.chunk2 = chunky.pop()

        self.chunk3 = chunky.pop()

        self.chunk4 = chunky.pop()

        self.chunk5 = chunky.pop()

        self.chunk6 = chunky.pop()

        self.chunk7 = chunky.pop()

        self.chunk8 = chunky.pop()


    def getHash(self):

        key = raw_input("What's the 6 LowerCase-Letter Key: ")

        self.key = key

        tempKey = hashlib.sha256()

        byteKey = str.encode(key)

        type(byteKey)

        tempKey.update(byteKey)

        self.origHash = tempKey.hexdigest()

        print "The Key you entered was: ", key
        print "Which has a hash of: ", self.origHash


    def whatWeGot(self):

        print "**********************************"
        print "Here's what we've got so far: "
        print
        print "Key is:       ", self.key
        print "Hash is:      ", self.origHash
        print "Searching:    ", self.alphaChoice
        print "**********************************"

    def isSolution(self, key):

        tempKey = hashlib.sha256()

        byteKey = str.encode(key)

        type(byteKey)

        tempKey.update(byteKey)

        possible = tempKey.hexdigest()

        if possible == self.origHash:

            print

            print"Solution found!"

            print "Key is: ", key

            print "Which has a hash of: ", possible

            return True

        else:

            return False


    def looper6(self, alphabet):

        for x in alphabet:

            print "Searching ...", x, "*****"

            for y in self.alphabet:

                for z in self.alphabet:

                    for a in self.alphabet:

                        for b in self.alphabet:

                            for c in self.alphabet:

                                self.countey += 1

                                key = x + y + z + a + b + c

                                if self.isSolution(key):

                                    return True

        return False

DemoCrack()