#   Brute_Force.py

#   This class does all the brute force cracking work,
#   interacting only with the controller class.

#from passlib.context import CryptContext
#import passlib
import hashlib
import itertools
import string
import time
from multiprocessing import cpu_count, Process, Queue, Value, current_process


class WorkUnit(object):
    def __init__(self, prefix, length, alphabet, algorithm, hash):
        self.prefix = prefix
        self.length = length
        self.alphabet = alphabet
        self.algorithm = algorithm
        self.hash = hash


class Brute_Force():
    minKeyLength = 6
    maxKeyLength = 16
    alphabet = string.ascii_lowercase + string.ascii_uppercase + string.digits #+ string.punctuation
    algorithm = None
    origHash = None
    key = ''
    rec = None
    charactersToCheck = 3
    queue = Queue(cpu_count()*5)
    chunk_size = 0
    countey = Value('I', 0)
    done = Value('b', False)
    total_work_units = 1
    possibilities_exhausted = False
    first_unit = True
    children = []
    result_queue = None
    processes_running = False
    #myctx = CryptContext(schemes=["sha1_crypt", "sha256_crypt", "sha512_crypt", "md5_crypt",
     #                             "des_crypt", 'ldap_salted_sha1', 'ldap_salted_md5',
      #                            'ldap_sha1', 'ldap_md5', 'ldap_plaintext', "mysql323"])

    def __init__(self):
        if not __name__ == '__main__':
            return
        current_process().authkey = "Popcorn is awesome!!!"

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
        self.alphabet = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation
        self.algorithm = ""
        self.origHash = ''
        self.key = ''
        self.rec = None
        self.charactersToCheck = 3
        self.queue = Queue(cpu_count()*5)
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

    def set_result_queue(self, result_queue):
        self.result_queue = result_queue

    def get_total_chunks(self):
        return self.total_work_units

    # start pool of check_keys workers
    def start_processes(self):
        if not self.processes_running:
            for j in range(0, cpu_count()):
                self.children.append(Process(target=self.check_keys, args=(self.queue,)))
                self.children[j].start()
                #print "bf internal process %i started." % self.children[j].pid
            self.processes_running = True

    # shutdown process pool
    def terminate_processes(self):
        for process in self.children:
            #print "killing process: %i" % process.pid
            process.terminate()
            process.join(timeout=.1)
            #if process.is_alive():
             #   print "process %i did not die." % process.pid

    # checks keys of length minKeyLength to charsToCheck, these keys will not use a prefix
    def check_short_keys(self):
        if self.done.value:
            return
        #print "check_short_keys called for lengths %d-%d and no prefix." % (self.minKeyLength, self.charactersToCheck)
        # compound iterable creates strings with a range of lengths
        keylist = itertools.chain.from_iterable(itertools.product(self.alphabet, repeat=j)
                                                for j in range(self.minKeyLength, self.charactersToCheck+1))
        for key in keylist:
            tempkey = ''.join(key)
            if self.isSolution(tempkey):
                self.result_queue.put(('w', tempkey))
                while not self.queue.empty():
                    self.queue.get()
                self.countey.value += 1
                #print "We win!"
                return True
            self.countey.value += 1
        params = "bruteforce\n" + self.algorithm + "\n" + self.origHash + "\n" + self.alphabet + "\n" \
                 + str(self.minKeyLength) + "\n" + str(self.maxKeyLength) + "\n" \
                 + "-99999999999999999999999999999999999" + "\n0\n0\n0"
        self.result_queue.put(('f', params))
        return False

    # take prefixes from the job queue and iterate through the possibilities for keys starting with that prefix
    def check_keys(self, queue):
        while queue:
            if self.done.value:
                return
            # get a workunit off the queue
            workunit = queue.get()
            if workunit.prefix == "******possibilities exhausted******":
                time.sleep(10)
                self.result_queue.put(('e', "sadness"))
            self.algorithm = workunit.algorithm
            self.origHash = workunit.hash
            prefix = ''.join(workunit.prefix)
            #create an iterable to produce suffixes to append to the prefix
            keylist = itertools.product(self.alphabet, repeat=self.charactersToCheck)
            # check possibilities until iterable is consumed
            for key in keylist:
                tempkey = prefix + ''.join(key)
                #print tempkey
                if self.isSolution(tempkey):
                    try:
                        # send key with success message
                        self.result_queue.put(('w', tempkey), timeout=1)
                    except Exception:
                        return
                    while not self.queue.empty():
                        queue.get()
                    self.countey.value += 1
                    queue.close()
                    #print "We win!"
                    return True
            self.countey.value += 1
            # send back parameters with a fail result
            params = "bruteforce\n" + self.algorithm + "\n" + self.origHash + "\n" + self.alphabet + "\n" \
                     + str(self.minKeyLength) + "\n" + str(self.maxKeyLength) + "\n" + prefix + "\n0\n0\n0"
            self.result_queue.put(('f', params))

        return False

