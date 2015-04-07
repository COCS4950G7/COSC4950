# this is a shortcut method to run client without any UI. For debugging purposes only.

from multiprocessing import Process, Event, Manager, current_process
from NetworkClient_r15b import Client
import os
import signal

class start():

    client = None

    def __init__(self):

        #self.start_client()
        return

    def start_client(self):
        #use a generic manager's shared dictionary to handle strings and ints
        #Define the shared dictionary and it's values
        manager = Manager()
        dictionary = manager.dict()
        dictionary["key"] = ''
        dictionary["finished chunks"] = 0
        dictionary["total chunks"] = 0
        dictionary["server ip"] = "127.1.1.1"

        #server/client/GUI signals shutdown when they're all done
        shutdown = Event()
        shutdown.clear()

        #Define the various events
        #server signals update when something has occurred (ie: chunk processed)
        update = Event()
        update.clear()

        #client signals if it's connected or not
        is_connected = Event()
        is_connected.clear()

        #client signals if it's doing stuff or not
        is_doing_stuff = Event()
        is_doing_stuff.clear()

        #Shared is a list of shared events
        shared = []
        shared.append(dictionary)
        shared.append(shutdown)
        shared.append(update)
        shared.append(is_connected)
        shared.append(is_doing_stuff)

        self.client = (Process(target=Client, args=("192.168.2.136", shared)))
        #self.client = (Process(target=Client, args=("10.121.12.111", shared)))
        self.client.start()
        self.client.join()
        self.client.terminate()

if __name__ == '__main__':
    start = start()
    start.start_client()