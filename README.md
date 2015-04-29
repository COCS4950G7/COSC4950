*************'s Project for UWyo COSC 4950/5
============================================

Authors: Chris Hamm, John Wright, Nick Baum, Chris Bugg
Group #7, *************, (13-stars)

Project Name: Mighty Cracker

Description:
Our project, Mighty Cracker, is a program designed to crack hashed passwords. It is stand-alone, GUI, and can run on Mac 10+,
Linux 14+, and Windows 7+. It uses the power of multiprocessing to fully utilize every computer available, and can utilize
a LAN to distribute the workload over up to 90 computers (nodes). For now, the algorithms that it can utilize are: sha 224,
sha 256, sha 384, sha 512, sha 1, and md5, which cover a fair amount of the common hashing algorithms used.

We've implemented three common "attack methods" to find an original password. 
    Dictionary takes a list of passwords, hashes them, and compares the hashes to the original (user inputted) hash to 
        find a match. 
    Brute Force will iterate through any combination (up to 16 characters) of letters, numbers, and symbols to "brute-force" 
        the password, returning an original if found. 
    Rainbow Tables are pre-computed arrays of hashes, organized to to provide a time-cost trade-off. The creator creates 
        tables to be used at a later time, and the user uses created tables. This gives one a huge advantage if you know 
        what the password will consist of ahead of time.

These three methods can all be used on either a single computer (single-user mode) or on a network of computers (similar
to a Beowulf cluster). When using on headless systems, the program can run in terminal (text-only) mode with a "-C" command.

Because of the distributed, multi-process, simple GUI approach this program takes, it is potentially more powerful and more user-friendly
than most other hash cracking software out there today, making it more accessible for more people. Simply open the executable
and crack passwords.

In the future we'd like to add on the ability to crack the LMT-family of hashes (Windows) as well as add in GPU support for
additional power. 

For Grader:

Our designs and concepts (along with an ER-ish Diagram) are in the Resources folder,
which may be helpful to browse before delving into the source. At the moment we have several versions of each file,
please assume that the most current version (Latest Stable Versions) is the correct one to look at.

The Latest_Stable_Versions folder contains several files:

ConsoleUI.py -> This is a main class that runs the console-only version of the program.
                    It only talks to the networking classes.
                    
GUI.py ->        This is the GUI class which is responsible to all User-Interaction
                    and Display of information to the user. It only talks to the networking classes.
                    
NetworkClient.py -> These are the class's that provides for all communication between the 
NetworkServer.py      server and the nodes (for the distributed aspect). They are directly run
                        by the UIs and then in turn directly run the attack method classes.
                    
Brute_Force.py -> This is the class that does all the work in regards to our Brute-Force capabilities.
                    It is run directly by the network classes when appropriate.
                    
Dictionary.py -> This is the class that does all the work in regards to our Dictionary capabilities.
                    It is run directly by the network classes when appropriate.
    
dic.txt       -> This is the word file for use with the Dictionary.py, in future we hope to have some more,
                     some could be simple dictionary words, others could be list of most common passwords.
                     
RainbowMaker.py -> This is the class that does all the work in regards to making rainbow tables.
                    It is run directly by the network classes when appropriate.

RainbowUser.py -> This is the class that does all the work in regards to using rainbow tables.
                    It is run directly by the network classes when appropriate.