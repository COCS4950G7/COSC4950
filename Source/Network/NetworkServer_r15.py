# NetworkServer_r15

# 2/25/2015

# Adapted r14B into a class based server so we can instantiate it from other classes. Moved IP detection to get_ip()
# method. Timer now runs inside run_server() function.



#=====================================================================================================================
#IMPORTS
#=====================================================================================================================
from multiprocessing.managers import SyncManager
from multiprocessing import Process, Value, Event
import platform
import Queue
import time
import socket
import string
import Dictionary
import Brute_Force
import RainbowMaker
import RainbowUser
#=====================================================================================================================
#END OF IMPORTS
#=====================================================================================================================


class Server():
    IP = "127.0.0.1" #defaults to the pingback
    PORTNUM = 22536
    AUTHKEY = "Popcorn is awesome!!!"

    cracking_mode = "dic"  # possible values are dic, bf, rain, rainmaker
    sent_chunks = []  # list of chunks added to queue, added with timestamp to keep track of missing pieces
    found_solution = Value('b', False)  # synchronized found solution variable
    variables = []
    def __init__(self):
        self.get_ip()
    #=====================================================================================================================
    #FUNCTIONS
    #=====================================================================================================================
    #--------------------------------------------------------------------------------------------------
    #runserver function
    #--------------------------------------------------------------------------------------------------

    def run_server(self):  #the primary server loop
        start_time= time.time()

        try: #runserver definition try block
            # Start a shared manager server and access its queues
            manager = self.make_server_manager(self.PORTNUM, self.IP, self.AUTHKEY) #Make a new manager
            shared_job_q = manager.get_job_q()
            shared_result_q = manager.get_result_q() #Shared result queue
            shutdown = manager.get_shutdown()
            # Spawn processes to feed the queue and monitor the result queue
            if self.cracking_mode == "dic":
                dictionary = Dictionary.Dictionary()
                # this will be replaced by input from the user once controller is reworked
                dictionary.setAlgorithm('sha1')
                dictionary.setFileName("dic") #reset this value to dic if you dont have this file
                dictionary.setHash("33da7a40473c1637f1a2e142f4925194") # popcorn
                #dictionary.setHash("b17a9909e09fda53653332431a599941") #Karntnerstrasse-Rotenturmstrasse (LONGER HASH)
                self.found_solution.value = False
                chunk_maker = Process(target=self.chunk_dictionary, args=(dictionary, manager, shared_job_q))
            else:
                if self.cracking_mode == "bf":
                    bf = Brute_Force.Brute_Force()
                    # this will be replaced by input from the user once controller is reworked
                    bf.set_params(alphabet=string.ascii_lowercase + string.ascii_uppercase + string.digits,
                                  algorithm="md5",
                                  origHash="12c8de03d4562ba9f810e7e1e7c6fc15",  # aa9999
                                  min_key_length=6,
                                  max_key_length=16)
                    chunk_maker = Process(target=self.chunk_brute_force, args=(bf, manager, shared_job_q))
                else:
                    if self.cracking_mode == "rain":
                        return  # haven't figured out how to set this up yet
                    else:
                        if self.cracking_mode == "rainmaker":
                            return  # haven't figured out how to set this up yet
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
            manager.shutdown()

            return
        except Exception as inst:
            print "============================================================================================="
            print "ERROR: An exception was thrown in runserver definition Try block"
            #the exception instance
            print type(inst)
            #srguments stored in .args
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
        try: #Make_server_manager definition try block
            job_q = Queue.Queue(maxsize=100)
            result_q = Queue.Queue()
            shutdown = Event()
            shutdown.clear()

            try: #JobQueueManager/Lambda functions Try Block
                self.JobQueueManager.register('get_job_q', callable=lambda: job_q)
                self.JobQueueManager.register('get_result_q', callable=lambda: result_q)
                self.JobQueueManager.register('get_shutdown', callable=lambda: shutdown)
            except Exception as inst:
                print "============================================================================================="
                print "ERROR: An exception was thrown in Make_server_Manager: JobQueueManager/Lambda functions Try Block"
                #the exception instance
                print type(inst)
                #srguments stored in .args
                print inst.args
                #_str_ allows args tto be printed directly
                print inst
                print "============================================================================================="

            manager = self.JobQueueManager(address=(ip, port), authkey=authkey)
            manager.start()
            print 'Server started at port %s' % port
            return manager
        except Exception as inst:
            print "============================================================================================="
            print "ERROR: An exception was thrown in Make_server_manager definition Try block"
            #the exception instance
            print type(inst)
            #srguments stored in .args
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
        try:
            while not self.found_solution.value:
                result = results_queue.get() #get chunk from shared result queue
                if result[0] == "w": #check to see if solution was found
                    print "The solution was found!"
                    shutdown.set()
                    print "shutdown notice sent to clients"
                    key = result[1]
                    self.found_solution.value = True
                    print "Key is: %s" % key

                elif(result[0] == "c"):  #check to see if client has crashed
                    print "A client has crashed!" #THIS FUNCTION IS UNTESTED
                elif result[0] == "e":
                    print "Final chunk processed, no solution found."
                    shutdown.set()
                    break
                else: #solution has not been found
                    print "Chunk finished with params: %s" %result[1]
                    # go through the sent chunks list and remove the finished chunk
                    for chunk in self.sent_chunks:
                        if chunk[0] == result[1]:
                            self.sent_chunks.remove(chunk)
        except Exception as inst:
            print "============================================================================================="
            print "ERROR: An exception was thrown in check_results definition Try block"
            #the exception instance
            print type(inst)
            #srguments stored in .args
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
            while not dictionary.isEof() and not self.found_solution.value:  # Keep looping while it is not the end of the file
                #chunk is a Chunk object
                chunk = dictionary.getNextChunk() #get next chunk from dictionary

                new_chunk = manager.Value(dict, {'params': chunk.params,
                                                 'data': chunk.data,
                                                 'timestamp': time.time(),
                                                 'halt': False})
                job_queue.put(new_chunk)  # put next chunk on the job queue.
                                          # queue is blocking by default, so will just wait until it is no longer full before adding another.
                #add chunk params to list of sent chunks along with a timestamp so we can monitor which ones come back
                self.sent_chunks.append((chunk.params, time.time()))
                if dictionary.isEof():
                    break
            if self.found_solution.value:
                while True:
                    try:
                        job_queue.get_nowait()
                    except Queue.Empty:
                        return
        except Exception as inst:
            print "============================================================================================="
            print "ERROR: An exception was thrown in chunk_dictionary definition Try block"
            #the exception instance
            print type(inst)
            #srguments stored in .args
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

                new_chunk = manager.Value(dict, {'params': params,
                                                 'data': '',
                                                 'timestamp': time.time(),
                                                 'halt': False})
                job_queue.put(new_chunk)  # put next chunk on the job queue.
                                          # queue is blocking by default, so will just wait until it is no longer full before adding another.
                #add chunk params to list of sent chunks along with a timestamp so we can monitor which ones come back
                self.sent_chunks.append((params, time.time()))
                if self.found_solution.value:
                    while True:
                        try:
                            job_queue.get_nowait()
                        except Queue.Empty:
                            return
                        finally:
                            return

        except Exception as inst:
            print "============================================================================================="
            print "ERROR: An exception was thrown in chunk_brute_force definition Try block"
            #the exception instance
            print type(inst)
            #srguments stored in .args
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
    def chunk_rainbow(self, rainbow, job_queue):
        try:
            #INSERT CODE HERE
            return
        except Exception as inst:
            print "============================================================================================="
            print "ERROR: An exception was thrown in chunk_rainbow definition Try block"
            #the exception instance
            print type(inst)
            #srguments stored in .args
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
    def chunk_rainbow_maker(self, rainmaker, job_queue):
        try:
            #INSERT CODE HERE
            return
        except Exception as inst:
            print "============================================================================================="
            print "ERROR: An exception was thrown in chunk_rainbow_maker definition Try block"
            #the exception instance
            print type(inst)
            #srguments stored in .args
            print inst.args
            #_str_ allows args tto be printed directly
            print inst
            print "============================================================================================="
    #--------------------------------------------------------------------------------------------------
    #end of chunks for rainbow maker function
    #--------------------------------------------------------------------------------------------------


    def get_ip(self):
                #detect the OS
            try: #getOS try block
                print "*************************************"
                print "    Network Server"
                print "*************************************"
                print "OS DETECTION:"
                if(platform.system()=="Windows"): #Detecting Windows
                    print platform.system()
                    print platform.win32_ver()
                elif(platform.system()=="Linux"): #Detecting Linux
                    print platform.system()
                    print platform.dist()
                elif(platform.system()=="Darwin"): #Detecting OSX
                    print platform.system()
                    print platform.mac_ver()
                else:                           #Detecting an OS that is not listed
                    print platform.system()
                    print platform.version()
                    print platform.release()
                print "*************************************"
            except Exception as inst:
                print "========================================================================================"
                print "ERROR: An exception was thrown in getOS try block"
                print type(inst) #the exception instance
                print inst.args #srguments stored in .args
                print inst #_str_ allows args tto be printed directly
                print "========================================================================================"
            #end of detect the OS

            #get the IP address
            try: #getIP tryblock
                print "STATUS: Getting your network IP adddress"
                if(platform.system()=="Windows"):
                    self.IP= socket.gethostbyname(socket.gethostname())
                    print "My IP Address: " + str(self.IP)
                elif(platform.system()=="Linux"):
                    #Source: http://stackoverflow.com/questions/11735821/python-get-localhost-ip
                    #Claims that this works on linux and windows machines
                    import fcntl
                    import struct
                    import os

                    def get_interface_ip(ifname):
                        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                        return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s',ifname[:15]))[20:24])
                    #end of def
                    def get_lan_ip():
                        ip = socket.gethostbyname(socket.gethostname())
                        if ip.startswith("127.") and os.name != "nt":
                            interfaces = ["eth0","eth1","eth2","wlan0","wlan1","wifi0","ath0","ath1","ppp0"]
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
                elif(platform.system()=="Darwin"):
                    self.IP= socket.gethostbyname(socket.gethostname())
                    print "My IP Address: "+ str(self.IP)
                else:
                    #NOTE: MAY REMOVE THIS AND REPLACE WITH THE LINUX DETECTION METHOD
                    print "INFO: The system has detected that you are not running Windows, OS X, or Linux."
                    print "INFO: System is using a generic IP detection method"
                    self.IP= socket.gethostbyname(socket.gethostname())
                    print "My IP Address: " + str(self.IP)
            except Exception as inst:
                print "========================================================================================"
                print "ERROR: An exception was thrown in getIP try block"
                print type(inst) #the exception instance
                print inst.args #srguments stored in .args
                print inst #_str_ allows args tto be printed directly
                print "========================================================================================"
            #end of get the IP address

    #=====================================================================================================================
    #END OF FUNCTIONS
    #=====================================================================================================================

    #=====================================================================================================================
    #AUXILLERY CLASSES
    #=====================================================================================================================

     # This is based on the examples in the official docs of multiprocessing.
        # get_{job|result}_q return synchronized proxies for the actual Queue
        # objects.
    class JobQueueManager(SyncManager):  
        pass


    #=====================================================================================================================
    #END OF AUXILLERY CLASSES
    #=====================================================================================================================
if __name__ == '__main__': #Equivalent to Main
    server = Server()
    server.run_server()