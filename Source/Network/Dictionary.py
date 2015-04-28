#   Dictonary.py

#   Uses a dictionary file to attempt to crack a given password hash.
#   Simply reads through the file line by line, and tries each entry.
#   Possible source for passwords are 'top most used passwords' lists

#Imports
import hashlib
from multiprocessing import Process, Pipe, Lock, cpu_count, Queue, Value
from Chunk import Chunk


class Dictionary():

    #Class variables

    #Are we done searching our current chunk
    done = False
    #What algorithm are we using
    algorithm = ""
    #What's the file name for the dictionary file
    fileName = ""
    #What's the list of hashes file name
    hash_file_name = ""
    #What's the results file name
    done_file_name = ""
    #What's the hash
    hash = ""
    #What's our current searching status
    status = ""
    #Have we found the key yet
    found = False
    #Dictionary File object
    file = 0
    #Hashes file object
    hashFile = 0
    #Results file object
    doneFile = 0
    #The key we're searching for
    key = ""
    #The list of all lines in the dictionary file
    all_lines_list = []
    #The location in the dictionary file, in bits
    file_location = 0
    #Have we reached the end of the dictionary file
    eof = False
    #The number of processes to run = # virtual cores in host computer
    num_processes = cpu_count()
    #List of hashes to crack
    list_of_hashes = []
    #List of results to send to results file
    done_list = []
    #Cracking a single hash or a file of hashes
    single_hash = True
    #Maximum lines in the dictionary file per chunk
    max_lines = 1000000
    #Total number of chunks that we'll get from a file
    total_chunks = 0

    #Constructor
    def __init__(self):

        #Do nothing
        x = 1

    ############################################################
    ###############         Main Methods         ###############
    ############################################################

    #Actually finds the hash in the file (hopefully)
    def find(self, chunk):

        #turns params from string to list
        params_list = chunk.params.split()

        #set class params with new info
        self.algorithm = params_list[1]

        self.hash = params_list[2]

        #Turns data from string into list
        chunk_list = chunk.data.split()

        #Sub chunk chunkList
        chunky = self.chunk_it(chunk_list, self.num_processes)

        #Create a lock
        lock = Lock()

        #Create the pipes used to communicate
        parent_pipe, child_pipe = Pipe()

        #Create a list for the children
        children = []

        #### List of Hashes ####
        if '$' in self.hash:

            #Split the string into a list
            self.list_of_hashes = self.hash.split('$')

            #Take out '$' deliminators from the hashes
            for x in self.list_of_hashes:

                x = x.strip('$')

            #Startup some processes.
            for i in range(0, self.num_processes):

                children.append(Process(target=self.sub_process_2, args=(child_pipe, lock, )))

                children[i].start()

            #Send each child a chunk
            for chunk in chunky:

                parent_pipe.send(chunk)

            #Count of processes done
            count = 0

            #If we're done searching
            done = False

            #What we've received from the children over the pipe
            rec = 0

            while not done:

                #If all the processes say their done
                if count > (self.num_processes - 1):

                    #Join them
                    for i in range(0, self.num_processes):

                        children[i].join()

                        self.done = True

                        done = True

                else:

                    rec = parent_pipe.recv()

                    if rec == "found":

                        self.key = parent_pipe.recv()

                        self.hash = parent_pipe.recv()

                        self.done_list.append(self.hash + "\n" + self.key)

                        self.found = True

                    count += 1

            return self.done_list

        ### Single Hash ####
        else:

            for i in range(0, self.num_processes):

                children.append(Process(target=self.sub_process, args=(child_pipe, lock, )))

                children[i].start()

            for chunk in chunky:

                parent_pipe.send(chunk)

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

                    count += 1

    #The sub-process worker function, for single hashes
    def sub_process(self, pipe, lock):

        #Get the lock
        lock.acquire()

        #Get the chunk to be worked from the parent
        chunk_list = pipe.recv()

        #Release the lock
        lock.release()

        #for every item in the allLinesList list
        for x in chunk_list:

            #Split the string ['able\r\n'] into a list ['able','\r','\n']
            #   Could also use .rstrip(), but this worked better
            x_line_to_list = x.split()

            #Check if it's NOT empty (or eof)
            if x_line_to_list:

                #If it's not, extract the word (leaving an '/n')
                new_x = x_line_to_list.pop()

            else:

                #Otherwise give it an empty value that doesn't crash the program
                new_x = ""

            #if the hashes match, YAY, return to get out of function
            if self.hash_this(new_x) == self.hash:

                lock.acquire()

                pipe.send("found")

                pipe.send(new_x)

                pipe.close()

                lock.release()

                return 0

        lock.acquire()

        pipe.send("not found")

        pipe.close()

        lock.release()

    #The sub-process2 worker function, for a file (list) of hashes
    def sub_process_2(self, pipe, lock):

        lock.acquire()

        chunk_list = pipe.recv()

        lock.release()

        #for every item in the allLinesList list
        for x in chunk_list:

            #Split the string ['able\r\n'] into a list ['able','\r','\n']
            x_line_to_list = x.split()

            #Check if it's NOT empty (or eof)
            if x_line_to_list:

                #If it's not, extract the word (leaving an '/n')
                new_x = x_line_to_list.pop()

            else:

                #Otherwise give it an empty value that doesn't crash the program
                new_x = ""

            #For every hash in our list
            for temp_hash in self.list_of_hashes:

                #if the hashes match, YAY, return to get out of function
                if self.hash_this(new_x) == temp_hash:

                    lock.acquire()

                    pipe.send("found")

                    pipe.send(new_x)

                    pipe.send(temp_hash)

                    pipe.close()

                    lock.release()

                    return 0

        lock.acquire()

        pipe.send("not found")

        pipe.close()

        lock.release()

    ###########################################################
    ###############         Get Methods         ###############
    ###########################################################

    #Returns status summary of searching so far
    def get_status(self):

        return self.status

    #Returns hash
    def get_hash(self):

        return self.hash

    #Returns list of lines in file
    def get_list(self):

        return self.all_lines_list

    #Gets next chunk of dictionary file as list
    def get_next_chunk(self):

        #Open the file for reading
        self.file = open(self.fileName, 'r')

        #Seek to where we left off in the file
        self.file.seek(self.file_location)

        #Placeholder for the line of the file we've just read
        line = self.file.readline()

        #String that is composed of all the keys we're currently searching through
        data = ""

        #keeps count of how many lines we've pu in currentChunk[]
        line_counter = 0

        #to send to controller to say we're not done yet
        eof = False

        #While we haven't hit the end of the file
        while not line == "":

            data += line

            line = self.file.readline()

            if line == "":

                eof = True

            line_counter += 1

            #If our chunk is at least self.max_lines lines, stop adding to it
            if line_counter >= self.max_lines:

                line = ""

                eof = False

        #update class on where we are in the file
        self.file_location = self.file.tell()

        self.file.close()

        self.eof = eof

        chunk = Chunk()

        chunk.data = data

        chunk.params = "dictionary " + self.algorithm + " " + self.hash + " 0 0 0 0 " + str(self.file_location) \
                       + " 0 0 " + str(eof)

        return chunk

    #Returns total_chunks variable
    def get_total_chunks(self):

        return self.total_chunks

    #Gets next chunk of file as list
    def get_this_chunk(self, params):

        #Open the file for reading
        self.file = open(self.fileName, 'r')

        #Get the chunk's fileLocation from params
        #turns params from string to list
        params_list = params.split()

        #set fileLocation to equivalent params value
        file_location = params_list[7]

        #Seek to where we left off in the file
        self.file.seek(file_location)

        line = self.file.readline()

        data = ""

        #keeps count of how many lines we've pu in currentChunk[]
        line_counter = 0

        #to send to controller to say we're not done yet
        eof = False

        while not line == "":

            data += line

            line = self.file.readline()

            if line == "":

                eof = True

            line_counter += 1

            #If our chunk is at least 1000 lines, stop adding to it
            if line_counter >= self.max_lines:

                line = ""

                eof = False

        #update class on where we are in the file
        file_location = self.file.tell()

        self.file.close()

        self.eof = eof

        chunk = Chunk()

        chunk.data = data

        chunk.params = "dictionary " + self.algorithm + " " + self.hash + " 0 0 0 0 " + str(file_location) + " 0 0 "

        return chunk

    ###########################################################
    ###############         Set Methods         ###############
    ###########################################################

    #Sets the original hash we're looking for
    def set_hash(self, temp_hash):

        self.hash = temp_hash

    #Sets key
    def set_key(self, key):

        self.key = key

    #Sets the total_chunks variable based on dictionary file
    def set_total_chunks(self):

        #Open the file
        temp_file = open(self.fileName, "r")

        #Number of lines in the file
        line_count = 0

        #For every line in the file
        for line in temp_file:

            #Increment the count
            line_count += 1

        temp_file.close()

        #Total chunks = lines in dictionary minus first line divided by size of chunks
        self.total_chunks = (line_count - 1) / self.max_lines

        #Adjust the total chunks to account for larger chunks that occur
        self.total_chunks -= 1

        #If total chunks is <1, make it at least 1
        if self.total_chunks < 1:

            self.total_chunks = 1

    #Sets algorithm to be used
    def set_algorithm(self, algorithm):

        self.algorithm = algorithm

    #Sets the dictionary file's name
    def set_file_name(self, file_name):

        self.fileName = str(file_name)

        #Checks for file not found and returns code to caller class
        try:
            temp_file = open(self.fileName, "r")
            temp_file.close()

        except (OSError, IOError):
            return "Fail"

        #sets total_chunks variable, based on dictionary file
        self.set_total_chunks()

        return "Good"

    #Sets the dictionary file's name
    def set_hash_file_name(self, file_name):

        self.hash_file_name = file_name

        #Checks for filenotfound and returns code to caller class
        try:
            temp_file = open(file_name, "r")
            temp_file.close()

        except (OSError, IOError):
            return "Fail"

        #Import file to set as hash

        #Open the file for reading
        self.hashFile = open(self.hash_file_name, 'r')

        #Put all the lines of the file in a list
        self.list_of_hashes = list(self.hashFile)

        self.hashFile.close()

        self.hash = ""

        #For every hash in the list
        for x in self.list_of_hashes:

            x = x.rstrip()

            #add it to the string, self.hash, with a delineating char
            self.hash += str(x) + "$"

        return "Good"

    #Sets the dictionary file's name
    def set_done_file_name(self, file_name):

        self.done_file_name = file_name

    ##########################################################
    ###############         Is Methods         ###############
    ##########################################################

    #Returns T/F if done searching or not
    def is_done(self):

        return self.done

    #Returns T/F if found or not
    def is_found(self):

        return self.found

    #Returns if eof
    def is_eof(self):

        return self.eof

    #############################################################
    ###############         Other Methods         ###############
    #############################################################

    #Creates the results file with keys and hashes
    def make_done_file(self, done_list):

        self.doneFile = open(self.done_file_name, 'w')

        done_list = list(set(done_list))

        for line in done_list:

            self.doneFile.write(line + "\n")

        self.doneFile.close()

    #Hashes a key
    def hash_this(self, key):

        this_hash = hashlib.new(self.algorithm, key).hexdigest()

        return this_hash

    #Returns key
    def show_key(self):

        return self.key

    #Convers all lines of file into global list
    def make_list_of_file(self):

        #Open the file for reading
        self.file = open(self.fileName, 'r')

        #Put all the lines of the file in a list
        self.all_lines_list = list(self.file)

        self.file.close()

    #Chunks up a list
    @staticmethod
    def chunk_it(temp_list, pieces):

        chunky = [temp_list[i::pieces] for i in range(pieces)]

        return chunky

    #Resets class object to default values
    def reset(self):

        self.done = False
        self.algorithm = ""
        self.fileName = ""
        self.hash = ""
        self.status = ""
        self.found = False
        self.file = 0
        self.key = ""
        self.all_lines_list = []
        self.file_location = 0
        self.eof = False