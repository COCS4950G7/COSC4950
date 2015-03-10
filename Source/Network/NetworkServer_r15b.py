# NetworkServer_r15a

# 2/28/2015

# Now requires a dictionary parameter which contains all necessary settings.

# 3/2/2015

# Added support for single node mode, without the need for any networking.

# Settings dictionary extended to include a new, required, entry 'single' with possible values: 'True' and 'False'
# to indicate whether the server is operating in single computer mode. For now, default value is networked mode.

# Added automatic setting of client cracking mode.

#=====================================================================================================================
#IMPORTS
#=====================================================================================================================
from multiprocessing.managers import SyncManager
from multiprocessing import Process, Value, Event, Queue
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
#=====================================================================================================================
#END OF IMPORTS
#=====================================================================================================================


class Server():
    try:
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

        def __init__(self, settings, shared_variables):
            self.settings = settings
            self.get_ip()
            self.cracking_mode = settings["cracking method"]

            self.shared_dict = shared_variables[0]
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
            if "single" in settings:
                if settings["single"] == "True":
                    self.single_user_mode = True
                else:
                    self.single_user_mode = False
            if self.cracking_mode == "rainmaker":
                self.rainmaker = RainbowMaker.RainbowMaker()
            self.run_server()
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
                    shutdown = Event()
                    shutdown.clear()
                    shared_job_q = Queue(100)
                    shared_result_q = Queue()
                    single = Process(target=self.start_single_user, args=(shared_job_q, shared_result_q, shutdown))
                    single.start()
                    manager = None

                else:
                    print "Network Server Mode"
                    # Start a shared manager server and access its queues
                    manager = self.make_server_manager(self.PORTNUM, self.IP, self.AUTHKEY)  # Make a new manager
                    shared_job_q = manager.get_job_q()
                    shared_result_q = manager.get_result_q()  # Shared result queue
                    shutdown = manager.get_shutdown()
                    mode_bit_1 = manager.get_mode_bit_1()
                    mode_bit_2 = manager.get_mode_bit_2()

                # Spawn processes to feed the job queue and monitor the result queue
                if self.cracking_mode == "dic":
                    if not self.single_user_mode:
                        mode_bit_1.set()
                        mode_bit_2.set()
                    dictionary = Dictionary.Dictionary()
                    dictionary.setAlgorithm(self.settings["algorithm"])
                    dictionary.setFileName(self.settings["file name"])
                    dictionary.setHash(self.settings["hash"])
                    self.found_solution.value = False
                    chunk_maker = Process(target=self.chunk_dictionary, args=(dictionary, manager, shared_job_q))
                elif self.cracking_mode == "bf":
                    if not self.single_user_mode:
                        mode_bit_1.set()
                        mode_bit_2.clear()
                    bf = Brute_Force.Brute_Force()
                    bf.set_params(alphabet=self.settings["alphabet"],
                                  algorithm=self.settings["algorithm"],
                                  origHash=self.settings["hash"],
                                  min_key_length=self.settings["min key length"],
                                  max_key_length=self.settings["max key length"])
                    self.total_chunks = bf.get_total_chunks()
                    chunk_maker = Process(target=self.chunk_brute_force, args=(bf, manager, shared_job_q))
                elif self.cracking_mode == "rain":
                    if not self.single_user_mode:
                        mode_bit_1.clear()
                        mode_bit_2.set()

                    rain = RainbowUser.RainbowUser()
                    rain.setFileName(self.settings["file name"])
                    rain.setHash(self.settings["hash"])
                    rain.gatherInfo()

                    chunk_maker = Process(target=self.chunk_rainbow, args=(rain, manager, shared_job_q, shutdown))

                elif self.cracking_mode == "rainmaker":
                    if not self.single_user_mode:
                        mode_bit_1.clear()
                        mode_bit_2.clear()
                    rainmaker = self.rainmaker

                    rainmaker.setAlgorithm(self.settings['algorithm'])
                    rainmaker.setNumChars(self.settings['key length'])
                    rainmaker.setAlphabet(self.settings['alphabet'])
                    rainmaker.setDimensions(self.settings['chain length'], self.settings['num rows'])
                    rainmaker.setFileName(self.settings['file name'])
                    rainmaker.setupFile()

                    chunk_maker = Process(target=self.chunk_rainbow_maker, args=(rainmaker, shared_job_q, shutdown))

                else:
                    return "wtf?"

                chunk_maker.start()

                result_monitor = Process(target=self.check_results, args=(shared_result_q, shutdown))
                result_monitor.start()
                # block while there is no result, then terminate chunking and checking
                result_monitor.join()
                result_monitor.terminate()
                chunk_maker.join()
                chunk_maker.terminate()
                # Sleep a bit before shutting down the server - to give clients time to
                # realize the job queue is empty and exit in an orderly way.
                time.sleep(2)
                self.update.set()
                if not self.single_user_mode:
                    manager.shutdown()

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

        #--------------------------------------------------------------------------------------------------
        #make_server_manager function
        #--------------------------------------------------------------------------------------------------
        def make_server_manager(self, port, ip, authkey):
            """ Create a manager for the server, listening on the given port.
                Return a manager object with get_job_q and get_result_q methods.
            """
            try:  # Make_server_manager definition try block
                job_q = Queue(maxsize=100)
                result_q = Queue()
                shutdown = self.shutdown
                shutdown.clear()
                mode_bit_1 = Event()
                mode_bit_2 = Event()

                try:  # JobQueueManager/Lambda functions Try Block
                    self.JobQueueManager.register('get_job_q', callable=lambda: job_q)
                    self.JobQueueManager.register('get_result_q', callable=lambda: result_q)
                    self.JobQueueManager.register('get_shutdown', callable=lambda: shutdown)
                    self.JobQueueManager.register('get_mode_bit_1', callable=lambda: mode_bit_1)
                    self.JobQueueManager.register('get_mode_bit_2', callable=lambda: mode_bit_2)
                except Exception as inst:
                    print "============================================================================================"
                    print "ERROR: An exception was thrown in Make_server_Manager: " \
                          + "JobQueueManager/Lambda functions Try Block"
                    #the exception instance
                    print type(inst)
                    #arguments stored in .args
                    print inst.args
                    #_str_ allows args tto be printed directly
                    print inst
                    print "============================================================================================"

                manager = self.JobQueueManager(address=(ip, port), authkey=authkey)
                manager.start()
                print 'Server started at port %s' % port
                return manager
            except Exception as inst:
                print "============================================================================================="
                print "ERROR: An exception was thrown in Make_server_manager definition Try block"
                #the exception instance
                print type(inst)
                #arguments stored in .args
                print inst.args
                #_str_ allows args tto be printed directly
                print inst
                print "============================================================================================="
        #--------------------------------------------------------------------------------------------------
        #End of make_server_manager function
        #--------------------------------------------------------------------------------------------------

        #--------------------------------------------------------------------------------------------------
        # monitor results queue
        #--------------------------------------------------------------------------------------------------
        def check_results(self, results_queue, shutdown):
            completed_chunks = 0
            try:
                while not self.found_solution.value:
                    try:
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
                        for chunk in self.sent_chunks:
                            if chunk[0] == result[1]:
                                self.sent_chunks.remove(chunk)
                        if self.cracking_mode == "rainmaker":
                            rainChunk = result[1]
                            #rainChunk.params = result[1]
                            #rainChunk.data = result[2]
                            self.rainmaker.putChunkInFile(rainChunk)
                            if self.rainmaker.isDone():
                                print "Table complete and stored in file '%s'." % self.rainmaker.getFileName()
                                shutdown.set()


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
        def chunk_dictionary(self, dictionary, manager, job_queue):
            try:
                import time
                while not dictionary.isEof() and not self.found_solution.value:  # Keep looping while it is not eof
                    #chunk is a Chunk object
                    chunk = dictionary.getNextChunk()  # get next chunk from dictionary
                    if self.single_user_mode:
                        while not self.shutdown.is_set():
                            try:
                                job_queue.put(chunk)
                                break
                            except Qqueue.Full:
                                continue
                    else:
                        new_chunk = manager.Value(dict, {'params': chunk.params,
                                                         'data': chunk.data,
                                                         'timestamp': time.time(),
                                                         'halt': False})
                        while not self.shutdown.is_set():
                            try:
                                job_queue.put(new_chunk, timeout=.1)
                                #add params to list of sent chunks along with a timestamp so we can monitor which ones come back
                                self.sent_chunks.append((chunk.params, time.time()))
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
        def chunk_brute_force(self, bf, manager, job_queue):
            try:
                # Had strange difficulties with the internal chunking method, so extracted the funtional bits here
                for prefix in bf.get_prefix():
                    if prefix == '':
                        prefix = "-99999999999999999999999999999999999"
                    params = "bruteforce\n" + bf.algorithm + "\n" + bf.origHash + "\n" + bf.alphabet + "\n" \
                             + str(bf.minKeyLength) + "\n" + str(bf.maxKeyLength) + "\n" + prefix + "\n0\n0\n0"
                    #print params
                    if self.single_user_mode:
                        new_chunk = Chunk.Chunk()
                        new_chunk.params = params
                    else:

                        new_chunk = manager.Value(dict, {'params': params,
                                                         'data': '',
                                                         'timestamp': time.time(),
                                                         'halt': False})
                    job_queue.put(new_chunk)  # put next chunk on the job queue.

                    self.sent_chunks.append((params, time.time()))
                    if self.found_solution.value:
                        while True:
                            try:
                                job_queue.get_nowait()
                            except Qqueue.Empty:
                                return
                            finally:
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
        def chunk_rainbow(self, rainbow, manager, job_queue, shutdown):
            try:
                while not rainbow.isEof() and not shutdown.is_set():
                    chunk = rainbow.getNextChunk()
                    if self.single_user_mode:
                        job_queue.put(chunk)
                    else:
                        new_chunk = manager.Value(dict, {'params': chunk.params,
                                                         'data': chunk.data,
                                                         'timestamp': time.time()})
                        job_queue.put(new_chunk)
                        self.sent_chunks.append((chunk.params, time.time()))
                    if shutdown.is_set():
                        while True:
                            try:
                                job_queue.get_nowait()
                            except Qqueue.Empty:
                                return
                            finally:
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
        def chunk_rainbow_maker(self, rainmaker, job_queue, shutdown):
            try:
                while not shutdown.is_set():
                    params_chunk = rainmaker.makeParamsChunk()
                    new_chunk = {"params": params_chunk.params,
                                 "data": params_chunk.data}
                    job_queue.put(new_chunk)
                    if shutdown.is_set():
                        while True:
                            try:
                                job_queue.get_nowait()
                            except Qqueue.Empty:
                                return
                            finally:
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

        def start_single_user(self, job_queue, result_queue, shutdown):
            print "Single User Mode"
            try:  # start_single_user definition try block

                chunk_runner = []
                if self.cracking_mode == "dic":
                    print "Starting dictionary cracking."
                    dictionary = Dictionary.Dictionary()
                    for i in range(0, 3):
                        chunk_runner.append(Process(target=self.run_dictionary,
                                                    args=(dictionary, job_queue, result_queue, shutdown)))

                else:
                    if self.cracking_mode == "bf":
                        print "Starting brute force cracking."
                        bf = Brute_Force.Brute_Force()

                        chunk_runner.append(Process(target=self.run_brute_force,
                                                    args=(bf, job_queue, result_queue, shutdown)))
                    else:
                        if self.cracking_mode == "rain":
                            print "Starting rainbow table cracking."
                            rainbow = RainbowUser.RainbowUser()

                            chunk_runner.append(Process(target=self.run_rain_user,
                                                        args=(rainbow, job_queue, result_queue, shutdown)))
                        else:
                            if self.cracking_mode == "rainmaker":
                                print "Starting rainbow table generator."
                                rainmaker = RainbowMaker.RainbowMaker()

                                chunk_runner.append(Process(target=self.run_rain_maker,
                                                            args=(rainmaker, job_queue, result_queue, shutdown)))
                            else:
                                return "wtf?"
                for process in chunk_runner:
                    process.start()
                for process in chunk_runner:
                    process.join()
                if shutdown.is_set():
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

        def run_dictionary(self, dictionary, job_queue, result_queue, shutdown):
            try:
                while not shutdown.is_set():
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
                       # result_queue.put(("c", key))
                    elif params[10] == "True":
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

        def run_brute_force(self, bf, job_queue, result_queue, shutdown):
            try:
                bf.result_queue = result_queue

                while not shutdown.is_set():
                    try:
                        chunk = job_queue.get()
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

        def run_rain_user(self, rain, job_queue, result_queue, shutdown):
            while not shutdown.is_set():
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

        def run_rain_maker(self, maker, job_queue, result_queue, shutdown):
            while not shutdown.is_set():
                params_chunk = Chunk.Chunk()
                try:
                    job = job_queue.get(block=True, timeout=.25)
                except Qqueue.Empty:
                    continue
                params_chunk.params = job["params"]
                finished_chunk = maker.create(params_chunk)
                result_queue.put(('f', finished_chunk))

        #=======================================4=======================================================================
        #END OF FUNCTIONS
        #===============================================================================================================

        #===============================================================================================================
        #AUXILLERY CLASSES
        #===============================================================================================================

         # This is based on the examples in the official docs of multiprocessing.
            # get_{job|result}_q return synchronized proxies for the actual Queue
            # objects.
        class JobQueueManager(SyncManager):
            pass

        #===============================================================================================================
        #END OF AUXILIARY CLASSES
        #===============================================================================================================
    except Exception as inst:
        print "========================================================================================"
        print "ERROR: An exception was thrown in master try block"
        print type(inst)  # the exception instance
        print inst.args  # arguments stored in .args
        print inst  #_str_ allows args tto be printed directly
        print "========================================================================================"