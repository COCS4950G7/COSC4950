# NetworkClient_r15

# 2/25/2015

# Adapted r14B into a class based server so we can instantiate it from other classes. Moved user input to get_ip().
# Timer now runs inside run_client() function.

from multiprocessing.managers import SyncManager
from multiprocessing import Process
import Queue
import Chunk
import time
import string
import platform
import Dictionary
import Brute_Force
import RainbowUser
import RainbowMaker


class Client():
    IP = "127.0.0.1" #default is pingback
    PORTNUM = 22536
    AUTHKEY = "Popcorn is awesome!!!"
    cracking_mode = 'dic'

    def __init__(self):
        self.get_ip()
        self.run_client()

    #===================================================================================================================
    #FUNCTIONS
    #===================================================================================================================


    #--------------------------------------------------------------------------------------------------
    #runclient function
    #--------------------------------------------------------------------------------------------------
    def run_client(self): #Client Primary loop
        start_time = time.time()
        print "start"
        try: #runclient definition try block
            manager = self.make_client_manager(self.IP, self.PORTNUM, self.AUTHKEY)
            job_queue = manager.get_job_q()
            result_queue = manager.get_result_q()
            shutdown = manager.get_shutdown()

            if self.cracking_mode == "dic":
                dictionary = Dictionary.Dictionary()

                chunk_runner = Process(target=self.run_dictionary, args=(dictionary, job_queue, result_queue, shutdown))
            else:
                if self.cracking_mode == "bf":
                    bf = Brute_Force.Brute_Force()

                    chunk_runner = Process(target=self.run_brute_force, args=(bf, job_queue, result_queue, shutdown))
                else:
                    if self.cracking_mode == "rain":
                        return  # haven't figured out how to set this up yet
                    else:
                        if self.cracking_mode == "rainmaker":
                            return  # haven't figured out how to set this up yet
                        else:
                            return "wtf?"

            chunk_runner.start()

            if shutdown.is_set():
                print "received shutdown notice from server."
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
            end_time= time.time() - start_time
            print "Client ran for: "+str(end_time)+" seconds"
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


    def get_ip(self):
            user_input = raw_input("Enter the Server's IP Address:")  #NOTE: needs to be made more tolerant of input errors
            self.IP = user_input

    def run_dictionary(self, dictionary, job_queue, result_queue, shutdown):

        while not shutdown.is_set():
            job = job_queue.get()
            chunk = Chunk.Chunk()
            chunk.params = job.value['params']
            chunk.data = job.value['data']
            print chunk.params
            dictionary.find(chunk)
            result = dictionary.isFound()
            if result:
                print "Hooray!"
                print "key is: " + dictionary.showKey()
                key = dictionary.showKey()
                result_queue.put(("w", key))
                time.sleep(1)
               # result_queue.put(("c", key))

            else:
                result_queue.put(("f", chunk.params))
                    #result_q.put(("c", chunk.params)) #unction has never been tested


    def run_brute_force(self, bf, job_queue, result_queue, shutdown):

        while not shutdown.is_set():
            job = job_queue.get()
            chunk = Chunk.Chunk()
            chunk.params = job.value['params']
            chunk.data = job.value['data']
            print chunk.params
            bf.result_queue = result_queue
            bf.start_processes()
            bf.run_chunk(chunk)


        return


    def run_rain_user(self, rain, job_queue, result_queue, shutdown):

        return


    def run_rain_maker(self, maker, job_queue, result_queue, shutdown):

        return

    #=====================================================================================================================
    #END OF FUNCTIONS
    #=====================================================================================================================

    #=====================================================================================================================
    #Auxillery CLASSES
    #=====================================================================================================================
    class ServerQueueManager(SyncManager):
        pass
    #=====================================================================================================================
    #End of Auxillery Classes
    #=====================================================================================================================

if __name__ == '__main__': #Equivalent to Main
    client = Client()
    client