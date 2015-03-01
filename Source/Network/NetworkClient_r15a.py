# NetworkClient_r15a.py

# 3/1/2015

# Now runs three instances of Dictionary concurrently, the result is consistent near 100% processor usage over
# long term runs (>20 chunks). Previously, usage was 40-60%. Also, removed function to request server ip from user as
# this is no longer used.


from multiprocessing.managers import SyncManager
from multiprocessing import Process
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

    #TODO: add shared variable for setting cracking mode
    def __init__(self, ip):
        #self.get_ip()
        self.IP = ip
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
        try:  # runclient definition try block
            manager = self.make_client_manager(self.IP, self.PORTNUM, self.AUTHKEY)
            job_queue = manager.get_job_q()
            result_queue = manager.get_result_q()
            shutdown = manager.get_shutdown()
            chunk_runner = []
            if self.cracking_mode == "dic":
                print "Starting dictionary cracking."
                dictionary = Dictionary.Dictionary()
                chunk_runner.append(Process(target=self.run_dictionary, args=(dictionary, job_queue, result_queue, shutdown)))
                chunk_runner.append(Process(target=self.run_dictionary, args=(dictionary, job_queue, result_queue, shutdown)))
                chunk_runner.append(Process(target=self.run_dictionary, args=(dictionary, job_queue, result_queue, shutdown)))
            else:
                if self.cracking_mode == "bf":
                    print "Starting brute force cracking."
                    bf = Brute_Force.Brute_Force()

                    chunk_runner.append(Process(target=self.run_brute_force, args=(bf, job_queue, result_queue, shutdown)))
                else:
                    if self.cracking_mode == "rain":
                        print "Starting rainbow table cracking."
                        return  # haven't figured out how to set this up yet
                    else:
                        if self.cracking_mode == "rainmaker":
                            print "Starting rainbow table generator."
                            return  # haven't figured out how to set this up yet
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
            return
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
            #output the timer, stating how long client ran for
            self.end_time= time.time() - self.start_time
            print "Client ran for: "+str(self.end_time)+" seconds"
    #--------------------------------------------------------------------------------------------------
    #End of runclient function
    #--------------------------------------------------------------------------------------------------

    #--------------------------------------------------------------------------------------------------
    #make_client_manager function
    #--------------------------------------------------------------------------------------------------
    def make_client_manager(self, ip, port, authkey):
        """ Create a manager for a client. This manager connects to a server on the
            given address and exposes the get_job_q and get_result_q methods for
            accessing the shared queues from the server.
            Return a manager object.
        """
        try:

            self.ServerQueueManager.register('get_job_q')
            self.ServerQueueManager.register('get_result_q')
            self.ServerQueueManager.register('get_shutdown')

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
                chunk.params = job.value['params']
                chunk.data = job.value['data']
                print chunk.params
                dictionary.find(chunk)
                result = dictionary.isFound()
                params = chunk.params.split()
                if result:
                    print "Hooray!"
                    print "key is: " + dictionary.showKey()
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
            #srguments stored in .args
            print inst.args
            #_str_ allows args tto be printed directly
            print inst
            print "============================================================================================="

    def run_brute_force(self, bf, job_queue, result_queue, shutdown):
        try:
            bf.result_queue = result_queue
            while not shutdown.is_set():
                job = job_queue.get()
                chunk = Chunk.Chunk()
                chunk.params = job.value['params']
                chunk.data = job.value['data']
                print chunk.params
                bf.start_processes()
                bf.run_chunk(chunk)

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
        #NEEDS ERROR HANDLING!!!!!!!!!!
        return

    def run_rain_maker(self, maker, job_queue, result_queue, shutdown):
        #NEEDS ERROR HANDLING!!!!!!!!!!!!!!!!!!
        return
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