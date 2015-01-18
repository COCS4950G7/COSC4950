#   Brute_Force.py

#   This class does all the Brute Forcing work,
#   interacting with the Controller class.

#   1/12/2015
#   Extracted prefix generation to get_prefix() and generalized it so the calling the get_prefix().next() method will
#   yield a prefix compatible with either the crack_it or the get_chunk methods.
#   Added get_chunk() method to generate an object of type Chunk to pass across the network.
#   Added run_chunk() method to start cracking based on data from a passed Chunk object.
#   Some oddities in run_chunk() still, basically works, but not finished.
#   Added tedt_chunking() method to implement tests of get_chunk and run_chunk.

#   In order to allow for the use of a space as an input I changed from a space separating fields in my use of Chunk to
#   newline characters '/n'.

#   Leaving this in latest stable despite the only semi-functional nature of the new methods because the methods
#   previously available still work as they did before.

#   These two methods are preliminary versions and at the moment multiprocessing is not available. I am working out
#   a good way to chunk out work to network clients. There are really two choices, send many chunks and  each one is
#   added to the queue on the client up to a total of, say, three times as many chunks as processors on the client.
#   This would seem to be a good choice since it has some built in calibration based on machine capabilities. The other
#   option would be to send much larger chunks, check the prefix over charsToCheck+1 which would be the equivalent of
#   sending as many chunks as there are characters in the alphabet. This could be ten minutes or more for slower systems
#   and/or large alphabets. on the other hand, it requires less code modification.

