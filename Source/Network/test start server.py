# This is a shortcut method to start server without any UI. For debugging purposes only.

from multiprocessing import Process
from NetworkServer_r15a import Server
import string

class start():

    client = Process()
    server = Process()
    settings = []
    settings.append({"cracking method": "dic",
                "algorithm": "md5",
                "hash": "b17a9909e09fda53653332431a599941",  # Karntnerstrasse-Rotenturmstrasse
                "file name": "realuniq",
                "single": "True"})                    # (long runtime on realuniq dictionary ~755M lines)

    settings.append({"cracking method": "dic",
                 "algorithm": "md5",
                 "hash": "33da7a40473c1637f1a2e142f4925194",  # popcorn
                 "file name": "realuniq",
                 "single": "False"})                    # (short run time on realuniq dictionary ~18M lines)

    settings.append( {"cracking method": "dic",
                 "algorithm": "md5",
                 "hash": "9d86c2b0caad030430c093530b77ba63",  # Sixth line from the bottom, non-ascii characters
                 "file name": "realuniq",
                 })                   # (longest run time on realuniq dictionary ~1.2B lines)

    settings.append( {"cracking method": "bf",
                 "algorithm": "md5",
                 "hash": "12c8de03d4562ba9f810e7e1e7c6fc15",  # aa9999
                 "min key length": 6,
                 "max key length": 16,
                 "alphabet": string.ascii_letters+string.digits+string.punctuation,
                 "single": "False"})

    def __init__(self):
        #self.start_server()
        return

    def start_server(self):
        self.server = Process(target=Server, args=(self.settings[3],))
        self.server.start()
        self.server.join()
        self.server.terminate()


if __name__ == '__main__':
    start = start()
    start.start_server()