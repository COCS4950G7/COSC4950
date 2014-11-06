#   Brute_Force.py

#   This class does all the Brute Forcing work,
#   interacting with the Controller class.

#   11/5/2014
#   Rebuilt to check smaller chunks fed to a queue, added a WorkUnit class as a container for whatever information needs
#   to be passed. Used a similar method of mutiprocessing to the one I added to demoCrack3, automatically creates the
#   right number of processes for the available processes. Using synchronized, shared variables to update counts and
#   end computation when solution is found. Also, it is currently broken for key lengths shorter than 5; finds the
#   solution but never terminates and the time and speed calculations fail.
#   Also added simple methods to allow the class to be called from other sources (ie. a controller) and set class
#   variables without direct user input. These methods are more or less untested. Lots of terminal spam at the moment.

#   Nick Baum


import hashlib
import os
import itertools
import string
from multiprocessing import cpu_count, Pipe, Process, Lock, Queue, Value

from time import time

# minKeyLength must be greater than 3
minKeyLength = 6
maxKeyLength = 16
alphabet = string.ascii_lowercase + string.ascii_uppercase + string.digits #+ string.punctuation
num_processes = cpu_count()


class WorkUnit(object):
    def __init__(self, prefix, length):
        self.prefix = prefix
        self.length = length


class Brute_Force():

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

    def __init__(self):
        if not __name__ == '__main__':
                return

        #print num_processes, " processes"
        self.commandline()

    def command_line_demo(self):
        self.commandline()

    def from_controller(self, alphabet, algorithm, origHash):
        self.alphabet = alphabet
        self.algorithm = algorithm
        self.origHash = origHash
        self.set_chars_to_check()

        return self

    def from_controller_demo(self, alphabet, algorithm, key):
        self.alphabet = alphabet
        self.algorithm = algorithm
        self.set_chars_to_check()
        self.origHash = hashlib.new(self.algorithm, key).hexdigest()
        self.what_we_got()
        self.run()

        print "That took: ", self.elapsed, " seconds."

        if self.rec == "found":

            print "At about: ", self.speed, " hashes per second."
            return self.key
        else:
            print "No bounce no play."
            return

    def set_chars_to_check(self):
        iterations = alphabet.__len__()
        while True:
            iterations *= alphabet.__len__()
            self.charactersToCheck += 1
            if iterations > 2000000:
                self.charactersToCheck -= 1
                iterations /= alphabet.__len__()
                break
        print "Checking ", self.charactersToCheck, "characters per chunk."
        self.chunk_size = iterations

    def crack_it(self):
        children = []
        for j in range(0, num_processes):
            children.append(Process(target=self.check_keys, args=(self.queue, self.countey, self.done)))
            children[j].start()

        #this may disappear, why even implement passwords that short?
        if minKeyLength < self.charactersToCheck:
            for i in range(minKeyLength, self.charactersToCheck):
                self.queue.put(WorkUnit('', i))

        for i in range(minKeyLength - self.charactersToCheck, maxKeyLength - self.charactersToCheck + 1):
            prefixes = itertools.chain.from_iterable(itertools.product(alphabet, repeat=j)for j in range(i, i+1))
            print "starting process for key length ", i + self.charactersToCheck
            for prefix in prefixes:
                if self.done.value:
                    self.queue.close()
                    return
                self.queue.put(WorkUnit(prefix, i))
            with self.done.get_lock():
                if self.done.value:
                    self.queue.close()
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
        mycount = 0
        while queue:
            if done.value:
                return
            workunit = queue.get()
            print "checkKeys called for the prefix ", ''.join(workunit.prefix)

            #support for 1 or 2 char keys is broken for now, maybe forever, who allows passwords so short?
            if workunit.length < self.charactersToCheck:
                keysize = workunit.length
            else:
                keysize = self.charactersToCheck

            prefix = ''.join(workunit.prefix)
            keylist = itertools.product(alphabet, repeat=self.charactersToCheck)
            for key in keylist:
                tempkey = prefix + ''.join(key)
                mycount += 1
                if self.is_solution(tempkey):
                    done.value = True
                    self.key = tempkey
                    while not queue.empty():
                        queue.get()
                    with self.countey.get_lock():
                        countey.value += mycount
                    print "We win!"

                    return True
            with self.countey.get_lock():
                countey.value += self.chunk_size
        return None

    def get_hash(self):

        key = raw_input("Enter a key from %d to %d characters: " % (minKeyLength, maxKeyLength))
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
        print "Searching:    ", alphabet
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

        self.speed = self.countey.value / self.elapsed

        return

    def commandline(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        self.what_we_got()
        self.get_hash()

        os.system('cls' if os.name == 'nt' else 'clear')
        self.what_we_got()

        self.set_chars_to_check()

        self.run()

        print "That took: ", self.elapsed, " seconds."
        self.speed = self.countey.value/self.elapsed
        print "At about: ", self.speed, " hashes per second."

        if self.done.value:
            return self.key
        else:
            print "You lose."

        exit()



if __name__ == '__main__':
    bf = Brute_Force()
    bf