#   get_prefix() is an iterator which produces all possible prefixes of appropriate length
#   as defined by min/max key lengths and charactersToCheck
    def get_prefix(self):
        if self.minKeyLength < self.charactersToCheck:
            yield ''
        if self.minKeyLength < self.charactersToCheck:
            # all keys up to charsToCheck will be handled by check_short_keys, so start with 1 char prefixes
            min_length = 1
        else:
            min_length = self.minKeyLength-self.charactersToCheck
        for i in range(min_length, (self.maxKeyLength - self.charactersToCheck + 1)):
            prefixes = itertools.chain.from_iterable(itertools.product(self.alphabet, repeat=j)for j in range(i, i+1))
            for prefix in prefixes:
                if self.done.value:
                    return
                yield ''.join(prefix)
        yield "******possibilities exhausted******"

#   Hash a possible key and check if it is equal to the hashed input.
    def isSolution(self, key):
        temp_key = hashlib.new(self.algorithm, key).hexdigest()
        if temp_key == self.origHash:
            self.rec = "found"
            #print "Solution found!\nKey is : %s\nWith a hash of %s" % (key, temp_key)
            with self.done.get_lock():
                self.done.value = True
            self.key = key
            return True
        else:
            return False

    # experimental method designed to work with passlib hashing library, not for normal use
    def isSolution2(self, key):
        if self.myctx.verify(key, self.origHash):
            #print "Solution found!\nKey is : %s\nWith a hash of %s" % (key, self.origHash)
            self.done.value = True
            self.key = key
            return True
        else:
            return False

#   setup here is to make chunks large enough that constant network communications are avoided but that won't last
#   forever on slower machines. A maximum chunk size of 10M hashes seemed a reasonable compromise.
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
        # calculate chunk size and total number of chunks
        self.chunk_size = self.alphabet.__len__() ** self.charactersToCheck
        for i in range(self.minKeyLength, self.maxKeyLength+1):
            self.total_work_units += ((self.alphabet.__len__() ** i)/self.chunk_size)

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
        settings_list = settings.split('\n')
        #print settings
        prefix = settings_list[6]
        if self.first_unit:
            self.algorithm = settings_list[1]
            self.origHash = settings_list[2]
            self.alphabet = settings_list[3]
            self.minKeyLength = int(settings_list[4])
            self.maxKeyLength = int(settings_list[5])
            self.set_chars_to_check()

        if prefix == "-99999999999999999999999999999999999":
            prefix = ''
        if prefix == '' and self.first_unit:

            shorts = Process(target=self.check_short_keys)
            shorts.start()
            #shorts.join()
            #shorts.terminate()
            #print "short keys started"
        else:
            if self.done.value:
                return True
            else:
                #print "run chunk prefix: %s" % prefix
                self.queue.put(WorkUnit(prefix, self.charactersToCheck, self.alphabet, self.algorithm, self.origHash))

        self.first_unit = False
        if self.done:
            return True
        else:
            return False
