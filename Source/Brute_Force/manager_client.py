from multiprocessing.managers import SyncManager
import Dictionary
import Queue
import Chunk
import time


IP = "192.168.2.136"
PORTNUM = 22536
AUTHKEY = "Popcorn is awesome!!!"


def runclient():
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
            if result:
                print "Hooray!"
                print "key is: " + dictionary.showKey()
                result_q.put(("win", dictionary.showKey()))
                return
            else:
                result_q.put(("fail", ))
        except Queue.Empty:
            return


def make_client_manager(ip, port, authkey):
    """ Create a manager for a client. This manager connects to a server on the
        given address and exposes the get_job_q and get_result_q methods for
        accessing the shared queues from the server.
        Return a manager object.
    """
    class ServerQueueManager(SyncManager):
        pass

    ServerQueueManager.register('get_job_q')
    ServerQueueManager.register('get_result_q')

    manager = ServerQueueManager(address=(ip, port), authkey=authkey)
    manager.connect()

    print 'Client connected to %s:%s' % (ip, port)
    return manager


if __name__ == '__main__':
    runclient()