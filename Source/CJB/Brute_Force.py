#   Brute_Force.py

#   This class does all the Brute Forcing work,
#   interacting with the Controller class.

#   Reworked the original, multiprocessing is disabled while I learn to use pools.
#   Additionally, it will now check a range of
#   key lengths as set by max/minKeyLength.

#   Tried a new, more concise way of getting hashes which was only intended to allow
#   for easy algorithm selection, but unexpectedly caused a significant speed increase.
#   Applied it to demoCrack3 as well and got a more modest speed increase, but this code
#   now runs at about the same single core speed as demoCrack3

#   10/23 Nick Baum


import hashlib
import os
import itertools
import string
from multiprocessing import Pool, cpu_count
from time import time

minKeyLength = 6
maxKeyLength = 6
alphabet = string.ascii_lowercase + string.ascii_uppercase + string.digits #+ string.punctuation
done = False


class Brute_Force():

    algorithm = "sha256"
    origHash = ''
    key = ''
    rec = None
    countey = 0
    threadPool = Pool()


    def __init__(self):

        if not __name__ == '__main__':

                return

        self.main()

    def main(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        self.whatWeGot()

        self.getHash()

        os.system('cls' if os.name == 'nt' else 'clear')
        self.whatWeGot()

        start = time()
        try:
            self.crackit()
            #for chunk in self.keygen():
                #self.checkKeys(chunk)
                #self.threadPool.apply_async(self.checkKeys, chunk)

        except Exception as e:
            if e == 'done':
                self.threadPool.terminate()


        finish = time()
        self.threadPool.close()
        self.threadPool.terminate()
        self.threadPool.join()
        elapsed = (finish - start)
        print "That took: ", elapsed, " seconds."

        speed = self.countey / elapsed

        if self.rec == "found":

            print "At about: ", speed, " hashes per second."
            return self.key
        else:
            print "No bounce no play."

        exit = raw_input("Hit (Enter/Return) to quit ")

    def checkKeys(self, keylist):
        for key in keylist:
            if self.isSolution(''.join(key)):
                self.rec = 'found'
                #raise Exception('done')
                return True

    def keygen(self):

        it = itertools.chain.from_iterable(itertools.product(alphabet, repeat=i)
                for i in range(minKeyLength, maxKeyLength + 1))

        def take():
            while True:
                yield itertools.islice(it, 100000)

        return take().next()

    def getHash(self):

        key = raw_input("Enter a key from 4 to 16 characters: ")
        self.key = key
        self.origHash = hashlib.new(self.algorithm, key).hexdigest()


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

    def crackit(self):
        it = itertools.chain.from_iterable(itertools.product(alphabet, repeat=i)
                        for i in range(minKeyLength, maxKeyLength + 1))
        #for chunk in itertools.islice(it, 100000):
        self.checkKeys(it)
        #self.threadPool.map_async(self.isSolution, it, 100000)
        self.threadPool.close()
        self.threadPool.terminate()
        self.threadPool.join()


    def isSolution(self, key):

        tempKey = hashlib.new(self.algorithm, key).hexdigest()
        self.countey += 1
        if tempKey == self.origHash:

            print

            print "Solution found!"
            print "Key is: ", key
            print "Which has a hash of: ", tempKey
            #raise Exception('done')
            self.rec = 'found'
            return True

        else:

            return False


Brute_Force()