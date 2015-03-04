__author__ = 'chris hamm'
#NetworkClient_r14B
#Created: 2/24/2015

#Designed to run with NetworkServer_r14B

#Changes made in this revision:
    #moved where the start_timer begins to after the os and ip detection for better accuracy

#=====================================================================================================================
#IMPORTS
#=====================================================================================================================
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

#=====================================================================================================================
#END OF IMPORTS
#=====================================================================================================================

#=====================================================================================================================
#FUNCTIONS
#=====================================================================================================================
#--------------------------------------------------------------------------------------------------
#runclient function
#--------------------------------------------------------------------------------------------------
def runclient(): #Client Primary loop
    try: #runclient definition try block
        manager = make_client_manager(IP, PORTNUM, AUTHKEY)
        job_queue = manager.get_job_q()
        result_queue = manager.get_result_q()
        shutdown = manager.get_shutdown()

        if cracking_mode == "dic":
            dictionary = Dictionary.Dictionary()

            chunk_runner = Process(target=run_dictionary, args=(dictionary, job_queue, result_queue, shutdown))
        else:
            if cracking_mode == "bf":
                bf = Brute_Force.Brute_Force()

                chunk_runner = Process(target=run_brute_force, args=(bf, job_queue, result_queue, shutdown))
            else:
                if cracking_mode == "rain":
                    return  # haven't figured out how to set this up yet
                else:
                    if cracking_mode == "rainmaker":
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
#--------------------------------------------------------------------------------------------------
#End of runclient function
#--------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------
#make_client_manager function
#--------------------------------------------------------------------------------------------------
def make_client_manager(ip, port, authkey):
    """ Create a manager for a client. This manager connects to a server on the
        given address and exposes the get_job_q and get_result_q methods for
        accessing the shared queues from the server.
        Return a manager object.
    """
    try:


        ServerQueueManager.register('get_job_q')
        ServerQueueManager.register('get_result_q')
        ServerQueueManager.register('get_shutdown')

        manager = ServerQueueManager(address=(ip, port), authkey=authkey)
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
        #_str_ allows args to be printed directly
        print inst
        print "============================================================================================="
#--------------------------------------------------------------------------------------------------
#End of make_client_manager function
#--------------------------------------------------------------------------------------------------


def run_dictionary(dictionary, job_queue, result_queue, shutdown):

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


def run_brute_force(bf, job_queue, result_queue, shutdown):

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


def run_rain_user(rain, job_queue, result_queue, shutdown):

    return


def run_rain_maker(maker, job_queue, result_queue, shutdown):

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


IP = "127.0.0.1" #default is pingback
PORTNUM = 22536
AUTHKEY = "Popcorn is awesome!!!"
cracking_mode = 'bf'

#=====================================================================================================================
#START OF MAIN
#=====================================================================================================================
if __name__ == '__main__': #Equivalent to Main
    try: #Main
        #Create timer to keep track of how long the client ran for
       # import time
       # start_time= time.time()

        #--------------------------------------------------------------------------------------------------
        #detect the OS
        #--------------------------------------------------------------------------------------------------
        try: #getOS try block
            print "*************************************"
            print "    Network Client"
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
        #--------------------------------------------------------------------------------------------------
        #end of detect the OS
        #--------------------------------------------------------------------------------------------------

        #--------------------------------------------------------------------------------------------------
        #Get the servers IP address from the user
        #--------------------------------------------------------------------------------------------------
        try:
            #request for the server's IP address
            user_input = raw_input("Enter the Server's IP Address:")  #NOTE: needs to be made more tolerant of input errors
            IP = user_input
        except Exception as inst:
            print "========================================================================================"
            print "ERROR: An exception was thrown in get server IP address from user try block"
            print type(inst) #the exception instance
            print inst.args #srguments stored in .args
            print inst #_str_ allows args tto be printed directly
            print "========================================================================================"
        #--------------------------------------------------------------------------------------------------
        #End of get the server IP address from the user
        #--------------------------------------------------------------------------------------------------

        #--------------------------------------------------------------------------------------------------
        #Start the primary client while loop
        #--------------------------------------------------------------------------------------------------
        import time
        start_time = time.time() #start timer after the os and ip detection for better accuracy
        runclient()
        #--------------------------------------------------------------------------------------------------
        #End the primary client while loop
        #--------------------------------------------------------------------------------------------------
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
        #output the timer, stating how long client ran for
        end_time= time.time() - start_time
        print "Client ran for: "+str(end_time)+" seconds"


#=====================================================================================================================
#END OF MAIN
#=====================================================================================================================