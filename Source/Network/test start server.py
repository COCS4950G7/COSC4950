# This is a shortcut method to start server without any UI. For debugging purposes only.

from multiprocessing import Process
from NetworkServer_r15a import Server


class start():

    client = Process()
    server = Process()
    settings = {"cracking method": "dic",
                "algorithm": "md5",
                "hash": "b17a9909e09fda53653332431a599941", # Karntnerstrasse-Rotenturmstrasse
                "file name": "realuniq"}                    # (long runtime on realuniq dictionary ~755M lines)

    settings2 = {"cracking method": "dic",
                "algorithm": "md5",
                "hash": "33da7a40473c1637f1a2e142f4925194", # popcorn
                "file name": "realuniq"}                    # (short run time on realuniq dictionary ~18M lines)

    settings3 = {"cracking method": "dic",
                "algorithm": "md5",
                "hash": "9d86c2b0caad030430c093530b77ba63", # Sixth line from the bottom, non-ascii characters
                "file name": "realuniq"}                    # (longest run time on realuniq dictionary ~1.2B lines)

    def __init__(self):
        #self.start_server()
        return

    def start_server(self):
        self.server = Process(target=Server, args=(self.settings3,))
        self.server.start()
        self.server.join()
        self.server.terminate()


if __name__ == '__main__':
    start = start()
    start.start_server()