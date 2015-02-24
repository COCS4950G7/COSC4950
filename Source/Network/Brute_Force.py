#   Brute_Force.py

#   This class does all the brute force cracking work,
#   interacting only with the controller class.

#   2/11/2015
#   Complete reworking of the previous code. Removed as many unnecessary functions, variables, and operations as I could
#   find. Minor changes to the way chunks are run.  Increased chunk size to a maximum of 100,000,000 hashes, since
#   brute forcing is going to ba a long term computation, it makes sense to minimize network overhead by giving
#   work units that last from a few tens to a couple hundred seconds.

#   2/23/2015
#   Removed internal get_chunk() method as chunking has moved into server to resolve a major issue. Removed internal
#   testing method as this class should never be run directly anymore. Changed the name of from_controller to set_params
#   to better reflect the new program structure. Added start_processes() method to start a global pool of processes
#   which are fed by the internal queue. Changed run_chunk to simply add the chunk to the queue. This should improve
#   efficiency of parallel processing with the new network client functionality by minimizing downtime and overhead.

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
    algorithm = "md5"
    origHash = '12c8de03d4562ba9f810e7e1e7c6fc15'
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
    children = []

    def __init__(self):
        if not __name__ == '__main__':
                return

    def set_params(self, alphabet, algorithm, origHash, min_key_length, max_key_length):
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
        self.origHash = '12c8de03d4562ba9f810e7e1e7c6fc15'
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

    def start_processes(self):
        for j in range(0, cpu_count()):
            self.children.append(Process(target=self.check_keys))
            self.children[j].start()

    def terminate_processes(self):
        for process in self.children:
            process.terminate()

    def check_short_keys(self):
        if self.done.value:
            return
        print "check_short_keys called for lengths %d-%d and no prefix." % (self.minKeyLength, self.charactersToCheck)

        keylist = itertools.chain.from_iterable(itertools.product(self.alphabet, repeat=j)
                                                for j in range(self.minKeyLength, self.charactersToCheck+1))
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
            keylist = itertools.product(self.alphabet, repeat=(self.charactersToCheck))

            for key in keylist:
                tempkey = prefix + ''.join(key)
                #print tempkey
                if self.isSolution(tempkey):
                    while not self.queue.empty():
                        self.queue.get()
                    self.countey.value += 1
                    self.queue.close()
                    print "We win!"
                    return True
            self.countey.value += 1
        return False

#   get_prefix() is an iterator which produces all possible prefixes of appropriate length
#   as defined by min/max key lengths and charactersToCheck
    def get_prefix(self):
        if self.minKeyLength < self.charactersToCheck:
            yield ''
        if self.minKeyLength < self.charactersToCheck:
            min_length = self.charactersToCheck
        else:
            min_length = self.minKeyLength-self.charactersToCheck
        for i in range(1, (self.maxKeyLength - self.charactersToCheck + 1)):
            prefixes = itertools.chain.from_iterable(itertools.product(self.alphabet, repeat=j)for j in range(i, i+1))
            for prefix in prefixes:
                if self.done.value:
                    return
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
            if iterations > 10000000:
                self.charactersToCheck -= 1
                iterations /= self.alphabet.__len__()
                break
        print "Checking ", self.charactersToCheck, "characters per chunk."
        self.chunk_size = iterations
        for i in range(self.minKeyLength, self.maxKeyLength):
            self.total_work_units += ((self.alphabet.__len__() ^ i)/self.chunk_size)

#   get_chunk() is an iterator which yields a new chunk of data each time get_chunk.next() is called.
        # BROKEN, DO NOT USE!
    # def get_chunk(self):
    # 
    #     for prefix in self.get_prefix():
    # 
    #         print "get chunk prefix: %s" % prefix
    #         if prefix == '':
    #             prefix = "-99999999999999999999999999999999999"
    # 
    #         chunk = Chunk.Chunk()
    #         chunk.params = "bruteforce\n" + self.algorithm + "\n" + self.origHash + "\n" + self.alphabet + "\n" + str(self.minKeyLength) + "\n" + str(self.maxKeyLength) + "\n" + prefix + "\n0\n0\n0"
    # 
    #         yield chunk
    #     self.possibilities_exhausted = True

#   run_chunk takes an object of type Chunk.Chunk(), checks all possibilities within the parameters of the chunk,
#   sets global variables according to the chunk data and returns True or False to indicate if the cracking succeeded.
    def run_chunk(self, chunk):
        settings = chunk.params
        settings_list = settings.split()
        self.algorithm = settings_list[1]
        self.origHash = settings_list[2]
        self.alphabet = settings_list[3]

        prefix = settings_list[6]

        alphabet = self.alphabet
        if prefix == "-99999999999999999999999999999999999":
            prefix = ''
        if prefix == '' and self.first_unit:
            self.first_unit = False
            self.check_short_keys()
        else:

            if self.done.value:
                return True
            else:
                print "run chunk prefix: %s" % prefix

                self.queue.put(WorkUnit(prefix, self.charactersToCheck, self.alphabet))

        if self.done:
            return True
        else:
            return False


    def what_we_got(self):

        print "**********************************"
        print "Here's what we've got so far: "
        print
        print "Key is:       ", self.key
        print "Hash is:      ", self.origHash
        print "Searching:    ", self.alphabet
        print "**********************************"
