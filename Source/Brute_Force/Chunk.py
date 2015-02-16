#   Chunk.py

#   Defines a general chunk object to be used
#   with Controller, Networks, and Attack Method classes


class Chunk():

    #params defines the parameters of the data, so the data can be re-accesed should it get lost
    #also so controller can parse chunk and send it to appropriate class
    """
    It's form should be (with possible examples):

        "method algorithm hash alphabetChoice minCharacters maxCharacters prefix fileLocation width height"
        "dictionary md5 c548ea990e910339a122aa466ee7f971 0 0 100 0 231 0 0"
        "bruteforce sha1 7cacb75c4cc31d62a6c2a0774cf3c41a70f01bc0 d 1 12 1234 0 0 0"
        "rainbowmaker sha256 63b0490d4736e740f26ea9483d55c254abe032845b70ba84ea463ca6582d106f M 6 6 0 0 1000 20000:

        with '0' being a default value if that value is not needed (like filelocation in bruteForce)

    Possible Values:
        method = bruteforce/dictionary/rainbowmaker/rainbowuser
        algorithm = md5/sha1/sha256/sha512
        hash = pou234rpoiu2orpiu3roi3rpo8uo3r30r9u20359
        alphabetChoice = a/A/m/M/d
        minCharacters = 1/10/16
        maxCharacters = 1/10/16
        prefix = adf/234/qw3#k
        fileLocation = 0/1213/23665
        width = 1/100/100000
        height = 1/100/10000

    """
    params = ""
    #data defines the actual data of the chunk, which depends on the attack method, so it could be any string
    data= ""