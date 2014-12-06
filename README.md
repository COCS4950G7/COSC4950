*************'s Project for UWyo COSC 4950/5
============================================

Authors: Chris Hamm, John Wright, Nick Baum, Chris Bugg

Mighty Cracker

This is a Python2 Distributed, Multi-Process, Multi-Platform, GUI hash cracker.


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