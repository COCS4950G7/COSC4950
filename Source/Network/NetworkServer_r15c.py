# NetworkServer_r15c

# 3/29/2015
# UNFINISHED and UNSTABLE

# This is a preliminary version to fix the Windows incompatibility.
# By removing make_server_manager() and adding that functionality in to each of the chunk maker functions,
# the SyncManager can be used without pickling. In addition, check results must be initiated from within the chunk
# maker functions so the manager's queues can be passed in.

# As of this update, the only function that has been tested and shown to do anything is Dictionary in networked mode,
# but it currently stops after just one chunk, this appears to be a problem with dictionary.
# Everything else should be treated as broken until proved otherwise.

# Nick Baum

#=====================================================================================================================
#IMPORTS
#=====================================================================================================================
#import dill #temporarily commented out
from multiprocessing.managers import SyncManager
from multiprocessing import Process, Value, Event, Queue, freeze_support, current_process
import os
import platform
import Queue as Qqueue
import time
import socket
import Dictionary
import Brute_Force
import RainbowMaker
import RainbowUser
import Chunk
import signal
#=====================================================================================================================
#END OF IMPORTS
#=====================================================================================================================
#NAMING CONFLICTS
#TODO Problematic naming convention used, there is a global shutdown variable (called via self.shutdown)
#TODO                                       there is also a shutdown variable as a parameter in chunk_results function (called shutdown)
#TODO                                       there is also a shutdown variable as a parameter in chunk_dictionary function (called shutdown)
#TODO                                       same thing for chunk_brute_force
#TODO                                       same thing for chunk_rainbow
#TODO                                       same thing for chunk_rainbow_maker
#TODO                                       same thing for check_results
#TODO RECOMMENDED SOLUTION: only use the global shutdown variable, OR set self.shutdown= shutdown (the parameter shutdown)

#NAMING CONFLICTS
#TODO Problematic naming convention used, there is a global result_queue variable (called via self.result_queue)
#TODO                                       there is also a result_queue local variable in chunk_dictionary (called result_queue)
#TODO                                       there is also a result_queue local variable in chunk_brute_force
#TODO                                       there is also a result_queue local variable in chunk_rainbow
#TODO                                       there is also a result_queue local variable in chunk_rainbow_maker
#TODO                                       there is also a result_queue local variable in start_single_user
#TODO                                       there is also a result_queue local variable in run_dictionary
#TODO                                       there is also a result_queue local variable in run_brute_force
#TODO                                       there is also a result_queue local variable in run_rain_user
#TODO                                       there is also a result_queue local variable in run_rain_maker

#NAMING CONFLICTS
#TODO Problematic naming convention used, there is a global job_queue variable (called via self.job_queue)
#TODO                                       there is also a job_queue local variable in chunk_dictionary (called job_queue)
#TODO                                       there is also a job_queue local variable in chunk_brute_force
#TODO                                       there is also a job_queue local variable in chunk_rainbow
#TODO                                       there is also a job_queue local variable in chunk_rainbow_maker
#TODO                                       there is also a job_queue local variable in start_single_user
#TODO                                       there is also a job_queue local variable in run_dictionary
#TODO                                       there is also a job_queue local variable in run_brute_force
#TODO                                       there is also a job_queue local variable in run_rain_user
#TODO                                       there is also a job_queue local variable in run_rain_maker

#INCONSISTENT USE OF self.total_chunks variable
#TODO self.total_chunks= dictionary.get_total_chunks inconsistancy, the assignment statement for self.total_chunks is commented out in run_server, if cracking mode == dic
#TODO                  = bf.get_total_chunks  inconsistency,  the assignment statement for self.total_chunks is NOT commented out in run_server, if cracking mode == bf
#TODO                  = rain.get_total_chunks inconsistency, the assignment statement for self.total_chunks is NOT commented out in run_server, if cracking mode == rain
#TODO                  = rainmaker.get_total_chunks inconsistency, the assignment statement for self.total_chunks is NOT commented out in run_server, if cracking mode == rainmaker

#INCONSISTENT USE OF THE SHUTDOWN VARIABLE
#TODO while not shutdown.is_set inconsistency, the while loop in chunk_results checks the local variable shutdown
#TODO while not SELF.shutdown.is_set (for single mode) the while loop in chunk_dictionary checks the global variable shutdown
#TODO while not shutdown.is_set  (for network mode)  the while  loop in chunk_dictionary checks the local variable shutdown
#TODO while not shutdown.is_set   the while loop in chunk_brute_force checks the local variable shutdown
#TODO while not rainbow.isEof() and not shutdown.is_set    the while loop in chunk_rainbow checks the local variable shutdown
#TODO while not shutdown.is_set (inside the while loop mentioned above)  the while loop in chunk_rainbow checks the local variable shutdown
#TODO if shutdown.is_set   the conditional if statement in chunk_rainbow checks the local variable shutdown
#TODO while not shutdown.is_set     the while loop in chunk_rainbow_maker checks the local variable shutdown
#TODO if shutdown.is_set       the conditional if statement in chunk_rainbow_maker checks the local variable shutdown
#TODO if SELF.shutdown.is_set    the conditional if statement in start_single_user checks the global variable shutdown
#TODO while not SELF.shutdown.is_set   the while loop in run_dictionary checks the global variable shutdown
#TODO while not SELF.shutdown.is_set   the while loop in run_brute_force checks the global variable shutdown
#TODO while not SELF.shutdown.is_set   the while loop in run_rain_user checks the global variable shutdown
#TODO while not SELF.shutdown.is_set   the while loop in run_rain_maker checks the global variable shutdown

