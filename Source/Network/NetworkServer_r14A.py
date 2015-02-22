__author__ = 'chris hamm'
#NetworkServer_r14A
#Created: 2/21/2015

#Designed to run with NetworkClient_r14A

#Things that have changed in this revision (compared to the original rev14)
    #(Implemented) Added additional comments and section dividers
    #(Implemented) Reorganized code to fit section dividers better
    #(Implemented) Added OS detection at the beginning of server startup, also prints what OS you are using
    #(Implemented) Added in IP detection. It will automatically detect your ip for you, and set the IP variable to that IP address

#NOTES/PROBLEMS ENCOUNTERED:
    #THE MANAGERS DO NOT ALLOW INDEXING ONN THIER AUTOPROXY OBJECTS (MAKING SHARING SINGLE VALUE NOT POSSIBLE VIA THIS METHOD)
        #POSSIBLE OPTION: SHARED CTYPE OBJECTS (QUITE COMPLICATED)
        #POSSIBLE OPTION: "CONTAINER PROXY"
        #POSSIBLE OPTION: USE SOCKETS TO SEND MESSAGES TO EACH OF THE CLIENTS INSTEAD OF THE MANAGERS
    #QUEUE IS NOT PRACTICAL DATA TYPE TO USE TO SHARE VALUE BECAUSE YOU MUST CONSTANTLY PUT MORE VALUS IN, THEREFORE CAUSING LATENCY DEFEATING THE PURPOSE
    #MODIFICATIONS TO MUTABLE VALUES/ITEMS IN DICT AND LIST PROXIES WILL NOT BE PROPOGATED THROUGH THE MANAGER BECAUSE THE PROXY HAS NO WAY OF KNOWING WHEN THE VALUES HAVE CHANGED



#IMPORTS===============================================================================================================
from multiprocessing.managers import SyncManager
from multiprocessing import Process, Value
import platform
import time
import Queue
import socket
import Dictionary
#END OF IMPORTS=======================================================================================================

#FUNCTIONS============================================================================================================
#runserver function--------------------------------------------------------------------------------
def runserver():  #the primary server loop
    try: #runserver definition try block
        # Start a shared manager server and access its queues
        manager = make_server_manager(PORTNUM, AUTHKEY) #Make a new manager
        shared_job_q = manager.get_job_q()
        shared_result_q = manager.get_result_q() #Shared result queue
        dictionary.setAlgorithm('md5')
        dictionary.setFileName("dic")
        dictionary.setHash("33da7a40473c1637f1a2e142f4925194") # popcorn
        found_solution.value = False

        # Spawn processes to feed the queue and monitor the result queue
        chunk_maker = Process(target=chunk_dictionary, args=(dictionary, manager, shared_job_q))
        chunk_maker.start()
        result_monitor = Process(target=check_results, args=(shared_result_q,))
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
#End of runserver function------------------------------------------------------------------------------------
#make_server_manager function---------------------------------------------------------------------------------
def make_server_manager(port, authkey):
    """ Create a manager for the server, listening on the given port.
        Return a manager object with get_job_q and get_result_q methods.
    """
    try: #Make_server_manager definition try block
        job_q = Queue.Queue(maxsize=100)
        result_q = Queue.Queue()

        try: #JobQueueManager/Lambda functions Try Block
            JobQueueManager.register('get_job_q', callable=lambda: job_q)
            JobQueueManager.register('get_result_q', callable=lambda: result_q)
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

        manager = JobQueueManager(address=(IP, port), authkey=authkey)
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
#End of make_server_manager function-------------------------------------------------------------------------------

# monitor reesults queue
def check_results(results_queue):
    while not found_solution.value:
        result = results_queue.get() #get chunk from shared result queue
        if result[0] == "w": #check to see if solution was found
            print "The solution was found!"
            key = result[1]
            found_solution.value = True
            print "Key is: %s" % key

        elif(result[0] == "c"):  #check to see if client has crashed
            print "A client has crashed!" #THIS FUNCTION IS UNTESTED
        else: #solution has not been found
            print "Chunk finished with params: %s" %result[1]
            # go through the sent chunks list and remove the finished chunk
            for chunk in sent_chunks:
                if chunk[0] == result[1]:
                    sent_chunks.remove(chunk)

# feed dictionary chunks to job queue
def chunk_dictionary(dictionary, manager, job_queue):
    while not dictionary.isEof() and not found_solution.value:  # Keep looping while it is not the end of the file
        #chunk is a Chunk object
        chunk = dictionary.getNextChunk() #get next chunk from dictionary
        new_chunk = manager.Value(dict, {'params': chunk.params,
                                         'data': chunk.data,
                                         'timestamp': time.time(),
                                         'halt': False})
        job_queue.put(new_chunk)  # put next chunk on the job queue.
                                  # queue is blocking by default, so will just wait until it is no longer full before adding another.
        #add chunk params to list of sent chunks along with a timestamp so we can monitor which ones come back
        sent_chunks.append((chunk.params, time.time()))
    if found_solution.value:
        while True:
            try:
                job_queue.get_nowait()
            except Queue.Empty:
                return

# placeholder for brute force integration
def chunk_brute_force(bf, job_queue):
    return

# placeholder for rainbow table integration
def chunk_rainbow(rainbow, job_queue):
    return

#END OF FUNCTIONS======================================================================================================

#AUXILLERY CLASSES===============================================================================================================

 # This is based on the examples in the official docs of multiprocessing.
    # get_{job|result}_q return synchronized proxies for the actual Queue
    # objects.
class JobQueueManager(SyncManager):
    pass



#END OF AUXILLERY CLASSES========================================================================================================


IP = "127.0.0.1" #defaults to the pingback
PORTNUM = 22536
AUTHKEY = "Popcorn is awesome!!!"

dictionary = Dictionary.Dictionary()
sent_chunks = []  # list of chunks added to queue, added with timestamp to keep track of missing pieces
found_solution = Value('b', False)  # synchronized found solution variable


if __name__ == '__main__': #Equivalent to Main
    try: #Main
        #setup timer to record how long the server ran for
        import  time
        start_time= time.time()

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
                IP= socket.gethostbyname(socket.gethostname())
                print "My IP Address: " + str(IP)
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
                IP= get_lan_ip()
                print "My IP Address: " + str(IP)
            elif(platform.system()=="Darwin"):
                IP= socket.gethostbyname(socket.gethostname())
                print "My IP Address: "+ str(IP)
            else:
                #NOTE: MAY REMOVE THIS AND REPLACE WITH THE LINUX DETECTION METHOD
                print "INFO: The system has detected that you are not running Windows, OS X, or Linux."
                print "INFO: System is using a generic IP detection method"
                IP= socket.gethostbyname(socket.gethostname())
                print "My IP Address: " + str(IP)
        except Exception as inst:
            print "========================================================================================"
            print "ERROR: An exception was thrown in getIP try block"
            print type(inst) #the exception instance
            print inst.args #srguments stored in .args
            print inst #_str_ allows args tto be printed directly
            print "========================================================================================"
        #end of get the IP address

        #start the primary server loop
        runserver()
    except Exception as inst:
        print "============================================================================================="
        print "ERROR: An exception was thrown in Main"
        #the exception instance
        print type(inst)
        #srguments stored in .args
        print inst.args
        #_str_ allows args tto be printed directly
        print inst
        print "============================================================================================="
    finally:
        #output how long the server ran for
        end_time= time.time() - start_time
        print "Server ran for "+str(end_time)+" seconds"

