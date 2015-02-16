from multiprocessing.managers import SyncManager

import time
import Queue

import Dictionary

IP = "10.121.0.158"
PORTNUM = 22536
AUTHKEY = "Popcorn is awesome!!!"

dictionary = Dictionary.Dictionary()

def runserver():
    # Start a shared manager server and access its queues
    manager = make_server_manager(PORTNUM, AUTHKEY)
    shared_job_q = manager.get_job_q()
    shared_result_q = manager.get_result_q()
    dictionary.setAlgorithm('md5')
    dictionary.setFileName("dic")
    dictionary.setHash("33da7a40473c1637f1a2e142f4925194") # popcorn

    while not dictionary.isEof():

        #chunk is a Chunk object
        chunk = dictionary.getNextChunk()
        newChunk = manager.Value(dict, {'params': chunk.params, 'data': chunk.data})
        shared_job_q.put(newChunk)

    while True:
        result = shared_result_q.get()
        if result[0] is "win":
            key = result[1]
            print "Key is: %s" % key
            break
        else:
            print "Chunk finished with params: %s" %result[1]

    # Sleep a bit before shutting down the server - to give clients time to
    # realize the job queue is empty and exit in an orderly way.
    time.sleep(2)
    manager.shutdown()
    return

 # This is based on the examples in the official docs of multiprocessing.
    # get_{job|result}_q return synchronized proxies for the actual Queue
    # objects.
class JobQueueManager(SyncManager):
    pass

def make_server_manager(port, authkey):
    """ Create a manager for the server, listening on the given port.
        Return a manager object with get_job_q and get_result_q methods.
    """
    job_q = Queue.Queue(maxsize=1000)
    result_q = Queue.Queue()


    try:
        JobQueueManager.register('get_job_q', callable=lambda: job_q)
        JobQueueManager.register('get_result_q', callable=lambda: result_q)
    except Exception as inst:
        print "============================================================================================="
        print "ERROR: An exception was thrown in Make_server_Manager: JobQueueManager"
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



if __name__ == '__main__':
    try:
        import  time
        start_time= time.time()
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
        end_time= time.time() - start_time
        print "Server ran for "+str(end_time)+" seconds"