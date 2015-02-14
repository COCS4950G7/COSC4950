#   Brute_Force.py

#   This class does all the brute force cracking work,
#   interacting only with the controller class.

#   2/11/2015
#   Complete reworking of the previous code. Removed as many unnecessary functions, variables, and operations as I could
#   find. Minor changes to the way chunks are run.  Increased chunk size to a maximum of 100,000,000 hashes, since
#   brute forcing is going to ba a long term computation, it makes sense to minimize network overhead by giving
#   work units that last from a few tens to a couple hundred seconds.

import hashlib
import os
import itertools
import string
from multiprocessing import cpu_count, Process, Queue, Value
import Chunk

from time import time, sleep


class WorkUnit(object):
    def __init__(self, prefix, length, alphabet):
        self.prefix = prefix
        self.length = length
        self.alphabet = alphabet

class Brute_Force():
    minKeyLength = 6
    maxKeyLength = 16
    alphabet = string.ascii_lowercase + string.ascii_uppercase + string.digits #+ string.punctuation
    algorithm = "sha256"
    origHash = ''
    key = ''
    rec = None
    charactersToCheck = 3
    queue = Queue(cpu_count()*5)
    chunk_size = 0
    countey = Value('I', 0)
    done = Value('b', False)
    total_work_units = 0
    possibilities_exhausted = False
    first_unit = True

    def __init__(self):
        if not __name__ == '__main__':
                return
        self.test_me()

    def from_controller(self, alphabet, algorithm, origHash, min_key_length, max_key_length):
        self.alphabet = alphabet
        self.algorithm = algorithm
        self.origHash = origHash
        self.minKeyLength = min_key_length
        self.maxKeyLength = max_key_length
        self.set_chars_to_check()

    def resetVariables(self):
        self.minKeyLength = 1
        self.maxKeyLength = 16
        self.alphabet = string.ascii_lowercase + string.ascii_uppercase + string.digits #+ string.punctuation
        self.algorithm = "sha256"
        self.origHash = ''
        self.key = ''
        self.rec = None
        self.charactersToCheck = 3
        self.queue = Queue(cpu_count()*10)
        self.chunk_size = 0
        self.countey = Value('I', 0)
        self.done = Value('b', False)
        self.total_work_units = 0
        self.possibilities_exhausted = False
        self.first_unit = True

    def isFound(self):
        return self.done.value

    def returnKey(self):
        return self.key

    def possibilitiesEhausted(self):
        return self.possibilities_exhausted

    def terminate_processes(self, children):
        for process in children:
            process.terminate()

    def check_short_keys(self):
        if self.done.value:
            return
        print "check_short_keys called for lengths %d-%d and no prefix." % (self.minKeyLength, self.charactersToCheck)

        keylist = itertools.chain.from_iterable(itertools.product(self.alphabet, repeat=j) for j in range(self.minKeyLength-1, self.charactersToCheck+1))
        for key in keylist:
            tempkey = ''.join(key)
            if self.isSolution(tempkey):
                while not self.queue.empty():
                    self.queue.get()
                self.countey.value += 1
                print "We win!"
                return True
            self.countey.value += 1
        return False

    def check_keys(self):
        while self.queue:
            if self.done.value:
                return
            workunit = self.queue.get()
            length = workunit.length + workunit.prefix.__len__()

            print "check_keys called for length %d and the prefix %s" % (length, ''.join(workunit.prefix))

            prefix = ''.join(workunit.prefix)
            keylist = itertools.chain.from_iterable(itertools.product(self.alphabet, repeat=(workunit.length)))

            for key in keylist:
                tempkey = prefix + ''.join(workunit.prefix)
                if self.isSolution(tempkey):
                    while not self.queue.empty():
                        self.queue.get()
                    self.countey.value += 1
                    print "We win!"
                    return True
            self.countey.value += 1
        return False

#   get_prefix() is an iterator which produces all possible prefixes of appropriate length
#   as defined by min/max key lengths and charactersToCheck
    def get_prefix(self):
        if self.minKeyLength < self.charactersToCheck:
            yield ''
        for i in range(self.charactersToCheck-1, self.maxKeyLength-self.charactersToCheck+1):
            prefixes = itertools.chain.from_iterable(itertools.product(self.alphabet, repeat=j)for j in range(i, i+1))
            for prefix in prefixes:
                yield ''.join(prefix)

#   Hash a possible key and check if it is equal to the hashed input.
    def isSolution(self, key):
        temp_key = hashlib.new(self.algorithm, key).hexdigest()
        if temp_key == self.origHash:
            self.rec = "found"
            print "Solution found!\nKey is : %s\nWith a hash of %s" % (key, temp_key)
            with self.done._lock:
                self.done.value = True
            self.key = key
            return True
        else:
            return False

