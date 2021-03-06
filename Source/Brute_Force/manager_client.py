
from multiprocessing.managers import SyncManager
import Dictionary
import Queue
import Chunk
import time

IP = "10.121.0.158"
PORTNUM = 22536
AUTHKEY = "Popcorn is awesome!!!"


def runclient():
    try: #runclient definition try block
        manager = make_client_manager(IP, PORTNUM, AUTHKEY)
        job_q = manager.get_job_q()
        result_q = manager.get_result_q()
        dictionary = Dictionary.Dictionary()

        while True:
            try:
                job = job_q.get_nowait()
                chunk = Chunk.Chunk()
                chunk.params = job.value['params']
                chunk.data = job.value['data']
                print chunk.params
                time.sleep(.01)
                dictionary.find(chunk)
                result = dictionary.isFound()
                time.sleep(0.00)
                if result:
                    print "Hooray!"
                    print "key is: " + dictionary.showKey()
                    key = dictionary.showKey()
                    result_q.put(("win", key))
                    return
                else:
                    result_q.put(("fail", chunk.params))
            except Queue.Empty:
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

class ServerQueueManager(SyncManager):
    pass

def make_client_manager(ip, port, authkey):
    """ Create a manager for a client. This manager connects to a server on the
        given address and exposes the get_job_q and get_result_q methods for
        accessing the shared queues from the server.
        Return a manager object.
    """



    ServerQueueManager.register('get_job_q')
    ServerQueueManager.register('get_result_q')

    manager = ServerQueueManager(address=(ip, port), authkey=authkey)
    manager.connect()

    print 'Client connected to %s:%s' % (ip, port)
    return manager


if __name__ == '__main__':
    try: #Main
        import time
        start_time= time.time()
        runclient()
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
        print "Client ran for: "+str(end_time)+" seconds"
