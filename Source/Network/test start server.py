# This is a shortcut method to start server without any UI. For debugging purposes only.

from multiprocessing import Process
from NetworkServer_r15a import Server
import string

class start():

    client = Process()
    server = Process()
    settings = []
    settings.append({"cracking method": "dic",  # settings[0]
                "algorithm": "SHA512",
                #"hash": "b17a9909e09fda53653332431a599941",  # Karntnerstrasse-Rotenturmstrasse in md5
                #"hash": "e7c0efb2dc699ede79983b8dfb5cb509ebf2bde9",  # Karntnerstrasse-Rotenturmstrasse in sha1
                #"hash": "7ab5f3733019c9e594526c9beb70c0cc51517b91a6557f4b4306564b753232af",  # Karntnerstrasse-Rotenturmstrasse in sha256
                "hash": "86034bef1d027523698b6a0768bb024fafb11d9b23890cd1829592e12c5ef0fa83e6eee93adc4919296b4ffa957ce036139a39b2bd6301d4fdae03bdbeab96a3",  # Karntnerstrasse-Rotenturmstrasse in sha512
                "file name": "realuniq",                    # last word in dic.txt
                "single": "False"})                    # (long runtime on realuniq dictionary ~755M lines)

    settings.append({"cracking method": "dic",  # settings[1]
                 "algorithm": "sha1",
                 "hash": "33da7a40473c1637f1a2e142f4925194",  # popcorn
                 "file name": "dic",                   # very short runtime in dic.txt
                 "single": "True"})                    # (short run time on realuniq dictionary ~18M lines)

    settings.append( {"cracking method": "dic",  # settings[2]
                 "algorithm": "md5",
                 "hash": "9d86c2b0caad030430c093530b77ba63",  # Sixth line from the bottom, non-ascii characters
                 "file name": "realuniq",
                 })                   # (longest run time on realuniq dictionary ~1.2B lines)

    settings.append( {"cracking method": "bf",  # settings[3]
                 "algorithm": "sha1",
                 #"hash": "12c8de03d4562ba9f810e7e1e7c6fc15"  # aa9999 in md5  -short runtime
                 #"hash": "96f36b618b63f4c7f22a34b6cd2245467465b355",  # aa9999 in sha1
                 "hash": "76c2436b593f27aa073f0b2404531b8de04a6ae7",  # apples in sha1  -fairly long runtime
                 #"hash": "dd9f980ae062d651ba2bf65053273dd25eafaa0ab3086909e3d0934320a66ad1",  # aa9999 in sha256
                 #"hash": "57178f9de330d80155a1f5feca08569cede59da3e5d59b3e3a861c93e37b44cdda355023bc74cb10c495f53413981373a78e9926bf249d3b862c795f23ee1d9c",  # aa9999 in sha512
                 "min key length": 6,                         # short runtime
                 "max key length": 16,
                 "alphabet": string.ascii_letters+string.digits+string.punctuation,
                 "single": "True"})

    settings.append({"cracking method": "rainmaker",  # settings[4]
                     "algorithm": "md5",
                     "key length": 10,
                     "alphabet": string.ascii_letters+string.digits+string.punctuation,
                     "chain length": 10000,
                     "num rows": 1000,
                     "file name": "rain.txt",
                     "single": "True"})

    settings.append({"cracking method": "rainmaker",  # settings[4]
                     "algorithm": "md5",
                     "key length": 10,
                     "alphabet": string.ascii_letters+string.digits+string.punctuation,
                     "chain length": 10000,
                     "num rows": 1000,
                     "file name": "raintable.txt",
                     "single": "False"})

    def __init__(self):
        #self.start_server()
        return

    def start_server(self):
        self.server = Process(target=Server, args=(self.settings[5],))
        self.server.start()
        self.server.join()
        self.server.terminate()


if __name__ == '__main__':
    start = start()
    start.start_server()