#   setup here is to make chunks large enough that constant network communications are avoided but that won't last
#   forever on slower machines. A maximum chunk size of 100M hashes seemed a reasonable compromise.
    def set_chars_to_check(self):
        self.charactersToCheck = 1
        iterations = self.alphabet.__len__()
        while True:
            iterations *= self.alphabet.__len__()
            self.charactersToCheck += 1
            if iterations > 100000000:
                self.charactersToCheck -= 1
                iterations /= self.alphabet.__len__()
                break
        print "Checking ", self.charactersToCheck, "characters per chunk."
        self.chunk_size = iterations
        for i in range(self.minKeyLength, self.maxKeyLength):
            self.total_work_units += ((self.alphabet.__len__() ^ i)/self.chunk_size)

#   get_chunk() is an iterator which yields a new chunk of data each time it is called.
    def get_chunk(self):
        for prefix in self.get_prefix():
            print "get chunk prefix: %s" % prefix
            if prefix == '':
                prefix = "-99999999999999999999999999999999999"
                min_length = self.minKeyLength
                if self.charactersToCheck > self.maxKeyLength:
                    max_length = self.maxKeyLength
                else:
                    max_length = self.charactersToCheck
            else:
                min_length = len(prefix) + self.charactersToCheck-1
                max_length = min_length
            chunk = Chunk.Chunk()
            chunk.params = "bruteforce\n" + self.algorithm + "\n" + self.origHash + "\n" + self.alphabet + "\n" + str(min_length) + "\n" + str(max_length) + "\n" + prefix + "\n0\n0\n0"
            yield chunk
        self.possibilities_exhausted = True

#   run_chunk takes an object of type Chunk.Chunk(), checks all possibilities within the parameters of the chunk,
#   sets global variables according to the chunk data and returns True or False to indicate if the cracking succeeded.
    def run_chunk(self, chunk):
        settings = chunk.params
        settings_list = settings.split()
        self.algorithm = settings_list[1]
        self.origHash = settings_list[2]
        self.alphabet = settings_list[3]
        self.minKeyLength = int(settings_list[4])
        self.maxKeyLength = int(settings_list[5])
        prefix = settings_list[6]
        self.set_chars_to_check()
        self.charactersToCheck -= 1
        children = []
        alphabet = self.alphabet
        print "run chunk prefix: %s" % prefix
        if prefix == "-99999999999999999999999999999999999":
            prefix = ''
            self.check_short_keys()
        else:
            for j in range(0, cpu_count()):
                children.append(Process(target=self.check_keys))
                children[j].start()
            for letter in alphabet:
                if self.done.value:
                    while not self.queue.empty():
                        self.queue.get()
                    self.queue.close()
                    self.terminate_processes(children)
                    return
                else:
                    pref = prefix
                    pref.join(letter)
                    self.queue.put(WorkUnit(pref, self.charactersToCheck-1, self.alphabet))

            #wait while we burn through any remaining queue
            while self.queue:
                if self.done.value:
                    break

            self.queue.close()
            self.terminate_processes(children)

        if self.done:
            return True
        else:
            return False

#   This method tests the operation of the chunking and cracking methods.
    def test_me(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        self.what_we_got()
        key = raw_input("Enter a key from %d to %d characters: " % (self.minKeyLength, self.maxKeyLength))
        self.key = key
        self.origHash = hashlib.new(self.algorithm, key).hexdigest()
        print "The Key you entered was: ", key
        print "Which has a hash of: ", self.origHash
        os.system('cls' if os.name == 'nt' else 'clear')
        self.what_we_got()

        self.set_chars_to_check()
        self.done.value = False
        start = time()
        while not self.done.value and not self.possibilities_exhausted:
            chunk = self.get_chunk().next()
            print "\n\nData from chunk:"
            settings = chunk.params
            settings_list = settings.split()
            self.algorithm = settings_list[1]
            print "Algorithm: " + self.algorithm
            self.origHash = settings_list[2]
            print "Hash: " + self.origHash
            self.alphabet = settings_list[3]
            print "Alphabet: " + self.alphabet
            self.minKeyLength = int(settings_list[4])
            self.maxKeyLength = int(settings_list[5])
            print "Checking keys from " + str(self.minKeyLength) + " to " + str(self.maxKeyLength) + " characters."
            prefix = settings_list[6]
            print "Prefix: " + prefix
            self.run_chunk(chunk)

        finish = time()
        speed = self.chunk_size / (finish - start)

        print "That took: %d seconds." %((finish - start))
        print "At about: %d hashes per second." % speed

    def what_we_got(self):

        print "**********************************"
        print "Here's what we've got so far: "
        print
        print "Key is:       ", self.key
        print "Hash is:      ", self.origHash
        print "Searching:    ", self.alphabet
        print "**********************************"

if __name__ == '__main__':
    bf = Brute_Force()
    bf