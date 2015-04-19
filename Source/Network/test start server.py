# This is a shortcut method to start server without any UI. For debugging purposes only.

from multiprocessing import Process, Event, Manager, current_process
from NetworkServer_r15c import Server
import string
import os
import time
import signal


class start():

    server = None
    settings = []
    debug_file = "/Users/327pzq/procs.txt"

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

                 "file name": "dic.txt",                   # very short runtime in dic.txt
                 "single": "False"})                    # (short run time on realuniq dictionary ~18M lines)

    settings.append( {"cracking method": "dic",  # settings[2]
                 "algorithm": "md5",
                 "hash": "9d86c2b0caad030430c093530b77ba63",  # Sixth line from the bottom, non-ascii characters (md5)
                 "file name": "realuniq.txt",
                 "single": "True"
                 })                   # (longest run time on realuniq dictionary ~1.2B lines)

    settings.append( {"cracking method": "bf",  # settings[3]
                      "algorithm": "md5",
                      #"hash": "d60d3056ff09d8d9a26da4fc116c7554",
                      #"hash": "12c8de03d4562ba9f810e7e1e7c6fc15",  # aa9999 in md5  -short runtime
                      "hash": "1f3870be274f6c49b3e31a0c6728957f",  # apple in md5
                      #"hash": "98ae126efdbc62e121649406c83337d9",  # aaaff in md5
                      #"hash": "96f36b618b63f4c7f22a34b6cd2245467465b355",  # aa9999 in sha1
                      #"hash": "76c2436b593f27aa073f0b2404531b8de04a6ae7",  # apples in sha1  -fairly long runtime
                      #"hash": "dd9f980ae062d651ba2bf65053273dd25eafaa0ab3086909e3d0934320a66ad1",  # aa9999 in sha256
                      #"hash": "57178f9de330d80155a1f5feca08569cede59da3e5d59b3e3a861c93e37b44cdda355023bc74cb10c495f53413981373a78e9926bf249d3b862c795f23ee1d9c",  # aa9999 in sha512
                      "min key length": 5,                         # short runtime
                      "max key length": 16,
                      "alphabet": string.ascii_letters+string.digits+string.punctuation+' ',
                      "single": "False"})

    settings.append({"cracking method": "rainmaker",  # settings[4]
                     "algorithm": "md5",
                     "key length": 10,
                     "alphabet": string.ascii_letters+string.digits+string.punctuation,
                     "chain length": 100,
                     "num rows": 3600,
                     "file name": "rain2.txt",
                     "single": "True"})

    settings.append({"cracking method": "rainmaker",  # settings[5]
                     "algorithm": "md5",
                     "key length": 10,
                     "alphabet": string.ascii_letters+string.digits+string.punctuation,
                     "chain length": 1000,
                     "num rows": 100,
                     "file name": "rain.txt",
                     "single": "False"})

    settings.append({"cracking method": "rain",  # settings[6]
                     "file name": "rain.txt",
                     #"hash": "d9af1fd83c9a1c30a7cc38c59acb31d7",   # pythagoras in md5
                     "hash": "9b6e7de86ccf4f9c05ac2504e132e414",
                     "single": "True"})

    settings.append({"cracking method": "rain",  # settings[7]
                     "file name": "myrain.txt",
                     #"hash": "d9af1fd83c9a1c30a7cc38c59acb31d7",   # pythagoras in md5
                     "hash": "11464b55161a44abe7e27ac44a2e6385",
                     "single": "False"})

    settings.append({"cracking method": "bf",  # settings[8]
                      "algorithm": "md5",
                      #"hash": "98ae126efdbc62e121649406c83337d9",
                      "hash": "daeccf0ad3c1fc8c8015205c332f5b42", # apples in md5
                      #"hash": "18b049cc8d8535787929df716f9f4e68",
                      "min key length": 1,                         # short runtime
                      "max key length": 6,
                      "alphabet": string.ascii_lowercase,
                      "single": "True"})

    settings.append({"cracking method": "bf",  # settings[9]
                      "algorithm": "md5",
                      "input file name": "top 500 password hashes.txt",
                      "output file name": "found passwords.txt",
                      "min key length": 1,
                      "max key length": 6,
                      "alphabet": string.ascii_lowercase,
                      "single": "True",
                      "file mode": True})

    settings.append({"cracking method": "dic",  # settings[10]
                      "algorithm": "md5",
                      "input file name": "top 500 password hashes.txt",
                      "output file name": "found passwords.txt",
                      "file name": "realuniq.txt",
                      "single": "True",
                      "file mode": True
                      })

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

        preset = 10
        if self.settings[preset]["single"] == "False":
            network = True
        else:
            network = False
        self.server = Process(target=Server, args=(self.settings[preset], shared))
        self.server.start()

        print "server pid: %i" % self.server.pid
        # this is a very simple example of how an update loop in the UI classes might work
        while not shutdown.is_set():
            # update is an Event, this means that a process can use the .wait() command to block until it is .set()
            update.wait(timeout=.5)
            print "%i chunks completed." % dictionary["finished chunks"]
            os.system('cls' if os.name == 'nt' else 'clear')
            if dictionary["key"] is not '':
                print "Printing key from start_server method: " + dictionary["key"]
                break
            #print "%d chunks completed of %i total." % (dictionary["finished chunks"], dictionary["total chunks"])
            # after UI data has been updated, .clear() the update event so it will wait again in the next iteration
            update.clear()
        shutdown.set()
        time.sleep(1)

        #self.server.terminate()
        self.server.join()
        self.server.terminate()
        #os.kill(self.server.pid, signal.SIGKILL)
        self.server.join()
        manager.shutdown()
        if network:
            print self.server.pid
            #os.kill(self.server.pid + 3, signal.SIGKILL)
            #os.kill(self.server.pid + 4, signal.SIGTERM)


if __name__ == '__main__':
    start = start()
    start.start_server()