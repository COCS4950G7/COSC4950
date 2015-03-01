# this is a shortcut method to run client without any UI. For debugging purposes only.

from multiprocessing import Process
from NetworkClient_r15a import Client



class start():

    client = Process()


    def __init__(self):
        #self.start_client()
        return


    def start_client(self):
        self.client = (Process(target=Client, args=("192.168.2.136",)))
        self.client.start()
        self.client.join()
        self.client.terminate()


if __name__ == '__main__':
    start = start()
    start.start_client()