#   Nick Baum


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
    num_processes = cpu_count()
    algorithm = "sha256"
    origHash = ''
    key = ''
    rec = None
    charactersToCheck = 1
    queue = Queue(num_processes*5)
    speed = 0
    elapsed = 0
    chunk_size = 0
    countey = Value('I', 0)
    done = Value('b', False)
    total_work_units = 0


    def __init__(self):
        if not __name__ == '__main__':
                return

        #print num_processes, " processes"
        self.commandline()
        #self.test_chunking("aaa999")

    def command_line_demo(self):
        self.commandline()

    def from_controller(self, alphabet, algorithm, origHash, min_key_length, max_key_length):
        self.alphabet = alphabet
        self.algorithm = algorithm
        self.origHash = origHash
        self.minKeyLength = min_key_length
        self.maxKeyLength = max_key_length
        self.set_chars_to_check()
        self.run()

    def get_chunk(self):

        #"method algorithm hash alphabetChoice minCharacters maxCharacters prefix fileLocation width height"
        #"bruteforce sha1 7cacb75c4cc31d62a6c2a0774cf3c41a70f01bc0 d 1 12 1234 0 0 0"
        for prefix in self.get_prefix():
            if len(prefix) == 0:
                min_length = self.minKeyLength
                max_length = self.charactersToCheck
            else:
                min_length = len(prefix) + self.charactersToCheck
                max_length = min_length
            chunk = Chunk.Chunk()
            chunk.params = "bruteforce\n" + self.algorithm + "\n" + self.origHash + "\n" + self.alphabet + "\n" + str(min_length) + "\n" + str(max_length) + "\n" + prefix + "\n0\n0\n0"
            yield chunk

    def run_chunk(self, chunk):
        #"method algorithm hash alphabetChoice minCharacters maxCharacters prefix fileLocation width height"
        #"bruteforce sha1 7cacb75c4cc31d62a6c2a0774cf3c41a70f01bc0 d 1 12 1234 0 0 0"
        settings = chunk.params
        settings_list = settings.split()
        self.algorithm = settings_list[1]
        self.origHash = settings_list[2]
        self.alphabet = settings_list[3]
        self.minKeyLength = int(settings_list[4])
        self.maxKeyLength = int(settings_list[5])
        prefix = settings_list[6]
        self.charactersToCheck = (self.charactersToCheck-1)

        children = []
        for j in range(0, self.num_processes):
            children.append(Process(target=self.check_keys, args=(self.queue, self.countey, self.done)))
            children[j].start()
        for letter in self.alphabet:
            if self.done.value:
                    while not self.queue.empty():
                        self.queue.get()
                    self.queue.close()
                    self.terminate_processes(children)
                    return
            self.queue.put(WorkUnit(prefix+letter, len(prefix)-1, self.alphabet))
            with self.done.get_lock():
                if self.done.value:
                    while not self.queue.empty():
                        self.queue.get()
                    self.queue.close()
                    self.terminate_processes(children)
                    return

        #wait while we burn through the remaining queue
        while self.queue:
            if self.done.value:
                break

        self.queue.close()
        self.terminate_processes(children)

        if self.done:
            return self.key
        else:
            return "fail"



    def test_chunking(self, testkey):
        os.system('cls' if os.name == 'nt' else 'clear')
        self.what_we_got()
        self.get_hash()

        os.system('cls' if os.name == 'nt' else 'clear')
        self.what_we_got()

        self.set_chars_to_check()

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

        print "That took: ", self.elapsed, " seconds."
        self.speed = (self.countey.value * self.chunk_size)/self.elapsed
        print "At about: ", self.speed, " hashes per second."

        if self.done.value:
            return self.key
        else:
            print "You lose."

        exit()

    def get_prefix(self):
        if self.minKeyLength - self.charactersToCheck < 0:
            starting_length = self.charactersToCheck
        else:
            starting_length = self.minKeyLength - self.charactersToCheck
        for i in range(starting_length, (self.maxKeyLength - self.charactersToCheck + 1)):
            prefixes = itertools.chain.from_iterable(itertools.product(self.alphabet, repeat=j)for j in range(i, i+1))
            for prefix in prefixes:
                yield ''.join(prefix)


    def set_chars_to_check(self):
        self.charactersToCheck = 1
        iterations = self.alphabet.__len__()
        while True:
            iterations *= self.alphabet.__len__()
            self.charactersToCheck += 1
            if iterations > 2000000:
                self.charactersToCheck -= 1
                iterations /= self.alphabet.__len__()
                break
        print "Checking ", self.charactersToCheck, "characters per chunk."
        self.chunk_size = iterations
        for i in range(self.minKeyLength, self.maxKeyLength):
            self.total_work_units += ((self.alphabet.__len__() ^ i)/self.chunk_size)

    def crack_it(self):
        children = []
        for j in range(0, self.num_processes):
            children.append(Process(target=self.check_keys, args=(self.queue, self.countey, self.done)))
            children[j].start()

        #this may disappear, why even implement passwords that short?
        if self.minKeyLength < self.charactersToCheck:
            for i in range(self.minKeyLength, self.charactersToCheck+1):
                self.queue.put(WorkUnit('', i, self.alphabet))

        """
        print "Starting length = %d" % starting_length
        for i in range(starting_length, (self.maxKeyLength - self.charactersToCheck + 1)):
            prefixes = itertools.chain.from_iterable(itertools.product(self.alphabet, repeat=j)for j in range(i, i+1))
            print "starting process for key length ", i + self.charactersToCheck
            for prefix in prefixes:
                if self.done.value:
                    while not self.queue.empty():
                        self.queue.get()
                    self.queue.close()
                    self.terminate_processes(children)
                    return
                self.queue.put(WorkUnit(prefix, i, self.alphabet))
            with self.done.get_lock():
                if self.done.value:
                    while not self.queue.empty():
                        self.queue.get()
                    self.queue.close()
                    self.terminate_processes(children)
                    return
        """

        for prefix in self.get_prefix():
            if self.done.value:
                    while not self.queue.empty():
                        self.queue.get()
                    self.queue.close()
                    self.terminate_processes(children)
                    return
            self.queue.put(WorkUnit(prefix, len(prefix), self.alphabet))
            with self.done.get_lock():
                if self.done.value:
                    while not self.queue.empty():
                        self.queue.get()
                    self.queue.close()
                    self.terminate_processes(children)
                    return


        #wait while we burn through the remaining queue
        while self.queue:
            if self.done.value:
                break

        self.queue.close()
        self.terminate_processes(children)

        return

    def terminate_processes(self, children):
        for process in children:
            process.terminate()

    def check_keys(self, queue, countey, done):

        while queue:
            if done.value:
                return
            workunit = queue.get()
            length = workunit.length+workunit.prefix.__len__()
            print "checkKeys called for length %d and the prefix %s" % (length, ''.join(workunit.prefix))

            #support for 1 or 2 char keys is broken for now, maybe forever, who allows passwords so short?
            if length < self.charactersToCheck:
                keysize = length
            else:
                keysize = self.charactersToCheck

            prefix = ''.join(workunit.prefix)
            keylist = itertools.product(self.alphabet, repeat=keysize)
            for key in keylist:
                tempkey = prefix + ''.join(key)
                if self.is_solution(tempkey):
                    done.value = True
                    self.key = tempkey
                    while not queue.empty():
                        queue.get()
                    with self.countey.get_lock():
                        countey.value += 1
                    print "We win!"

                    return True
            with self.countey.get_lock():
                countey.value += 1
        return None

    def get_hash(self):

        key = raw_input("Enter a key from %d to %d characters: " % (self.minKeyLength, self.maxKeyLength))
        self.key = key

        self.origHash = hashlib.new(self.algorithm, key).hexdigest()

        print "The Key you entered was: ", key
        print "Which has a hash of: ", self.origHash

    def what_we_got(self):

        print "**********************************"
        print "Here's what we've got so far: "
        print
        print "Key is:       ", self.key
        print "Hash is:      ", self.origHash
        print "Searching:    ", self.alphabet
        print "**********************************"

    def is_solution(self, key):

        temp_key = hashlib.new(self.algorithm, key).hexdigest()
        if temp_key == self.origHash:

            print

            print "Solution found!"
            print "Key is: ", key
            print "Which has a hash of: ", temp_key
            self.rec = 'found'
            return True

        else:

            return False

    def run(self):
        start = time()
        self.crack_it()
        finish = time()

        self.elapsed = (finish - start)

        self.speed = (self.countey.value * self.chunk_size)/self.elapsed

        return self.key

    def commandline(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        self.what_we_got()
        self.get_hash()

        os.system('cls' if os.name == 'nt' else 'clear')
        self.what_we_got()

        self.set_chars_to_check()

        self.run()

        print "That took: ", self.elapsed, " seconds."
        self.speed = (self.countey.value * self.chunk_size)/self.elapsed
        print "At about: ", self.speed, " hashes per second."

        if self.done.value:
            return self.key
        else:
            print "You lose."

        exit()



if __name__ == '__main__':
    bf = Brute_Force()
    bf