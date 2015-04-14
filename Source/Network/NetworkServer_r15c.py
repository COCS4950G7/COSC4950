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
        debug_file = "/Users/327pzq/procs.txt"

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
            #print "DEBUG: cracking method="+str(settings["cracking method"])
            #print "DEBUG: algorithm="+str(settings["algorithm"])
            #print "DEBUG: hash="+str(settings["hash"])
            #print "DEBUG: min key length="+str(settings["min key length"])
            #print "DEBUG: max key length="+str(settings["max key length"])
            #print "DEBUG: alphabet="+str(settings["alphabet"])
            #print "DEBUG: single="+str(settings["single"])

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
            start_time = time.time()
            try:  # runserver definition try block
                if self.single_user_mode:
                    print "Single User Mode"
                else:
                    print "Network Server Mode"

                # Spawn processes to feed the job queue and monitor the result queue
                if self.cracking_mode == "dic": #if running dictionary mode, create new dictionary, set up settings, start new process

                    dictionary = Dictionary.Dictionary()
                    dictionary.setAlgorithm(self.settings["algorithm"])
                    dictionary.setFileName(self.settings["file name"])
                    dictionary.setHash(self.settings["hash"])
                    self.found_solution.value = False
                    self.total_chunks = dictionary.get_total_chunks()
                    self.shared_dict["total chunks"] = self.total_chunks
                    chunk_maker = Process(target=self.chunk_dictionary, args=(dictionary, self.shutdown))

                elif self.cracking_mode == "bf":
                    self.found_solution.value = False
                    bf = Brute_Force.Brute_Force()
                    bf.set_params(alphabet=self.settings["alphabet"],
                                  algorithm=self.settings["algorithm"],
                                  origHash=self.settings["hash"],
                                  min_key_length=self.settings["min key length"],
                                  max_key_length=self.settings["max key length"])

                    self.total_chunks = bf.get_total_chunks()
                    self.shared_dict["total chunks"] = self.total_chunks
                    chunk_maker = Process(target=self.chunk_brute_force, args=(bf, self.shutdown))

                elif self.cracking_mode == "rain":
                    self.found_solution.value = False
                    rain = RainbowUser.RainbowUser()
                    rain.setFileName(self.settings["file name"])
                    rain.setHash(self.settings["hash"])
                    rain.gatherInfo()
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
                    self.total_chunks = rainmaker.get_total_chunks()
                    self.shared_dict["total chunks"] = self.total_chunks
                    chunk_maker = Process(target=self.chunk_rainbow_maker, args=(rainmaker, self.shutdown))

                else:
                    return "wtf?"

                chunk_maker.start()
                #print "chunk maker pid: %i" % chunk_maker.pid
                chunk_maker.join()
                #chunk_maker.terminate()
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
        def check_results(self, results_queue, shutdown):
            current_process().authkey = "Popcorn is awesome!!!"
            #print "check results started"
            completed_chunks = 0
            try:
                while not shutdown.is_set():
                    try:
                        self.update.set()
                        result = results_queue.get(block=True, timeout=.25)
                    except Qqueue.Empty:
                        continue
                    #print "chunk done, result: %s" % result[0]
                    #print "params: %s" % result[1]
                    if result[0] == "w":  # check to see if solution was found
                        print "The solution was found!"
                        shutdown.set()
                        self.shutdown.set()
                        print "shutdown notice sent to clients"
                        key = result[1]
                        self.found_solution.value = True
                        print "Key is: %s" % key
                        self.shared_dict["finished chunks"] += 1
                        self.shared_dict["key"] = key
                        self.update.set()
                        #print "win block finished"
                        #print "result monitor process: %i" % current_process().pid
                        #print "result monitor parent process: %i" % current_process()._parent_pid
                        time.sleep(2)
                        try:
                            os.kill(current_process().pid-1, signal.SIGKILL)
                        except Exception:
                            print
                            #print "process %i is already dead." % current_process().pid-1
                        try:
                            os.kill(current_process()._parent_pid, signal.SIGKILL)
                        except Exception:
                            print
                            #print "process %i is already dead." % current_process()._parent_pid
                        try:
                            os.kill(current_process().pid, signal.SIGKILL)
                        except Exception:
                            print
                            #print "process %i is already dead." % current_process().pid
                        break
                    elif(result[0] == "c"):  # check to see if client has crashed
                        print "A client has crashed!"  # THIS FUNCTION IS UNTESTED
                        break
                    elif result[0] == "e":
                        print "Final chunk processed, no solution found."
                        shutdown.set()
                        self.shutdown.set()
                        self.shared_dict["finished chunks"] += 1
                        time.sleep(2)
                        try:
                            os.kill(current_process().pid-1, signal.SIGKILL)
                        except Exception:
                            print
                            #print "process %i is already dead." % current_process().pid-1
                        try:
                            os.kill(current_process()._parent_pid, signal.SIGKILL)
                        except Exception:
                            print
                            #print "process %i is already dead." % current_process()._parent_pid
                        try:
                            os.kill(current_process().pid, signal.SIGKILL)
                        except Exception:
                            print
                            #print "process %i is already dead." % current_process().pid
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
                                shutdown.set()
                                self.shutdown.set()
                                self.found_solution = True
                                time.sleep(2)
                                try:
                                    os.kill(current_process().pid-1, signal.SIGKILL)
                                except Exception:
                                    print
                                    #print "process %i is already dead." % current_process().pid-1
                                try:
                                    os.kill(current_process()._parent_pid, signal.SIGKILL)
                                except Exception:
                                    print
                                    #print "process %i is already dead." % current_process()._parent_pid
                                try:
                                    os.kill(current_process().pid, signal.SIGKILL)
                                except Exception:
                                    print
                                    #print "process %i is already dead." % current_process().pid
                                break

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
        def chunk_dictionary(self, dictionary, shutdown):
            try:
                if not self.single_user_mode:  # setup a networked manager
                    # register shared variables
                    JobQueueManager.register('get_job_q', callable=self.get_job_queue)
                    JobQueueManager.register('get_result_q', callable=self.get_result_queue)
                    JobQueueManager.register('get_shutdown', callable=self.get_shutdown)
                    JobQueueManager.register('get_mode_bit_1', callable=self.get_mode_bit_1)
                    JobQueueManager.register('get_mode_bit_2', callable=self.get_mode_bit_2)
                    # set server's IP and port number
                    manager = JobQueueManager(address=(self.IP, self.PORTNUM), authkey=self.AUTHKEY)
                    manager.start()  # start the server
                    #get the shared variables from the manager
                    job_queue = manager.get_job_q()
                    result_queue = manager.get_result_q()
                    mode_bit_1 = manager.get_mode_bit_1()
                    mode_bit_2 = manager.get_mode_bit_2()
                    #set cracking mode
                    mode_bit_1.set()
                    mode_bit_2.set()
                else:
                    manager = None  # no manager needed for local cracking
                    job_queue = self.job_queue
                    result_queue = self.result_queue
                    #start the single user process which starts the correct run method
                    single = Process(target=self.start_single_user, args=(self.job_queue, self.result_queue,))
                    single.start()
                #start the result monitor process which reads finished chunks off the result queue
                result_monitor = Process(target=self.check_results, args=(result_queue, shutdown))
                result_monitor.start()
                import time
                while not dictionary.isEof() and not self.shutdown.is_set():  # Keep looping while it is not eof
                    #chunk is a Chunk object
                    chunk = dictionary.getNextChunk()  # get next chunk from dictionary
                    #Retrieves word from chunk
                    temp_word = self.extract_word(chunk)
                    #Shares a 'current' word with UIs for display
                    self.shared_dict["current word"] = temp_word
                    if self.single_user_mode:
                        while not self.shutdown.is_set():
                            try:
                                #single node mode can just push a chunk object onto the queue
                                job_queue.put(chunk, timeout=.1)
                                break
                            except Qqueue.Full:
                                continue
                    else:
                        #chunks don't work across the network, use a dictionary instead
                        new_chunk = {'params': chunk.params,
                                     'data': chunk.data,
                                     'timestamp': time.time(),
                                     'halt': False}
                        while not self.shutdown.is_set():
                            try:
                                job_queue.put(new_chunk, timeout=.1)
                                #add params to list of sent chunks along with a timestamp
                                self.sent_chunks.append((chunk.params, time.time()))
                                break
                            except Qqueue.Full:
                                continue

                        self.sent_chunks.append((chunk.params, time.time()))
                    if dictionary.isEof():
                        break
                    if self.shutdown.is_set():
                        while True:
                            try:
                                job_queue.get_nowait()
                            except Qqueue.Empty:
                                break
                result_monitor.join()
                #result_monitor.terminate()
                if manager is not None:
                    manager.shutdown()

                time.sleep(1)
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
        def chunk_brute_force(self, bf, shutdown):
            try:
                current_process()._authkey = self.AUTHKEY
                if not self.single_user_mode:  # setup a networked manager
                    # register shared variables
                    JobQueueManager.register('get_job_q', callable=self.get_job_queue)
                    JobQueueManager.register('get_result_q', callable=self.get_result_queue)
                    JobQueueManager.register('get_shutdown', callable=self.get_shutdown)
                    JobQueueManager.register('get_mode_bit_1', callable=self.get_mode_bit_1)
                    JobQueueManager.register('get_mode_bit_2', callable=self.get_mode_bit_2)
                    # set server's IP and port number
                    manager = JobQueueManager(address=(self.IP, self.PORTNUM), authkey=self.AUTHKEY)
                    manager.start()  # start the server
                    #get the shared variables from the manager
                    result_queue = manager.get_result_q()
                    job_queue = manager.get_job_q()
                    mode_bit_1 = manager.get_mode_bit_1()
                    mode_bit_2 = manager.get_mode_bit_2()
                    #set cracking mode
                    mode_bit_1.set()
                    mode_bit_2.clear()
                    result_monitor = Process(target=self.check_results, args=(result_queue, shutdown))
                else:
                    manager = None  # no manager needed for local cracking
                    job_queue = self.job_queue
                    result_monitor = Process(target=self.check_results, args=(self.result_queue, shutdown))
                    #start the single user process which starts the correct run method
                    single = Process(target=self.start_single_user, args=(self.job_queue, self.result_queue,))
                    single.start()
                result_monitor.start()
                for prefix in bf.get_prefix():
                    if prefix == '':
                        prefix = "-99999999999999999999999999999999999"  # sentinel for keys shorter than chars_to_check
                    else:
                        #Shares a 'current' word with UIs for display
                        self.shared_dict["current word"] = prefix
                    if prefix == "******possibilities exhausted******":
                        prefix = "******possibilities exhausted******"
                    params = "bruteforce\n" + bf.algorithm + "\n" + bf.origHash + "\n" + bf.alphabet + "\n" \
                             + str(bf.minKeyLength) + "\n" + str(bf.maxKeyLength) + "\n" + prefix + "\n0\n0\n0"
                    #print params
                    if self.single_user_mode: #if in single mode
                        new_chunk = Chunk.Chunk()
                        new_chunk.params = params
                    else: #if in network mode
                        new_chunk = {'params': params,
                                     'data': '',
                                     'timestamp': time.time(),
                                     'halt': False}
                    while not shutdown.is_set():
                        try:
                            job_queue.put(new_chunk, timeout=.1)  # put next chunk on the job queue.
                            #self.sent_chunks.append((params, time.time()))
                            break
                        except Qqueue.Full:
                            continue
                while not shutdown.is_set():
                    time.sleep(.1)

                result_monitor.terminate()
                result_monitor.join()
                if manager is not None:
                    manager.shutdown()
                time.sleep(1)
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
        def chunk_rainbow(self, rainbow, shutdown):
            try:
                if not self.single_user_mode:
                    JobQueueManager.register('get_job_q', callable=self.get_job_queue)
                    JobQueueManager.register('get_result_q', callable=self.get_result_queue)
                    JobQueueManager.register('get_shutdown', callable=self.get_shutdown)
                    JobQueueManager.register('get_mode_bit_1', callable=self.get_mode_bit_1)
                    JobQueueManager.register('get_mode_bit_2', callable=self.get_mode_bit_2)
                    manager = JobQueueManager(address=(self.IP, self.PORTNUM), authkey=self.AUTHKEY)
                    manager.start()
                    job_queue = manager.get_job_q()
                    result_queue = manager.get_result_q()
                    mode_bit_1 = manager.get_mode_bit_1()
                    mode_bit_2 = manager.get_mode_bit_2()
                    mode_bit_1.clear()
                    mode_bit_2.set()
                else: #if in single mode
                    manager = None
                    result_queue = self.result_queue
                    job_queue = self.job_queue
                    single = Process(target=self.start_single_user, args=(self.job_queue, self.result_queue,))
                    single.start()
                result_monitor = Process(target=self.check_results, args=(result_queue, shutdown))
                result_monitor.start()
                while not shutdown.is_set():
                    chunk = rainbow.getNextChunk()
                    #Retrieves word from chunk
                    #temp_word = self.extract_word(chunk)  # TODO: Broken, throws list index out of range exception
                    #Shares a 'current' word with UIs for display
                    #self.shared_dict["current word"] = temp_word
                    if self.single_user_mode: #if in single mode
                        while not shutdown.is_set():
                            try:
                                job_queue.put(chunk, timeout=.1)
                                break
                            except Qqueue.Full:
                                continue
                    else:
                        new_chunk = {'params': chunk.params,
                                     'data': chunk.data,
                                     'timestamp': time.time()}
                        while not shutdown.is_set():
                            try:
                                job_queue.put(new_chunk, timeout=.1)
                                #self.sent_chunks.append((chunk.params, time.time()))
                                break
                            except Qqueue.Full:
                                continue
                    if shutdown.is_set():
                        print "chunker trying to shut down"
                        while True:
                            try:
                                job_queue.get_nowait()
                            except Qqueue.Empty:
                                return
                            finally:
                                time.sleep(2)
                                if manager is not None:
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
        def chunk_rainbow_maker(self, rainmaker, shutdown):
            try:
                if not self.single_user_mode:
                    JobQueueManager.register('get_job_q', callable=self.get_job_queue)
                    JobQueueManager.register('get_result_q', callable=self.get_result_queue)
                    JobQueueManager.register('get_shutdown', callable=self.get_shutdown)
                    JobQueueManager.register('get_mode_bit_1', callable=self.get_mode_bit_1)
                    JobQueueManager.register('get_mode_bit_2', callable=self.get_mode_bit_2)
                    manager = JobQueueManager(address=(self.IP, self.PORTNUM), authkey=self.AUTHKEY)
                    manager.start()
                    job_queue = manager.get_job_q()
                    result_queue = manager.get_result_q()
                    mode_bit_1 = manager.get_mode_bit_1()
                    mode_bit_2 = manager.get_mode_bit_2()
                    mode_bit_1.clear()
                    mode_bit_2.clear()
                else:
                    manager = None
                    result_queue = self.result_queue
                    job_queue = self.job_queue
                    single = Process(target=self.start_single_user, args=(self.job_queue, self.result_queue,))
                    single.start()

                result_monitor = Process(target=self.check_results, args=(result_queue, shutdown))
                result_monitor.start()

                while not shutdown.is_set():
                    params_chunk = rainmaker.makeParamsChunk()
                    new_chunk = {"params": params_chunk.params,
                                 "data": params_chunk.data}
                    try:
                        job_queue.put(new_chunk, timeout=.1)
                    except Qqueue.Full:
                        continue
                    if shutdown.is_set():
                        while True:
                            try:
                                job_queue.get_nowait()
                            except Qqueue.Empty:
                                return
                            finally:
                                if manager is not None:
                                    time.sleep(1)
                                    manager.shutdown()
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

        def start_single_user(self, job_queue, result_queue):
            print "Single User Mode"
            try:  # start_single_user definition try block

                chunk_runner = []
                if self.cracking_mode == "dic":
                    print "Starting dictionary cracking."
                    dictionary = Dictionary.Dictionary()
                    for i in range(0, 3):
                        chunk_runner.append(Process(target=self.run_dictionary,
                                                    args=(dictionary, job_queue, result_queue)))

                elif self.cracking_mode == "bf":
                    print "Starting brute force cracking."
                    bf = Brute_Force.Brute_Force()
                    chunk_runner.append(Process(target=self.run_brute_force, args=(bf, job_queue, result_queue)))

                elif self.cracking_mode == "rain":
                    print "Starting rainbow table cracking."
                    rainbow = RainbowUser.RainbowUser()
                    chunk_runner.append(Process(target=self.run_rain_user, args=(rainbow, job_queue, result_queue)))

                elif self.cracking_mode == "rainmaker":
                    print "Starting rainbow table generator."
                    rainmaker = RainbowMaker.RainbowMaker()
                    chunk_runner.append(Process(target=self.run_rain_maker, args=(rainmaker, job_queue, result_queue)))

                else:
                    return "wtf?"

                for process in chunk_runner:
                    process.start()
                for process in chunk_runner:
                    process.join()

                if self.shutdown.is_set():
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

        def run_dictionary(self, dictionary, job_queue, result_queue):
            try:
                while not self.shutdown.is_set():
                    try:
                        chunk = job_queue.get(block=True, timeout=.25)  # block for at most .25 seconds, then loop again
                        print "got a chunk"
                    except Qqueue.Empty:
                        continue
                    dictionary.find(chunk)
                    result = dictionary.isFound()
                    params = chunk.params.split()
                    if result:
                        key = dictionary.showKey()
                        result_queue.put(("w", key))
                    elif params[10] == "True":
                        result_queue.put(("e", chunk.params))
                    else:
                        result_queue.put(("f", chunk.params))

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

        def run_brute_force(self, bf, job_queue, result_queue):
            bf.result_queue = result_queue
            while not self.shutdown.is_set():
                try:
                    chunk = job_queue.get(timeout=.1)
                except Qqueue.Empty:
                    continue

                bf.run_chunk(chunk)
                bf.start_processes()

            bf.terminate_processes()

        def run_rain_user(self, rain, job_queue, result_queue):
            while not self.shutdown.is_set():
                try:
                    chunk = job_queue.get(block=True, timeout=.25)
                except Qqueue.Empty:
                    continue

                rain.find(chunk)
                if rain.isFound():
                    result_queue.put(("w", rain.getKey()))
                elif chunk.params.split()[10] == "True":
                    result_queue.put(("e", chunk.params))
                else:
                    result_queue.put(("f", chunk.params))

        def run_rain_maker(self, maker, job_queue, result_queue):
            while not self.shutdown.is_set():
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

        #Retrieves word from chunk
        def extract_word(self, chunk):

            #If the chunk isn't empty
            if not chunk.params == "":

                #Take the parameters and split them into a list
                params_list = chunk.params.split()

                #Get the attack method from the parameters
                attack_method = params_list[0]

                #Take the data and split it into a list
                chunk_list = chunk.data.split()

                if attack_method == "dictionary":

                    #Return the 1th item from the data
                    return chunk_list[1]

                elif attack_method == "bruteforce":

                    #TODO: Fix bruteforce chunk parsing
                    #BROKEN
                    #return chunk_list[1]
                    x = "Fix Me"
                    return x

                elif attack_method == "rainbowuser":

                    #Return the 0th item from the data
                    return chunk_list[0]

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
    current_process().authkey = "Popcorn is awesome!!!"
    pass