#CREATING A REDUNDANT LOCAL VARIABLE OF A GLOBAL VARIABLE
#TODO creating a local variable job_queue with the same name and the same value as the global variable self.job_queue in chunk_dictionary
#TODO                           job_queue with the same name and the same value as the global variable self.job_queue in chunk_brute_force
#TODO                           job_queue with the same name and the same value as the global variable self.job_queue in chunk_rainbow
#TODO [this list is not exhaustive...]

#CREATING A REDUNDANT LOCAL VARIABLE OF A GLOBAL VARIABLE
#TODO creating a local variable result_queue with the same name and the same value as the global variable self.result_queue in chunk_dictionary
#TODO                           result_queue with the same name and the same value as the global variable self.result_queue in chunk_brute_force
#TODO                           result_queue with the same name and the same value as the global variable self.result_queue in chunk_rainbow
#TODO [this list is not exhaustive...]

#I am sure there are more, but this is definely enough to get started, Chris Hamm (Sorry to have to be the bringer of bad news)


class Server():
        IP = "127.0.0.1"  # defaults to the ping back
        PORTNUM = 22536
        AUTHKEY = "Popcorn is awesome!!!"

        cracking_mode = "dic"  # possible values are dic, bf, rain, rainmaker
        sent_chunks = []  # list of chunks added to queue, added with timestamp to keep track of missing pieces
        found_solution = Value('b', False)  # synchronized found solution variable
        total_chunks = 0
        settings = dict()
        single_user_mode = False
        rainmaker = RainbowMaker.RainbowMaker()
        shared_dict = None
        update = None
        shutdown = None
        job_queue = Queue(100)
        result_queue = Queue()
        mode_bit_1 = Event()
        mode_bit_2 = Event()
        manager = None

        def __init__(self, settings, shared_variables):
            current_process()._authkey = self.AUTHKEY #set the authentication key
            self.settings = settings
            self.get_ip() #gets the ip address of the machine
            self.cracking_mode = settings["cracking method"]

            self.shared_dict = shared_variables[0]
            self.shared_dict["server ip"] = self.IP
            self.shutdown = shared_variables[1]

            self.update = shared_variables[2]
            #Dictionary settings check
            #print "DEBUG: cracking method= "+str(settings["cracking method"])
            #print "DEBUG: algorithm= "+str(settings["algorithm"])
            #print "DEBUG: hash= "+str(settings["hash"])
            #print "DEBUG: file name= "+str(settings["file name"])
            #print "DEBUG: single= "+str(settings["single"])
            #Brute Force settings Check
            #print "DEBUG: cracking method= "+str(settings["cracking method"])
            #print "DEBUG: algorithm= "+str(settings["algorithm"])
            #print "DEBUG: hash= "+str(settings["hash"])
            #print "DEBUG: min key length= "+str(settings["min key length"])
            #print "DEBUG: max key length= "+str(settings["max key length"])
            #print "DEBUG: alphabet= "+str(settings["alphabet"])
            #print "DEBUG: single= "+str(settings["single"])

            #Rainbow Table Maker settings check
            '''
            print "Rainbow Table Maker Settings Check"
            print "DEBUG: cracking method= "+str(settings["cracking method"])
            print "DEBUG: algorithm= "+str(settings["algorithm"])
            print "DEBUG: key length= "+str(settings["key length"])
            print "DEBUG: alphabet= "+str(settings["alphabet"])
            print "DEBUG: chain length= "+str(settings["chain length"])
            print "DEBUG: num rows= "+str(settings["num rows"])
            print "DEBUG: file name= "+str(settings["file name"])
            print "DEBUG: single= "+str(settings["single"])
            '''
            #check to see if running single mode
            if "single" in settings:
                if settings["single"] == "True":
                    self.single_user_mode = True
                else:
                    self.single_user_mode = False
            #check to if in rainbow maker mode
            if self.cracking_mode == "rainmaker":
                self.rainmaker = RainbowMaker.RainbowMaker()
            self.run_server() #start running the server
        #==============================================================================================================
        #FUNCTIONS
        #==============================================================================================================
        #--------------------------------------------------------------------------------------------------
        #runserver function
        #--------------------------------------------------------------------------------------------------

        def run_server(self):  # the primary server loop
            print "run server"
            print "NETWORK SERVER DEBUG: in run_server function" #Added by Chris Hamm, a more useful print statement
            start_time = time.time()
            try:  # runserver definition try block
                #if running in single mode, set shared queues and then start the process
                if self.single_user_mode:
                    print "Single User Mode"
                    shared_job_q = Queue(100)
                    shared_result_q = Queue()
                    single = Process(target=self.start_single_user, args=(shared_job_q, shared_result_q,))
                    single.start()

                else:
                    #if not in single mode
                    print "Network Server Mode"
                    # Start a shared manager server and access its queues
                    #TODO why are shared variables set for single user mode (above) but nothing is done for network server mode (here)

                # Spawn processes to feed the job queue and monitor the result queue
                if self.cracking_mode == "dic": #if running dictionary mode, create new dictionary, set up settings, start new process

                    dictionary = Dictionary.Dictionary()
                    dictionary.setAlgorithm(self.settings["algorithm"])
                    dictionary.setFileName(self.settings["file name"])
                    dictionary.setHash(self.settings["hash"])
                    self.found_solution.value = False
                    #TODO INCONSISTANT why is this (line below) only commented out for dictionary???
                    #self.total_chunks = dictionary.get_total_chunks()
                    self.shared_dict["total chunks"] = self.total_chunks
                    chunk_maker = Process(target=self.chunk_dictionary, args=(dictionary,self.shutdown))
                elif self.cracking_mode == "bf":

                    bf = Brute_Force.Brute_Force()
                    bf.set_params(alphabet=self.settings["alphabet"],
                                  algorithm=self.settings["algorithm"],
                                  origHash=self.settings["hash"],
                                  min_key_length=self.settings["min key length"],
                                  max_key_length=self.settings["max key length"])
                    #TODO INCONSISTANT why is this line commented out for dictionary, but not here???????
                    self.total_chunks = bf.get_total_chunks()
                    self.shared_dict["total chunks"] = self.total_chunks
                    chunk_maker = Process(target=self.chunk_brute_force, args=(bf, self.shutdown))
                elif self.cracking_mode == "rain":


                    rain = RainbowUser.RainbowUser()
                    rain.setFileName(self.settings["file name"])
                    rain.setHash(self.settings["hash"])
                    rain.gatherInfo()
                    #TODO INCONSISTANT why is this line commented out for dictionary, but not here???????
                    self.total_chunks = rain.get_total_chunks()
                    self.shared_dict["total chunks"] = self.total_chunks
                    chunk_maker = Process(target=self.chunk_rainbow, args=(rain, self.shutdown))

                elif self.cracking_mode == "rainmaker":

                    rainmaker = self.rainmaker

                    rainmaker.setAlgorithm(self.settings['algorithm'])
                    rainmaker.setNumChars(self.settings['key length'])
                    rainmaker.setAlphabet(self.settings['alphabet'])
                    rainmaker.setDimensions(self.settings['chain length'], self.settings['num rows'])
                    rainmaker.setFileName(self.settings['file name'])
                    rainmaker.setupFile()
                    #TODO INCONSISTANT why is this line commented out for dictionary, but not here???????
                    self.total_chunks = rainmaker.get_total_chunks()
                    self.shared_dict["total chunks"] = self.total_chunks
                    chunk_maker = Process(target=self.chunk_rainbow_maker, args=(rainmaker, self.shutdown))

                else:
                    return "wtf?"

                chunk_maker.start()

                chunk_maker.join()
                chunk_maker.terminate()
                if chunk_maker.is_alive():
                    print "oh no!"
                    print "NETWORKSERVER DEBUG: chunk_maker is alive" #Added by c hamm, a more useful print statement

                self.update.set()


            except Exception as inst:
                print "============================================================================================="
                print "ERROR: An exception was thrown in runserver definition Try block"
                #the exception instance
                print type(inst)
                #arguments stored in .args
                print inst.args
                #_str_ allows args tto be printed directly
                print inst
                print "============================================================================================="
            finally:
                end_time= time.time() - start_time
                print "Server ran for "+str(end_time)+" seconds"
                return

        #--------------------------------------------------------------------------------------------------
        #End of runserver function
        #--------------------------------------------------------------------------------------------------

        def get_job_queue(self):
            return self.job_queue

        def get_result_queue(self):
            return self.result_queue

        def get_shutdown(self):
            return self.shutdown

        def get_mode_bit_1(self):
            return self.mode_bit_1

        def get_mode_bit_2(self):
            return self.mode_bit_2

        #--------------------------------------------------------------------------------------------------
        # monitor results queue
        #--------------------------------------------------------------------------------------------------
        def check_results(self, results_queue, shutdown): #TODO naming conflict, shutdown is also a global variable
            print "check results started"
            completed_chunks = 0
            try:
                while not shutdown.is_set(): #TODO INCONSISTANT: doesnt match the (inconsistant) while not shut down loops in dictionary
                    try:
                        self.update.set()
                        result = results_queue.get(block=True, timeout=.1)  # get chunk from shared result queue
                    except Qqueue.Empty:
                        continue
                    if result[0] == "w":  # check to see if solution was found
                        print "The solution was found!"
                        shutdown.set()
                        print "shutdown notice sent to clients"
                        key = result[1]
                        self.found_solution.value = True
                        print "Key is: %s" % key
                        self.shared_dict["finished chunks"] += 1
                        self.shared_dict["key"] = key
                        self.update.set()

                    elif(result[0] == "c"):  # check to see if client has crashed
                        print "A client has crashed!"  # THIS FUNCTION IS UNTESTED
                    elif result[0] == "e":
                        print "Final chunk processed, no solution found."
                        shutdown.set()
                        self.shared_dict["finished chunks"] += 1
                        break
                    else:  # solution has not been found
                        completed_chunks += 1
                        self.shared_dict["finished chunks"] += 1
                        #print "Chunk finished with params: %s" %result[1]
                        os.system('cls' if os.name == 'nt' else 'clear')
                        print "%d chunks completed." % completed_chunks
                        # go through the sent chunks list and remove the finished chunk

                        if self.cracking_mode == "rainmaker":
                            rainChunk = result[1]

                            self.rainmaker.putChunkInFile(rainChunk)
                            if self.rainmaker.isDone():
                                print "Table complete and stored in file '%s'." % self.rainmaker.getFileName()
                                shutdown.set() #TODO are you setting the correct shutdown???
                                return

            except Exception as inst:
                print "============================================================================================="
                print "ERROR: An exception was thrown in check_results definition Try block"
                #the exception instance
                print type(inst)
                #arguments stored in .args
                print inst.args
                #_str_ allows args tto be printed directly
                print inst
                print "============================================================================================="
        #--------------------------------------------------------------------------------------------------
        #end of monitor results queue
        #--------------------------------------------------------------------------------------------------

        #--------------------------------------------------------------------------------------------------
        # feed dictionary chunks to job queue
        #--------------------------------------------------------------------------------------------------
        def chunk_dictionary(self, dictionary, shutdown):  #TODO naming conflict, shutdown is also a global variable
            try:

                if not self.single_user_mode:
                    JobQueueManager.register('get_job_q', callable=self.get_job_queue)
                    JobQueueManager.register('get_result_q', callable=self.get_result_queue)
                    JobQueueManager.register('get_shutdown', callable=self.get_shutdown)
                    JobQueueManager.register('get_mode_bit_1', callable=self.get_mode_bit_1)
                    JobQueueManager.register('get_mode_bit_2', callable=self.get_mode_bit_2)
                    manager = JobQueueManager(address=(self.IP, self.PORTNUM), authkey=self.AUTHKEY)
                    manager.start()
                    job_queue = manager.get_job_q()  #TODO naming conflict, job_queue is alos a global variable
                    result_queue = manager.get_result_q() #TODO naming conflict, result_queue is also a global variable
                    mode_bit_1 = manager.get_mode_bit_1()
                    mode_bit_2 = manager.get_mode_bit_2()
                    mode_bit_1.set()
                    mode_bit_2.set()
                else:
                    job_queue = self.job_queue  #TODO creating another variable (with the same name) that hols the same data as the global variable
                    result_queue = self.result_queue  #TODO creating another variable (with the same name) that holds the same data as the global variable
                result_monitor = Process(target=self.check_results, args=(result_queue, shutdown))
                result_monitor.start()
                import time
                while not dictionary.isEof() and not self.found_solution.value:  # Keep looping while it is not eof
                    #chunk is a Chunk object
                    chunk = dictionary.getNextChunk()  # get next chunk from dictionary
                    if self.single_user_mode:
                        while not self.shutdown.is_set(): #TODO INCONSISTANT: this uses the global shutdown variable
                                                            #TODO while loop below uses the parameter shutdown variable
                            try:
                                self.shared_dict["current chunk"] = chunk
                                job_queue.put(chunk)
                                break
                            except Qqueue.Full:
                                continue
                    else:
                        new_chunk = manager.Value(dict, {'params': chunk.params,
                                                         'data': chunk.data,
                                                         'timestamp': time.time(),
                                                         'halt': False})
                        while not shutdown.is_set():  #TODO INCONSISTANT: this uses the parameter shutdown variable
                                                        #TODO while loop above uses the global shutdown variable
                            try:
                                #self.shared_dict["current chunk"] = new_chunk
                                job_queue.put(new_chunk, timeout=.1)
                                #add params to list of sent chunks along with a timestamp so we can monitor which ones come back
                                self.sent_chunks.append((chunk.params, time.time()))
                                break
                            except Qqueue.Full:
                                continue

                        self.sent_chunks.append((chunk.params, time.time()))
                    if dictionary.isEof():
                        break
                if self.found_solution.value:
                    while True:
                        try:
                            job_queue.get_nowait()
                        except Qqueue.Empty:
                            return
                result_monitor.join()
                result_monitor.terminate()
                time.sleep(2)
                manager.shutdown()
            except Exception as inst:
                print "============================================================================================="
                print "ERROR: An exception was thrown in chunk_dictionary definition Try block"
                #the exception instance
                print type(inst)
                #arguments stored in .args
                print inst.args
                #_str_ allows args tto be printed directly
                print inst
                print "============================================================================================="
        #--------------------------------------------------------------------------------------------------
        #end of feed dictionary chunks to job queue
        #--------------------------------------------------------------------------------------------------

        #--------------------------------------------------------------------------------------------------
        # Chunk for brute force function
        #--------------------------------------------------------------------------------------------------
        def chunk_brute_force(self, bf, shutdown):  #TODO naming conflict, shutdown is also a global variable
            try:
                if not self.single_user_mode:
                    JobQueueManager.register('get_job_q', callable=self.get_job_queue)
                    JobQueueManager.register('get_result_q', callable=self.get_result_queue)
                    JobQueueManager.register('get_shutdown', callable=self.get_shutdown)
                    JobQueueManager.register('get_mode_bit_1', callable=self.get_mode_bit_1)
                    JobQueueManager.register('get_mode_bit_2', callable=self.get_mode_bit_2)
                    manager = JobQueueManager(address=(self.IP, self.PORTNUM), authkey=self.AUTHKEY)
                    manager.start()
                    job_queue = manager.get_job_q()  #TODO naming conflict, job_queue is alos a global variable
                    result_queue = manager.get_result_q()  #TODO naming conflict, result_queue is also a global variable
                    mode_bit_1 = manager.get_mode_bit_1()
                    mode_bit_2 = manager.get_mode_bit_2()
                    mode_bit_1.set()
                    mode_bit_2.clear()

                else:
                    result_queue = self.result_queue  #TODO creating another variable (with the same name) that holds the same data as the global variable
                    job_queue = self.job_queue  #TODO creating another variable (with the same name) that hols the same data as the global variable

                result_monitor = Process(target=self.check_results, args=(result_queue, shutdown))
                result_monitor.start()
                for prefix in bf.get_prefix():
                    if prefix == '':
                        prefix = "-99999999999999999999999999999999999"
                    params = "bruteforce\n" + bf.algorithm + "\n" + bf.origHash + "\n" + bf.alphabet + "\n" \
                             + str(bf.minKeyLength) + "\n" + str(bf.maxKeyLength) + "\n" + prefix + "\n0\n0\n0"
                    #print params
                    if self.single_user_mode: #if in single mode
                        new_chunk = Chunk.Chunk()
                        new_chunk.params = params
                    else: #if in network mode
                        new_chunk = manager.Value(dict, {'params': params,
                                                         'data': '',
                                                         'timestamp': time.time(),
                                                         'halt': False})
                    while not shutdown.is_set(): #TODO INCONSISTANT: does not match the (inconsistant) while not shutdown loops in dictionary
                                                #TODO this uses the parameter shutdown variable
                        try:
                            job_queue.put(new_chunk, timeout=.25)  # put next chunk on the job queue.
                            self.sent_chunks.append((params, time.time()))
                            break
                        except Qqueue.Full:
                            continue
                    if self.found_solution.value:
                        while True:
                            try:
                                job_queue.get_nowait()
                            except Qqueue.Empty:
                                return
                            finally:
                                result_monitor.terminate()
                                time.sleep(2)
                                manager.shutdown()

                                return

            except Exception as inst:
                print "============================================================================================="
                print "ERROR: An exception was thrown in chunk_brute_force definition Try block"
                #the exception instance
                print type(inst)
                #arguments stored in .args
                print inst.args
                #_str_ allows args tto be printed directly
                print inst
                print "============================================================================================="
        #--------------------------------------------------------------------------------------------------
        #end of chunk for brute force function
        #--------------------------------------------------------------------------------------------------

        #--------------------------------------------------------------------------------------------------
        # Chunks for rainbow function
        #--------------------------------------------------------------------------------------------------
        def chunk_rainbow(self, rainbow, shutdown): #TODO naming conflict, shutdown is also a global variable
            try:
                if not self.single_user_mode: #if in network mode (THIS IS UNUSUAL, single is always dealt with first elsewhere)
                    JobQueueManager.register('get_job_q', callable=self.get_job_queue)
                    JobQueueManager.register('get_result_q', callable=self.get_result_queue)
                    JobQueueManager.register('get_shutdown', callable=self.get_shutdown)
                    JobQueueManager.register('get_mode_bit_1', callable=self.get_mode_bit_1)
                    JobQueueManager.register('get_mode_bit_2', callable=self.get_mode_bit_2)
                    manager = JobQueueManager(address=(self.IP, self.PORTNUM), authkey=self.AUTHKEY)
                    manager.start()
                    job_queue = manager.get_job_q()  #TODO naming conflict, job_queue is alos a global variable
                    result_queue = manager.get_result_q()   #TODO naming conflict, result_queue is also a global variable
                    mode_bit_1 = manager.get_mode_bit_1()
                    mode_bit_2 = manager.get_mode_bit_2()
                    mode_bit_1.clear()
                    mode_bit_2.set()
                else: #if in single mode
                    result_queue = self.result_queue  #TODO creating another variable (with the same name) that holds the same data as the global
                    job_queue = self.job_queue  #TODO creating another variable (with the same name) that hols the same data as the global variable
                result_monitor = Process(target=self.check_results, args=(result_queue, shutdown))
                result_monitor.start()
                while not rainbow.isEof() and not shutdown.is_set(): #TODO INCONSISTANT: doesnt match the (inconsistant) while not shut down loops in dictionary
                    chunk = rainbow.getNextChunk()
                    if self.single_user_mode: #if in single mode
                        while True:
                            try:
                                self.shared_dict["current chunk"] = chunk
                                job_queue.put(chunk, timeout=.1)
                                break
                            except Qqueue.Full:
                                continue
                    else:
                        new_chunk = manager.Value(dict, {'params': chunk.params,
                                                         'data': chunk.data,
                                                         'timestamp': time.time()})
                        while not shutdown.is_set(): #TODO INCONSISTANT: doesnt match the (inconsistant) while not shut down loops in dictionary
                            try:
                                self.shared_dict["current chunk"] = new_chunk
                                job_queue.put(new_chunk, timeout=.1)
                                self.sent_chunks.append((chunk.params, time.time()))
                                break
                            except Qqueue.Full:
                                continue
                    if shutdown.is_set(): #TODO INCONSISTANT: doesnt match the (inconsistant) while not shut down loops in dictionary
                        print "chunker trying to shut down"
                        while True:
                            try:
                                job_queue.get_nowait()
                            except Qqueue.Empty:
                                return
                            finally:
                                time.sleep(2)
                                manager.shutdown()
                                return

            except Exception as inst:
                print "============================================================================================="
                print "ERROR: An exception was thrown in chunk_rainbow definition Try block"
                #the exception instance
                print type(inst)
                #arguments stored in .args
                print inst.args
                #_str_ allows args tto be printed directly
                print inst
                print "============================================================================================="
        #--------------------------------------------------------------------------------------------------
        #end of chunks for rainbow function
        #--------------------------------------------------------------------------------------------------

        #--------------------------------------------------------------------------------------------------
        # chunks for rainbow maker function
        #--------------------------------------------------------------------------------------------------
        def chunk_rainbow_maker(self, rainmaker, shutdown): #TODO naming conflict, shutdown is also a global variable
            try:
                if not self.single_user_mode:
                    JobQueueManager.register('get_job_q', callable=self.get_job_queue)
                    JobQueueManager.register('get_result_q', callable=self.get_result_queue)
                    JobQueueManager.register('get_shutdown', callable=self.get_shutdown)
                    JobQueueManager.register('get_mode_bit_1', callable=self.get_mode_bit_1)
                    JobQueueManager.register('get_mode_bit_2', callable=self.get_mode_bit_2)
                    manager = JobQueueManager(address=(self.IP, self.PORTNUM), authkey=self.AUTHKEY)
                    manager.start()
                    job_queue = manager.get_job_q()  #TODO naming conflict, job_queue is alos a global variable
                    result_queue = manager.get_result_q()  #TODO naming conflict, result_queue is also a global variable
                    mode_bit_1 = manager.get_mode_bit_1()
                    mode_bit_2 = manager.get_mode_bit_2()
                    mode_bit_1.clear()
                    mode_bit_2.clear()
                else:
                    result_queue = self.result_queue  #TODO creating another variable (with the same name) that holds the same data as the global
                    job_queue = self.job_queue  #TODO creating another variable (with the same name) that hols the same data as the global variable

                result_monitor = Process(target=self.check_results, args=(result_queue, shutdown))
                result_monitor.start()

                while not shutdown.is_set(): #TODO INCONSISTANT: doesnt match the (inconsistant) while not shut down loops in dictionary
                    params_chunk = rainmaker.makeParamsChunk()
                    new_chunk = {"params": params_chunk.params,
                                 "data": params_chunk.data}
                    try:
                        job_queue.put(new_chunk, timeout=.1)
                    except Qqueue.Full:
                        continue
                    if shutdown.is_set(): #TODO INCONSISTANT: doesnt match the (inconsistant) while not shut down loops in dictionary
                        while True:
                            try:
                                job_queue.get_nowait()
                            except Qqueue.Empty:
                                return
                            finally:
                                time.sleep(2)
                                manager.shutdown()
                                return
            except Exception as inst:
                print "============================================================================================="
                print "ERROR: An exception was thrown in chunk_rainbow_maker definition Try block"
                #the exception instance
                print type(inst)
                #arguments stored in .args
                print inst.args
                #_str_ allows args tto be printed directly
                print inst
                print "============================================================================================="
        #--------------------------------------------------------------------------------------------------
        #end of chunks for rainbow maker function
        #--------------------------------------------------------------------------------------------------

        def get_ip(self):
                    #detect the OS
                try:  # getOS try block
                    print "*************************************"
                    print "    Network Server"
                    print "*************************************"
                    print "OS DETECTION:"
                    if platform.system() == "Windows":  # Detecting Windows
                        print platform.system()
                        print platform.win32_ver()
                    elif platform.system() == "Linux":  # Detecting Linux
                        print platform.system()
                        print platform.dist()
                    elif platform.system() == "Darwin":  # Detecting OSX
                        print platform.system()
                        print platform.mac_ver()
                    else:                           # Detecting an OS that is not listed
                        print platform.system()
                        print platform.version()
                        print platform.release()
                    print "*************************************"
                except Exception as inst:
                    print "========================================================================================"
                    print "ERROR: An exception was thrown in getOS try block"
                    print type(inst)  # the exception instance
                    print inst.args  # arguments stored in .args
                    print inst  # _str_ allows args tto be printed directly
                    print "========================================================================================"
                #end of detect the OS

                #get the IP address
                try:  # getIP tryblock
                    print "STATUS: Getting your network IP address"
                    if platform.system() == "Windows":
                        self.IP= socket.gethostbyname(socket.gethostname())
                        print "My IP Address: " + str(self.IP)
                    elif platform.system() == "Linux":
                        #Source: http://stackoverflow.com/questions/11735821/python-get-localhost-ip
                        #Claims that this works on linux and windows machines
                        import fcntl
                        import struct
                        import os

                        def get_interface_ip(ifname):
                            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                            return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915,
                                                                struct.pack('256s', ifname[:15]))[20:24])

                        #end of def
                        def get_lan_ip():
                            ip = socket.gethostbyname(socket.gethostname())
                            if ip.startswith("127.") and os.name != "nt":
                                interfaces = ["eth0", "eth1", "eth2", "wlan0", "wlan1", "wifi0", "ath0", "ath1", "ppp0"]
                                for ifname in interfaces:
                                    try:
                                        ip = get_interface_ip(ifname)
                                        print "IP address was retrieved from the " + str(ifname) + " interface."
                                        break
                                    except IOError:
                                        pass
                            return ip
                        #end of def
                        self.IP= get_lan_ip()
                        print "My IP Address: " + str(self.IP)
                    elif platform.system() == "Darwin":
                        self.IP = socket.gethostbyname(socket.gethostname())
                        print "My IP Address: " + str(self.IP)
                    else:
                        #NOTE: MAY REMOVE THIS AND REPLACE WITH THE LINUX DETECTION METHOD
                        print "INFO: The system has detected that you are not running Windows, OS X, or Linux."
                        print "INFO: System is using a generic IP detection method"
                        self.IP = socket.gethostbyname(socket.gethostname())
                        print "My IP Address: " + str(self.IP)
                except Exception as inst:
                    print "========================================================================================"
                    print "ERROR: An exception was thrown in getIP try block"
                    print type(inst)  # the exception instance
                    print inst.args  # arguments stored in .args
                    print inst  # _str_ allows args tto be printed directly
                    print "========================================================================================"
                #end of get the IP address

        def start_single_user(self, job_queue, result_queue):  #TODO name conflict result_queue os also the name of the global variable
                                                               #TODO name conflict job_queue is also the name of the global variable
            print "Single User Mode"
            try:  # start_single_user definition try block

                chunk_runner = []
                if self.cracking_mode == "dic":
                    print "Starting dictionary cracking."
                    dictionary = Dictionary.Dictionary()
                    for i in range(0, 3):
                        chunk_runner.append(Process(target=self.run_dictionary,
                                                    args=(dictionary, job_queue, result_queue)))

                else:   #NOTE: why not use elif statements here???
                    if self.cracking_mode == "bf":
                        print "Starting brute force cracking."
                        bf = Brute_Force.Brute_Force()

                        chunk_runner.append(Process(target=self.run_brute_force,
                                                    args=(bf, job_queue, result_queue)))
                    else:
                        if self.cracking_mode == "rain":
                            print "Starting rainbow table cracking."
                            rainbow = RainbowUser.RainbowUser()

                            chunk_runner.append(Process(target=self.run_rain_user,
                                                        args=(rainbow, job_queue, result_queue)))
                        else:
                            if self.cracking_mode == "rainmaker":
                                print "Starting rainbow table generator."
                                rainmaker = RainbowMaker.RainbowMaker()

                                chunk_runner.append(Process(target=self.run_rain_maker,
                                                            args=(rainmaker, job_queue, result_queue)))
                            else:
                                return "wtf?"
                for process in chunk_runner:
                    process.start()
                for process in chunk_runner:
                    process.join()
                if self.shutdown.is_set(): #TODO INCONSISTANT: doesnt match the (inconsistant) while not shut down loops in dictionary
                    print "received shutdown notice from server."
                    for process in chunk_runner:
                        process.terminate()
            except Exception as inst:
                print "============================================================================================="
                print "ERROR: An exception was thrown in start_single_user definition try block"
                #the exception instance
                print type(inst)
                #arguments stored in .args
                print inst.args
                #_str_ allows args tto be printed directly
                print inst
                print "============================================================================================="

        def run_dictionary(self, dictionary, job_queue, result_queue): #TODO name conflict result_queue os also the name of the global variable
                                                                       #TODO name conflict job_queue is also the name of the global variable
            try:
                while not self.shutdown.is_set(): #TODO INCONSISTANT: doesnt match the (inconsistant) while not shut down loops in dictionary (not this dict)
                    try:
                        chunk = job_queue.get(block=True, timeout=.25)  # block for at most .25 seconds, then loop again
                    except Qqueue.Empty:
                        continue
                    dictionary.find(chunk)
                    result = dictionary.isFound()
                    params = chunk.params.split()
                    if result:
                        key = dictionary.showKey()
                        result_queue.put(("w", key))
                    elif params[10] == "True":  #Does this comparison check actually work?? (it has caused problems for me)
                        result_queue.put(("e", chunk.params))
                    else:
                        result_queue.put(("f", chunk.params))
                            #result_q.put(("c", chunk.params)) #unction has never been tested
            except Exception as inst:
                print "============================================================================================="
                print "ERROR: An exception was thrown in run_dictionary definition try block"
                #the exception instance
                print type(inst)
                #arguments stored in .args
                print inst.args
                #_str_ allows args tto be printed directly
                print inst
                print "============================================================================================="

        def run_brute_force(self, bf, job_queue, result_queue):  #TODO name conflict result_queue os also the name of the global variable
                                                                #TODO name conflict job_queue is also the name of the global variable
            try:
                bf.result_queue = result_queue   #TODO name conflict result_queue os also the name of the global variable

                while not self.shutdown.is_set(): #TODO INCONSISTANT: doesnt match the (inconsistant) while not shut down loops in dictionary
                    try:
                        chunk = job_queue.get(timeout=.1)
                    except Qqueue.Empty:
                        continue
                    bf.run_chunk(chunk)
                    bf.start_processes()

            except Exception as inst:
                print "============================================================================================="
                print "ERROR: An exception was thrown in run_brute_force definition try block"
                #the exception instance
                print type(inst)
                #arguments stored in .args
                print inst.args
                #_str_ allows args tto be printed directly
                print inst
                print "============================================================================================="
            finally:
                bf.terminate_processes()

        def run_rain_user(self, rain, job_queue, result_queue):  #TODO name conflict result_queue os also the name of the global variable
                                                                #TODO name conflict job_queue is also the name of the global variable
            while not self.shutdown.is_set(): #TODO INCONSISTANT: doesnt match the (inconsistant) while not shut down loops in dictionary
                try:
                    chunk = job_queue.get(block=True, timeout=.25)
                except Qqueue.Empty:
                    continue
                rain.find(chunk)
                if rain.isFound():
                    result_queue.put(("w", rain.getKey()))
                elif chunk.params.split()[10] == "True": #Are we sure this comparison check actually works??? (it hasnt worked for me in the past)
                    result_queue.put(("e", chunk.params))
                else:
                    result_queue.put(("f", chunk.params))

        def run_rain_maker(self, maker, job_queue, result_queue):  #TODO name conflict result_queue os also the name of the global variable
                                                                    #TODO name conflict job_queue is also the name of the global variable
            while not self.shutdown.is_set(): #TODO INCONSISTANT: doesnt match the (inconsistant) while not shut down loops in dictionary
                params_chunk = Chunk.Chunk()
                try:
                    job = job_queue.get(block=True, timeout=.25)
                except Qqueue.Empty:
                    continue
                params_chunk.params = job["params"]
                finished_chunk = maker.create(params_chunk)
                result_queue.put(('f', finished_chunk))

        #Returns a list of hashes from the hash file
        def get_hashes_from_file(self, file_name):

            temp_file = open(file_name, "r")

            list_of_hashes = list(temp_file)

            temp_file.close()

            return list_of_hashes

        #=======================================4=======================================================================
        #END OF FUNCTIONS
        #===============================================================================================================

        #===============================================================================================================
        #AUXILLERY CLASSES
        #===============================================================================================================

         # This is based on the examples in the official docs of multiprocessing.
            # get_{job|result}_q return synchronized proxies for the actual Queue
            # objects.


        #===============================================================================================================
        #END OF AUXILIARY CLASSES
        #===============================================================================================================


class JobQueueManager(SyncManager):
    pass
