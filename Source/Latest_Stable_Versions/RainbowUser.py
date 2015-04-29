#   RainbowUser.py

#   A companion to RainbowMaker.py, RainbowUser uses a pre-computed
#   rainbow table to search for a given hash, attempting to find the
#   associated key.

#   Chris Bugg
#   10/7/14

#TODO: Implement hashes-from-a-file

import hashlib
import random
from multiprocessing import Process, Pipe, Lock, cpu_count

from Chunk import Chunk


class RainbowUser():

    #Class Variables

    #Algorithm that is used
    algorithm = ""
    #How many characters is the key
    numChars = 1
    #List of the alphabet to be used
    alphabet = []
    #What is the shorthand of the alphabet
    alphabet_choice = ""
    #Name of the file to be used
    file_name = "1"
    #File object
    file = 1
    #Width of the table
    width = 1
    #Height of the table
    height = 1
    #List of hashes
    hash_list = []
    key_list = []
    done = False
    file_location = 1
    chunk_count = 0
    hash = 0
    eof = False
    found = False
    key = ""
    iteration = 100000
    num_processes = cpu_count()
    total_chunks = 0

    #Constructor
    def __init__(self):

        #Do nothing
        x=0

    ############################################################
    ###############         Main Methods         ###############
    ############################################################

    #Searches the chunk for the key (given the hash in the chunk.params)
    def find(self, chunk):

        #Set class variables based on parameters from the chunk
        self.set_variables(chunk.params)

        #Split the data (as a string) into a list of lines
        lines_list = chunk.data.splitlines()

        #
        # First, we'll take the data and put it into two lists for searching

        #Make two lists, one for each key and one for each hash of the lines
        key_list = []
        hash_list = []

        tempCounter = 0

        #For every line in the list
        for x in lines_list:

            #Split the line into a list of the two elements
            line_list = x.split()

            #Put the key in the key list
            key_list.append(line_list[0])

            #put the hash in the hash list
            hash_list.append(line_list[1])

        #divides up list into smaller lists, that we will feed the sub-processes
        key_sub_list = self.chunk_it(key_list, self.num_processes)
        hash_sub_list = self.chunk_it(hash_list, self.num_processes)

        #
        # Second, we'll actually do the searching

        lock = Lock()

        parent_pipe, child_pipe = Pipe()

        children = []

        for i in range(0, self.num_processes):
            children.append(Process(target=self.sub_process,
                                    args=(child_pipe, lock,
                                          key_sub_list[i],
                                          hash_sub_list[i], )))
            children[i].start()

        count = 0

        done = False

        rec = 0

        while not done:

            if count > (self.num_processes - 1):

                for i in range(0, self.num_processes):

                    children[i].join()

                    self.found = False

                    self.done = True

                    done = True

            else:

                rec = parent_pipe.recv()

                if rec == "found":

                    self.key = parent_pipe.recv()

                    for i in range(0, self.num_processes):

                        children[i].terminate()

                    done = True

                    self.found = True

                    self.done = True

                elif rec == "collisionDetected":

                    print "Collision Detected!"

                count += 1

    #The sub-process function
    def sub_process(self, pipe, lock, key_list, hash_list):

        done = False

        temp_hash = self.hash

        #Which line we found the hash on
        where = 0

        timeout = 0

        #Did we find a matching line? (Y=1/N=0)
        signal = 0

        while not done:

            #For every hash in the list
            for x in hash_list:

                #If our hash matches the one in the list
                if temp_hash == x:

                    #We found the line that matches, now just search the line for the key
                    done = True

                    signal = 1

                    #Which line we found the hash on (index location)
                    where = hash_list.index(x)

            if not done:

                temp_reduced = self.get_seeded_key(temp_hash)

                temp_hash = self.hash_this(temp_reduced)

            timeout += 1

            #If we've searched farther than we're supposed to, stop
            if timeout > self.iteration:

                done = True

        #If we found a matching line
        if signal == 1:

            #Set our key to the starting key of that line
            temp_key = key_list[where]

            #For as wide as our table is plus one
            for y in range(self.width + 1):

                #hash our temp_key
                temp_hash = self.hash_this(temp_key)

                #And compare to original key
                if self.hash == temp_hash:

                    #FOUND THE KEY!

                    self.found = True

                    self.done = True

                    lock.acquire()

                    pipe.send("found")

                    pipe.send(temp_key)

                    pipe.close()

                    lock.release()

                else:

                    #If not, reduce the hash and try again
                    temp_key = self.get_seeded_key(temp_hash)

            if self.found == False:

                self.done = True

                lock.acquire()

                pipe.send("collisionDetected")

                pipe.close()

                lock.release()

        else:

            #No matching line found
            self.done = True

            lock.acquire()

            pipe.send("notFound")

            pipe.close()

            lock.release()

    ###########################################################
    ###############         Get Methods         ###############
    ###########################################################

    #Gets the fileName
    def get_file_name(self):

        return self.file_name

    #Produces seeded key
    def get_seeded_key(self, seed):

        random.seed(seed)

        seed_key = ""

        characters = int(self.numChars)

        for x in range(characters):

            seed_key = seed_key + random.choice(self.alphabet)

        return seed_key

    #Produces a random key to start
    def get_rand_key(self):

        random.seed()

        rand_key = ""

        characters = int(self.numChars)

        for x in range(characters):

            rand_key = rand_key + random.choice(self.alphabet)

        return rand_key

    #Returns number of rows in table
    def get_height(self):

        return self.height

    #Returns number of columns (chains) in table
    def get_length(self):

        return self.width

    #Returns key
    def get_key(self):

        return self.key

    #Gets the next chunk from the file to process
    def get_next_chunk(self):

        #Open the file for reading
        self.file = open(self.file_name, 'r')

        #Seek to where we left off in the file
        self.file.seek(self.file_location)

        line = self.file.readline()

        data = ""

        #keeps count of how many lines we've pu in currentChunk[]
        line_counter = 0

        #to send to controller to say we're not done yet
        eof = False

        if line == "":

            eof = True

        while not line == "":

            data += line

            line = self.file.readline()

            if line == "":

                eof = True

            line_counter += 1

            #If our chunk is at least 1000 lines, stop adding to it
            if line_counter >= 1000:

                line = ""

                eof = False

        #update class on where we are in the file
        self.file_location = self.file.tell()

        self.file.close()

        self.eof = eof

        chunk = Chunk()

        chunk.data = data

        chunk.params = "rainbowuser " + self.algorithm + " " + self.hash + " " + str(self.alphabet)
        chunk.params += " " + str(self.numChars) + " 0 0 0 " + str(self.width) + " 0 " + str(eof)

        return chunk

    #Returns the original hash
    def get_hash(self):

        return self.hash

    #Returns total_chunks variable
    def get_total_chunks(self):

        return self.total_chunks

    ###########################################################
    ###############         Set Methods         ###############
    ###########################################################

    #Sets the hash we're looking for
    def set_hash(self, temp_hash):

        self.hash = temp_hash

    #Sets the algorithm choice
    def set_algorithm(self, algo):

        self.algorithm = algo

    #Sets the number of characters of the key
    def set_num_chars(self, num_chars):

        self.numChars = num_chars

    #Get the alphabet and direction to be searched
    def set_alphabet(self, alphabet):

        self.alphabet = alphabet

    #Get file name
    def set_file_name(self, file_name):

        self.file_name = file_name

        #Checks for filenotfound and returns code to caller class
        try:
            temp_file = open(file_name, "r")
            temp_file.close()

        except (OSError, IOError):

            return "Fail"

        return "Good"

    #Sets all class variables to ones given from server (params)
    def set_variables(self, params_string):

        params_list = params_string.split()

        self.algorithm = params_list[1]

        self.hash = params_list[2]

        self.alphabet = params_list[3]

        self.set_alphabet(self.alphabet)

        self.numChars = int(params_list[4])

        self.width = int(params_list[8])

        self.iteration = self.width * 2

    #Sets the total_chunks variable based on file
    def set_total_chunks(self):

        temp_file = open(self.file_name, "r")

        line_count = 0

        for line in temp_file:
            line_count += 1

        temp_file.close()

        #Total chunks = lines in dictionary minus first line divided by size of chunks
        self.total_chunks = (line_count - 1) / 1000

        #Adjust the total chunks to account for larger chunks that occur
        self.total_chunks -= 1

        #If total chunks is <1, make it at least 1
        if self.total_chunks < 1:

            self.total_chunks = 1

    #############################################################
    ###############         Other Methods         ###############
    #############################################################

    #Returns whether or not we're done creating
    def is_done(self):

        return self.done

    #Hashes key
    def hash_this(self, key):

        return hashlib.new(self.algorithm, key).hexdigest()

    #Resets all class variables to default
    def reset(self):

        self.algorithm = 1
        self.numChars = 1
        self.alphabet = 1
        self.file_name = "1"
        self.file = 1
        self.width = 1
        self.height = 1
        self.hash_list = []
        self.key_list = []
        self.done = False

    #Returns if eof
    def is_eof(self):

        return self.eof

    #Returns T/F if found or not
    def is_found(self):

        return self.found

    #Reads the first line of file to setup variables
    def gather_info(self):

        #Open the file for reading
        self.file = open(self.file_name, 'r')

        #Read the first line
        line = self.file.readline()

        #Update class on where we are in the file (hopefully, second line)
        self.file_location = self.file.tell()

        #Close the file, since we're done with it
        self.file.close()
        #print line
        #Split the line into a list, and assign list elements to variables
        vars_list = line.split()
        #print vars_list
        self.algorithm = vars_list[0]

        self.numChars = int(vars_list[1])

        self.alphabet = vars_list[2]

        #self.alphabet = self.setAlphabet(self.alphabet)

        self.width = int(vars_list[3])
        #print self.width

        #Sets the total_chunks variable based on file
        self.set_total_chunks()

    #Divides up a list, and stores those sub-lists in a big list
    @staticmethod
    def chunk_it(temp_list, pieces):

        chunky = [temp_list[i::pieces] for i in range(pieces)]

        return chunky