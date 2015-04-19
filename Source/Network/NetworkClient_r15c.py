# NetworkClient_r15a.py

# 3/1/2015

# Now runs three instances of Dictionary concurrently, the result is consistent near 100% processor usage over
# long term runs (>20 chunks). Previously, usage was 40-60%. Also, removed function to request server ip from user as
# this is no longer used.

# 3/2/2015

# Added automatic setting of client cracking mode.


from multiprocessing.managers import SyncManager
from multiprocessing import Process, current_process
import Queue
import Chunk
import time
import Dictionary
import Brute_Force
import RainbowUser
import RainbowMaker

class Client():
    IP = "127.0.0.1" #default is pingback
    PORTNUM = 22536
    AUTHKEY = "Popcorn is awesome!!!"
    cracking_mode = 'dic'
    is_connected = None
    is_doing_stuff = None
    client_shutdown = None

    def __init__(self, ip, shared_variables):
        current_process().authkey = self.AUTHKEY
        current_process().authkey = "Popcorn is awesome!!!"
        #Allows ConsoleUI to use shared value and others to use parameter value
        if not ip == "127.0.1.1":

            self.IP = ip

        else:

            self.shared_dict = shared_variables[0]

            self.IP = self.shared_dict["server ip"]

        self.client_shutdown = shared_variables[1]
        self.is_connected = shared_variables[3]
        self.is_doing_stuff = shared_variables[4]

        self.run_client()
        self.start_time = 0
        self.end_time = 0

    #===================================================================================================================
    #FUNCTIONS
    #===================================================================================================================


    #--------------------------------------------------------------------------------------------------
    #runclient function
    #--------------------------------------------------------------------------------------------------
    def run_client(self):  # Client Primary loop
        #start_time = time.time()
        current_process().authkey = "Popcorn is awesome!!!"
        try:  # runclient definition try block
            manager = self.make_client_manager(self.IP, self.PORTNUM, self.AUTHKEY)
            self.is_connected.set()
            job_queue = manager.get_job_q()
            result_queue = manager.get_result_q()
            shutdown = manager.get_shutdown()
            self.set_cracking_mode(manager)
            chunk_runner = []
            self.is_doing_stuff.set()
            if self.cracking_mode == "dic":
                print "Starting dictionary cracking."
                dictionary = Dictionary.Dictionary()
                chunk_runner.append(Process(target=self.run_dictionary, args=(dictionary, job_queue, result_queue, shutdown)))
                chunk_runner.append(Process(target=self.run_dictionary, args=(dictionary, job_queue, result_queue, shutdown)))
                chunk_runner.append(Process(target=self.run_dictionary, args=(dictionary, job_queue, result_queue, shutdown)))

            elif self.cracking_mode == "bf":
                print "Starting brute force cracking."
                bf = Brute_Force.Brute_Force()
                chunk_runner.append(Process(target=self.run_brute_force, args=(bf, job_queue, result_queue, shutdown)))

            elif self.cracking_mode == "rain":
                rainbow = RainbowUser.RainbowUser()
                print "Starting rainbow table cracking."
                chunk_runner.append(Process(target=self.run_rain_user(rainbow, job_queue, result_queue, shutdown)))

            elif self.cracking_mode == "rainmaker":
                rainmaker = RainbowMaker.RainbowMaker()
                print "Starting rainbow table generator."
                chunk_runner.append(Process(target=self.run_rain_maker(rainmaker, job_queue, result_queue, shutdown)))

            else:
                return "wtf?"

            for process in chunk_runner:
                process.start()
            for process in chunk_runner:
                process.join()

            if shutdown.is_set():
                print "received shutdown notice from server."
                self.client_shutdown.set()
                self.is_connected.clear()
                self.is_doing_stuff.clear()

            for process in chunk_runner:
                process.terminate()


        except Exception as inst:
            print "============================================================================================="
            print "ERROR: An exception was thrown in runclient definition try block"
            #the exception instance
            print type(inst)
            #srguments stored in .args
            print inst.args
            #_str_ allows args tto be printed directly
            print inst
            print "============================================================================================="
            #result_queue.put(("c", chunk.params)) #tell server that client crashed, NEVER BEEN TESted
            print "Sent crash message to server"
        finally:
            self.client_shutdown.set()
            self.is_connected.clear()
            self.is_doing_stuff.clear()
            #output the timer, stating how long client ran for
            self.end_time= time.time() - self.start_time
            print "Client ran for: "+str(self.end_time)+" seconds"
    #--------------------------------------------------------------------------------------------------
    #End of runclient function
    #--------------------------------------------------------------------------------------------------

    def set_cracking_mode(self, manager):
        bit_1 = manager.get_mode_bit_1()
        bit_2 = manager.get_mode_bit_2()

        if bit_1.is_set() and bit_2.is_set():
            self.cracking_mode = 'dic'
        elif bit_1.is_set() and not bit_2.is_set():
            self.cracking_mode = 'bf'
        elif not bit_1.is_set() and bit_2.is_set():
            self.cracking_mode = 'rain'
        elif not bit_1.is_set() and not bit_2.is_set():
            self.cracking_mode = 'rainmaker'

    #--------------------------------------------------------------------------------------------------
    #make_client_manager function
    #--------------------------------------------------------------------------------------------------
    def make_client_manager(self, ip, port, authkey):
        try:

            self.ServerQueueManager.register('get_job_q')
            self.ServerQueueManager.register('get_result_q')
            self.ServerQueueManager.register('get_shutdown')
            self.ServerQueueManager.register('get_mode_bit_1')
            self.ServerQueueManager.register('get_mode_bit_2')
            print [ip]
            manager = self.ServerQueueManager(address=(ip, port), authkey=authkey)
            manager.connect()
            import time
            self.start_time = time.time()

            print 'Client connected to %s:%s' % (ip, port)
            return manager
        except Exception as inst:
            print "============================================================================================="
            print "ERROR: An exception was thrown in make_client_manager definition try block"
            #the exception instance
            print type(inst)
            #srguments stored in .args
            print inst.args
            #_str_ allows args tto be printed directly
            print inst
            print "============================================================================================="
    #--------------------------------------------------------------------------------------------------
    #End of make_client_manager function
    #--------------------------------------------------------------------------------------------------

    def run_dictionary(self, dictionary, job_queue, result_queue, shutdown):
        try:
            while not shutdown.is_set():
                try:
                    job = job_queue.get(block=True, timeout=.25)  # block for at most .25 seconds, then loop again
                except Queue.Empty:
                    continue
                chunk = Chunk.Chunk()
                chunk.params = job['params']
                chunk.data = job['data']
                dictionary.find(chunk)
                result = dictionary.isFound()
                params = chunk.params.split()
                if result:
                    if dictionary.doneList is not []:
                        result_queue.put(("w", dictionary.doneList))
                        dictionary.doneList = []
                        dictionary.result = False
                    else:
                        print "Hooray!"
                        print "key is: " + dictionary.showKey()
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
            #srguments stored in .args
            print inst.args
            #_str_ allows args tto be printed directly
            print inst
            print "============================================================================================="

    def run_brute_force(self, bf, job_queue, result_queue, shutdown):
        try:
            current_process().authkey = "Popcorn is awesome!!!"
            bf.result_queue = result_queue
            while not shutdown.is_set():
                try:
                    job = job_queue.get(block=True, timeout=.25)
                except Queue.Empty:
                    continue
                chunk = Chunk.Chunk()
                chunk.params = job['params']
                chunk.data = job['data']
                #print chunk.params
                bf.run_chunk(chunk)
                bf.start_processes()

        except Exception as inst:
            print "============================================================================================="
            print "ERROR: An exception was thrown in run_brute_force definition try block"
            #the exception instance
            print type(inst)
            #srguments stored in .args
            print inst.args
            #_str_ allows args tto be printed directly
            print inst
            print "============================================================================================="
        finally:
            bf.terminate_processes()

    def run_rain_user(self, rain, job_queue, result_queue, shutdown):
        try:
            while not shutdown.is_set():
                try:
                    job = job_queue.get(block=True, timeout=.25)
                except Queue.Empty:
                    continue
                chunk = Chunk.Chunk()
                chunk.params = job["params"]
                chunk.data = job["data"]
                rain.find(chunk)
                if rain.isFound():
                    result_queue.put(("w", rain.getKey()))
                elif chunk.params.split()[10] == "True":
                    result_queue.put(("e", chunk.params))
                else:
                    result_queue.put(("f", chunk.params))
        except Exception as inst:
            print "============================================================================================="
            print "ERROR: An exception was thrown in run_rain_user definition try block"
            #the exception instance
            print type(inst)
            #srguments stored in .args
            print inst.args
            #_str_ allows args tto be printed directly
            print inst
            print "============================================================================================="

    def run_rain_maker(self, maker, job_queue, result_queue, shutdown):
        try:
            while not shutdown.is_set():
                try:
                    job = job_queue.get(block=True, timeout=.25)
                except Queue.Empty:
                    continue
                params_chunk = Chunk.Chunk()
                params_chunk.params = job["params"]
                chunk_of_rainbow = maker.create(params_chunk)

                result_queue.put(('f', chunk_of_rainbow), timeout=.2)
                time.sleep(.05)
        except Exception as inst:
            print "============================================================================================="
            print "ERROR: An exception was thrown in run_rain_maker definition try block"
            #the exception instance
            print type(inst)
            #srguments stored in .args
            print inst.args
            #_str_ allows args tto be printed directly
            print inst
            print "============================================================================================="
    #===================================================================================================================
    #END OF FUNCTIONS
    #===================================================================================================================

    #===================================================================================================================
    #Auxillery CLASSES
    #===================================================================================================================
    class ServerQueueManager(SyncManager):
        pass
    #===================================================================================================================
    #End of Auxillery Classes
    #===================================================================================================================