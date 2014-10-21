#   Brute_Force.py

#   This class does all the Brute Forcing work,
#   interacting with the Controller class.

#   Reworked the original, using an iterable instead of manual loops has
#   resulted in about an 8x speedup on my machine. Additionally, it will now check
#   a range of key lengths as set by max/minKeyLength. Also, added some simple
#   if statements to support changing hashing algorithms through the algorithm variable.

#   Update: 10/21/14
#       Changed time estimate line and saw 1/3 slow-down on my machine (vs demo3)...-CJB

#   Nick Baum
#   Chris Bugg
#   10/7/14

import hashlib
import os
import itertools
import string
from multiprocessing import Pool
from time import time

minKeyLength = 6
maxKeyLength = 16
alphabet = string.ascii_lowercase + string.ascii_uppercase + string.digits #+ string.punctuation
done = False


class Brute_Force():

    algorithm = "sha256"
    origHash = ''
    key = ''
    rec = None
    countey = 0

    def __init__(self):

        if not __name__ == '__main__':

                return

        os.system('cls' if os.name == 'nt' else 'clear')
        self.whatWeGot()

        self.getHash()

        os.system('cls' if os.name == 'nt' else 'clear')
        self.whatWeGot()

        keygen = itertools.chain.from_iterable(itertools.product(alphabet, repeat=i)
                 for i in range(minKeyLength, maxKeyLength + 1))
        #threadPool = Pool()

        start = time()

        self.checkKeys(keygen)

        finish = time()
        #threadPool.close()
        #threadPool.join()
        elapsed = (finish - start)
        print "That took: ", elapsed, " seconds."

        #This line needs to be changed to reflect the number of processes running
        speed = (1 * int(self.countey)) / elapsed

        if self.rec == "found":

            print "At about: ", speed, " hashes per second."
        else:
            print "No bounce no play."

        exit = raw_input("Hit (Enter/Return) to quit ")


    def checkKeys(self, keygen):
        for aKey in keygen:
            self.countey += 1
            #print ''.join(aKey)
            if self.isSolution(''.join(aKey)):
                self.rec = "found"

                return True

    def getHash(self):

        key = raw_input("Enter a key from 4 to 16 characters: ")

        self.key = key

        if self.algorithm == "sha1":
            tempKey = hashlib.sha1()
        elif self.algorithm == "sha224":
            tempKey = hashlib.sha224()
        elif self.algorithm == "sha256":
            tempKey = hashlib.sha256()
        elif self.algorithm == "sha384":
            tempKey = hashlib.sha384()
        elif self.algorithm == "sha512":
            tempKey = hashlib.sha512()
        elif self.algorithm == "md5":
            tempKey = hashlib.md5()

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
        print "Searching:    ", alphabet
        print "**********************************"

    def isSolution(self, key):

        if self.algorithm == "sha1":
            tempKey = hashlib.sha1()
        elif self.algorithm == "sha224":
            tempKey = hashlib.sha224()
        elif self.algorithm == "sha256":
            tempKey = hashlib.sha256()
        elif self.algorithm == "sha384":
            tempKey = hashlib.sha384()
        elif self.algorithm == "sha512":
            tempKey = hashlib.sha512()
        elif self.algorithm == "md5":
            tempKey = hashlib.md5()

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


Brute_Force()