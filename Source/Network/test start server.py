# This is a shortcut method to start server without any UI. For debugging purposes only.

from multiprocessing import Process, Event, Manager
from NetworkServer_r15b import Server
import string
import os

class start():

    client = Process()
    server = Process()
    settings = []

    settings.append({"cracking method": "dic",  # settings[0]
                "algorithm": "md5",
                "hash": "b17a9909e09fda53653332431a599941",  # Karntnerstrasse-Rotenturmstrasse in md5
                #"hash": "e7c0efb2dc699ede79983b8dfb5cb509ebf2bde9",  # Karntnerstrasse-Rotenturmstrasse in sha1
                #"hash": "7ab5f3733019c9e594526c9beb70c0cc51517b91a6557f4b4306564b753232af",  # Karntnerstrasse-Rotenturmstrasse in sha256
                "file name": "realuniq.txt",                    # last word in dic.txt
                "single": "True"})                    # (long runtime on realuniq dictionary ~755M lines)

    settings.append({"cracking method": "dic",  # settings[1]
                 "algorithm": "md5",
                 "hash": "33da7a40473c1637f1a2e142f4925194",  # popcorn (md5)
                 #"hash": "c3dc5a6ab47d683eb4e8d5c74c6147afa3f86f700301c3eb858689189761f91e4cfd2c6c5ccb1c03ec023b8f3457a5df918d279a4e192fabe1ef0f8b47592364",  # popcorn in sha512

                 "file name": "realuniq.txt",                   # very short runtime in dic.txt
                 "single": "True"})                    # (short run time on realuniq dictionary ~18M lines)

    settings.append( {"cracking method": "dic",  # settings[2]
                 "algorithm": "md5",
                 "hash": "9d86c2b0caad030430c093530b77ba63",  # Sixth line from the bottom, non-ascii characters (md5)
                 "file name": "realuniq.txt",
                 "single": "True"
                 })                   # (longest run time on realuniq dictionary ~1.2B lines)

    settings.append( {"cracking method": "bf",  # settings[3]
                      "algorithm": "MD5",
                      #"hash": "d60d3056ff09d8d9a26da4fc116c7554",
                      "hash": "12c8de03d4562ba9f810e7e1e7c6fc15",  # aa9999 in md5  -short runtime
                      #"hash": "96f36b618b63f4c7f22a34b6cd2245467465b355",  # aa9999 in sha1
                      #"hash": "76c2436b593f27aa073f0b2404531b8de04a6ae7",  # apples in sha1  -fairly long runtime
                      #"hash": "dd9f980ae062d651ba2bf65053273dd25eafaa0ab3086909e3d0934320a66ad1",  # aa9999 in sha256
                      #"hash": "57178f9de330d80155a1f5feca08569cede59da3e5d59b3e3a861c93e37b44cdda355023bc74cb10c495f53413981373a78e9926bf249d3b862c795f23ee1d9c",  # aa9999 in sha512
                      "min key length": 6,                         # short runtime
                      "max key length": 16,
                      "alphabet": string.ascii_letters+string.digits+string.punctuation+' ',
                      "single": "False"})

    settings.append({"cracking method": "rainmaker",  # settings[4]
                     "algorithm": "md5",
                     "key length": 10,
                     "alphabet": string.ascii_letters+string.digits+string.punctuation,
                     "chain length": 100,
                     "num rows": 1000,
                     "file name": "rain2.txt",
                     "single": "True"})

    settings.append({"cracking method": "rainmaker",  # settings[5]
                     "algorithm": "md5",
                     "key length": 10,
                     "alphabet": string.ascii_letters+string.digits+string.punctuation,
                     "chain length": 100,
                     "num rows": 1000,
                     "file name": "rain.txt",
                     "single": "False"})

    settings.append({"cracking method": "rain",  # settings[6]
                     "file name": "rain.txt",
                     #"hash": "d9af1fd83c9a1c30a7cc38c59acb31d7",   # pythagoras in md5
                     "hash": "51fe5861351b604b32f8dfdf4fa3beca",
                     "single": "True"})

    settings.append({"cracking method": "rain",  # settings[7]
                     "file name": "rain.txt",
                     #"hash": "d9af1fd83c9a1c30a7cc38c59acb31d7",   # pythagoras in md5
                     "hash": "51fe5861351b604b32f8dfdf4fa3beca",
                     "single": "False"})

    def __init__(self):
        return

    def start_server(self):
        #use a generic manager's shared dictionary to handle strings and ints
        manager = Manager()
        dictionary = manager.dict()
        dictionary["key"] = ''
        dictionary["finished chunks"] = 0

        # update is an event intended to be set by server to let the UI know that the shared dictionary has been updated.
        update = Event()
        update.clear()

        # shutdown is linked to the server/client shared shutdown command, setting this should shutdown server and clients.
        shutdown = Event()
        shutdown.clear()

        # shared is just an array, each shared variable is added to allow passing all shared values using one variable.
        shared = []
        shared.append(dictionary)
        shared.append(shutdown)
        shared.append(update)

        self.server = Process(target=Server, args=(self.settings[7], shared))
        self.server.start()

        # this is a very simple example of how an update loop in the UI classes might work
        while not shutdown.is_set():
            # update is an Event, this means that a process can use the .wait() command to block until it is .set()
            update.wait()
            os.system('cls' if os.name == 'nt' else 'clear')
            if dictionary["key"] is not '':
                print "Printing key from start_server method: " + dictionary["key"]
            print "%d chunks completed." % dictionary["finished chunks"]
            # after UI data has been updated, .clear() the update event so it will wait again in the next iteration
            update.clear()

        print "end"
        #self.server.join()
        self.server.terminate()


if __name__ == '__main__':
    start = start()
    start.start_server()