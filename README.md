*************'s Project for UWyo COSC 4950/5
============================================

Authors: Chris Hamm, John Wright, Nick Baum, Chris Bugg
Group #7, *************

Project Name: Mighty Cracker

Description:
This is a Python 2.7.8 Distributed, Multi-Process, Multi-Platform, GUI hash cracker. The goal of this project is to 
take a hash and run through our different methods and return the un-hashed password. To start we can crack a password 
that has been hashed using on of the following hashing algorithms. sha244, sha256, sha512, sha1, md5. In the future we 
hope to include more hashing algorithms.

Our methods include dictionary, brute force, and rainbow table. Dictionary will take a list of most common passwords
and hash them using the selected algorithm and compare it to the hash that is given, when a match is found it will 
return the un-hashed password. Brute Force will run through every possible combination of letters, numbers, and symbols
and hash them until it is matched with the original hash. Rainbow table will use a rainbow table to compare hashes and
return the un-hashed password.

For this project we plan on having a GUI mode and a terminal mode. With these two modes a user can run the program in 
either single user mode or network mode. Single user mode is only one computer working to find the password associated 
with the hash algorithm. network mode will divide up the work between two or more computers to find the un-hashed 
password faster.


For Grader:

Our designs and concepts (along with an ER-ish Diagram) are in the Resources folder,
which may be helpful to browse before delving into the source.

The source contains Seven files:

Controller.py -> This is the main, 'controlling' class which acts as an interface
                    between the GUI, the Networking, and the other classes.
                    
GUI.py ->        This is the GUI class which is responsible to all User-Interaction
                    and Display of information to the user. That's all it does.
                    
Networking.py -> This is the class that provides for all communication between the 
                    server and the nodes (for the distributed aspect).
                    
Brute_Force.py ->This is the class that does all the work in regards to our Brute-Force
                    capabilities. It talks only with the Controller.py class to get and
                    give information.