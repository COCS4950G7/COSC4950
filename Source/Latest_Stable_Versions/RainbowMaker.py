#   RainbowMaker.py

#   A companion to RainbowUser.py, RainbowMaker creates rainbow
#   tables for a time/cost trade-off. Essentially, it will pre-compute
#   a large amount of hashes so that they can be used later to
#   find a key (given a hash), in a manner that is many times
#   faster than a regular brute-force approach.

#   Chris Bugg
#   10/7/14

#Imports
import hashlib
import random
from multiprocessing import Process, Pipe, Lock, cpu_count

from Chunk import Chunk


class RainbowMaker():

    #Class Variables

    #Algorithm that is used
    algorithm = ""
    #How many characters is the key
    num_chars = 1
    #List of the alphabet to be used
    alphabet = []
    #Name of the file we're creating
    file_name = "1"
    #File object
    file = 1
    #Width of the table, in columns
    width = 1
    #Height of the table, in rows
    height = 1
    #List of hashes
    hash_list = []
    #List of keys
    key_list = []
    #Are we done making the table yet?
    done = False
    #How far in the file are we, in bits
    file_location = 1
    #How many chunks we've processed
    chunk_count = 0
    #Number of processes we should run, based on virtual cpu cores
    num_processes = cpu_count()
    #Total chunks in the file
    total_chunks = 0
    #Total rows per chunk, depends on table width
    total_rows = 0
    #About how many operations per chunk, think of this as height*width of a chunk
    chunk_size = 1000000

    #Constructor
    def __init__(self):

        #Do nothing
        x=0

    ############################################################
    ###############         Main Methods         ###############
    ############################################################

    #Create (and return) a chunk of the table, and do all that sub-process stuff
    def create(self, params_chunk):

        #Set variables to that of server, get from parameter(-bearing) chunk
        self.set_variables(params_chunk.params)

        #big list containing all the lines from the nodes
        big_chunk = ""

        #This is duplicate code because it needs to be determined by server and clients
        #rows per chunk equals chunk_size (good chunk size) divided by width
        #   this gives us a continuous size of <= chunk_size
        self.total_rows = self.chunk_size / self.width

        #If table size wide enough, just make it one row per chunk
        if self.total_rows <= 0:

            self.total_rows = 1
        #print "total_rows in create():", str(self.total_rows)
        #Number of rows each sub-process will create
        #   equals total rows per chunk divided by number of processes
        sub_chunk_size = self.total_rows / self.num_processes

        #If the rows are wider than our chunk_size, do one per process
        if sub_chunk_size <= 0:

            sub_chunk_size = 1

        #print "sub_chunk_size: ", str(sub_chunk_size)

        #Create lock
        lock = Lock()

        #Create the pipes
        parent_pipe, child_pipe = Pipe()

        children = []

        for i in range(0, self.num_processes):

            children.append(Process(target=self.sub_process, args=(child_pipe, lock, sub_chunk_size, )))

            children[i].start()

        #Count our iterations of responses
        count = 0

        #Are we done yet?
        done = False

        rec = 0

        while not done:

            #If all the nodes have given us their lists
            if count > (self.num_processes - 1):

                for i in range(0, self.num_processes):

                    children[i].join()

                    self.done = True

                    done = True

            else:

                #Get a sub-chunk from a node
                rec = parent_pipe.recv()

                big_chunk += rec

                count += 1

        return_chunk = Chunk()

        return_chunk.data = big_chunk

        return return_chunk

    #The sub-process function
    def sub_process(self, pipe, lock, chunk_size):

        #The list to return with strings to be the lines of the file
        return_list = ""

        for x in range(chunk_size):

            rand_key = self.get_rand_key()

            reduced = rand_key

            #temp_hash = self.hashThis(reduced)

            for y in range(self.width):

                temp_hash = self.hash_this(reduced)

                reduced = self.get_seeded_key(temp_hash)

            temp_hash = self.hash_this(reduced)

            return_list += rand_key + " " + temp_hash + "\n"

        lock.acquire()

        pipe.send(return_list)

        pipe.close()

        lock.release()

    #Finds collisions so the user can determine if they want to run collisionFixer()
    def collision_finder(self):

        #Open file for reading
        self.file = open(self.file_name, 'r')

        #Make every line an element in a list
        all_lines_list = list(self.file)

        #Close the dang file
        self.file.close()

        #Number of offending hashes (duplicates)
        offender_count = 0

        #For every line (x) in the list (of all the lines)
        for x in all_lines_list:

            #Split the line into a list of two (key and hash)
            line_list_x = x.split()

            #Store hash value in temp var
            hash_x = line_list_x[1]

            #How many times have we seen this hash
            hash_count = 0

            #For every other line in the list (of all the lines)
            for y in all_lines_list:

                #Split the line into a list of two (key and hash)
                line_list_y = y.split()

                #Store hash value in temp var
                hash_y = line_list_y[1]

                if hash_x == hash_y:

                    hash_count += 1

            #If this hash has duplicates, increment offender_count
            if hash_count > 1:

                offender_count += 1

        #Returns the number of duplicate hashes
        return offender_count

    #Finds and fixes collisions in the final hash list
    def collision_fixer(self):

        #Create/open file
        self.file = open(self.file_name, 'r')

        #Make every line an element in a list
        all_lines_list = list(self.file)

        self.file.close()

        #Counter to keep track of how many duplicates
        offender_count = 0

        #For every line (x) in the list (of all the lines)
        for x in all_lines_list:

            #Split the line into a list of two (key and hash)
            line_list_x = x.split()

            #Store hash value in temp var
            hash_x = line_list_x[1]

            #How many times have we seen this hash
            hash_count = 0

            #For every other line in the list (of all the lines)
            for y in all_lines_list:

                #Split the line into a list of two (key and hash)
                line_list_y = y.split()

                #Store hash value in temp var
                hash_y = line_list_y[1]

                if hash_x == hash_y:

                    hash_count += 1

            #If this hash has duplicates, increment offender_count
            if hash_count > 1:

                #remove that line (since it's a duplicate)
                all_lines_list.remove(x)

                offender_count += 1

        #for every line that was a duplicate, make a new one
        for x in range(offender_count):

            #Get a new key for this row
            rand_key = self.get_rand_key()

            reduced = rand_key

            #Do the iteration for this row
            for y in range(self.width):

                temp_hash = self.hash_this(reduced)

                reduced = self.get_seeded_key(temp_hash)

            temp_hash = self.hash_this(reduced)

            line = rand_key + " " + temp_hash + "\n"

            all_lines_list.append(line)

        #Create/open file
        self.file = open(self.file_name, 'r+')

        for z in all_lines_list:

            self.file.write("%s" % z)

        self.file.close()

    ###########################################################
    ###############         Get Methods         ###############
    ###########################################################

    #Gets the fileName
    def get_file_name(self):

        return self.file_name

    #Produces seeded key (Reduction Function)
    def get_seeded_key(self, seed):

        random.seed(seed)

        seed_key = ""

        characters = int(self.num_chars)

        for x in range(characters):

            seed_key = seed_key + random.choice(self.alphabet)

        return seed_key

    #Produces a random key to start
    def get_rand_key(self):

        random.seed()

        rand_key = ""

        characters = int(self.num_chars)

        for x in range(characters):

            rand_key = rand_key + random.choice(self.alphabet)

        return rand_key

    #Returns number of rows in table
    def get_rows(self):

        return self.height

    #Returns number of columns (chains) in table
    def get_length(self):

        return self.width

    #Returns number of rows in table
    def get_height(self):

        return self.height

    #Returns total_chunks variable
    def get_total_chunks(self):

        return self.total_chunks

    ###########################################################
    ###############         Set Methods         ###############
    ###########################################################

    #Sets the algorithm choice
    def set_algorithm(self, algo):

        self.algorithm = algo

    #Sets the number of characters of the key
    def set_num_chars(self, num_chars):

        self.num_chars = num_chars

    #Get the alphabet and direction to be searched
    def set_alphabet(self, alphabet):

        self.alphabet = alphabet

    #Get file name
    def set_file_name(self, file_name):

        self.file_name = file_name

    #Get dimensions of the table
    def set_dimensions(self, chain_length, num_rows):

        self.width = int(chain_length)

        self.height = int(num_rows)

    #Sets all class variables to ones given from server (params)
    def set_variables(self, params_string):

        params_list = params_string.split()

        self.algorithm = params_list[1]

        self.alphabet = params_list[3]

        self.set_alphabet(self.alphabet)

        self.num_chars = int(params_list[4])

        self.width = int(params_list[8])

        self.height = int(params_list[9])

    #Sets the total_chunks variable
    def set_total_chunks(self):

        #rows per chunk equals chunk_size (good chunk size) divided by width
        #   this gives us a continuous size of <= chunk_size
        self.total_rows = self.chunk_size / self.width

        #If table size wide enough, just make it one row per chunk
        if self.total_rows <= 0:

            self.total_rows = 1

        #total chunks equals all rows in table divided by rows per chunk
        self.total_chunks = self.height / self.total_rows

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

    #Sets up the file initially (put info in first line)
    def setup_file(self):

        #Open the file for writing
        self.file = open(self.file_name, 'w')

        self.file.write(self.algorithm + " " + str(self.num_chars) + " " + str(self.alphabet) + " "
                        + str(self.width) + "\n")

        self.file_location = self.file.tell()

        self.file.close()

        #Sets total_chunk variable, based on input variables
        self.set_total_chunks()

    #Puts a done chunk (already processed by a node) into the table (file)
    def put_chunk_in_file(self, chunk_of_done):

        #Split chunkOfDone's data into a list
        lines_list = chunk_of_done.data.splitlines()

        #Open the file for writing
        self.file = open(self.file_name, 'r+')

        #Seek to where we left off in the file
        self.file.seek(self.file_location)

        for x in lines_list:

            #print to file
            self.file.write(x + "\n")

            #And increment count
            self.chunk_count += 1

        #Save where we are in file
        self.file_location = self.file.tell()

        #Close the file
        self.file.close()

        #Check if we've gotten all the chunks we need
        if self.chunk_count >= self.height:

            #Chunk count will now represent the true height (since we're done adding to it)
            self.height = self.chunk_count

            self.done = True

    #Resets all class variables to default
    def reset(self):

        self.algorithm = ""
        self.num_chars = 1
        self.alphabet = 1
        self.file_name = "1"
        self.file = 1
        self.width = 1
        self.height = 1
        self.hash_list = []
        self.key_list = []
        self.done = False
        self.file_location = 1
        self.chunk_count = 0

    #Returns a chunk with all variables needed by nodes
    def make_params_chunk(self):

        temp_chunk = Chunk()

        temp_chunk.params = "rainbowmaker " + self.algorithm + " 0 " + str(self.alphabet) + " " + str(self.num_chars)
        temp_chunk.params += " " + str(self.num_chars) + " 0 0 " + str(self.width) + " " + str(self.height)

        return temp_chunk