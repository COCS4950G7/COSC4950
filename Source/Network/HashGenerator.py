# This script is just to save me having to go out and find a hash generator every time I want to test something.
# It takes in a string from the command line and outputs a hash for each algorithm in the python hashlib.

import hashlib

key = raw_input("enter key: ")
for algorithm in hashlib.algorithms:
    print "The %s hash representation of %s is: " % (algorithm, key)
    print hashlib.new(algorithm, key).hexdigest()