# This script is just to save me having to go out and find a hash generator every time I want to test something.
# It takes in a string from the command line and outputs a hash for each algorithm in the python hashlib.

import hashlib
from passlib.context import CryptContext

schemes = ["sha1_crypt", "sha256_crypt", "sha512_crypt", "md5_crypt",
           "des_crypt", 'ldap_salted_sha1', 'ldap_salted_md5',
           'ldap_sha1', 'ldap_md5', 'ldap_plaintext', "mysql323"]
myctx = CryptContext(schemes)

key = raw_input("enter key: ")
print "hashlib hashes:\n"
for algorithm in hashlib.algorithms:
    print "The %s hash representation of %s is: " % (algorithm, key)
    print hashlib.new(algorithm, key).hexdigest()

print "\npasslib hashes:\n"

for algorithm in schemes:
    print "The %s hash representation of %s is: " % (algorithm, key)
    print myctx.encrypt(key, algorithm)


hash1 = myctx.encrypt(key, 'ldap_md5')

if myctx.verify(key, hash1):
    print "true"
else:
    print "false"