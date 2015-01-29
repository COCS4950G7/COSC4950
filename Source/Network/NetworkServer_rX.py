__author__ = 'chris hamm'
#NetworkServer_rX (revision 10)
#Created: 1/27/2015
#Designed to work with NetworkClient_rX

#THINGS ADDED/CHANGED WITH THIS VERSION
    #(Implemented)Removed Chunk Parsing Functions (these functions are no longer needed)
    #(Implemented)Restructure the primary loop of the server so that the server responds to a clients message immeadiately (instead of listen to client, then listen to controller, then distribute commands)
    #(Implemented)Change the recv (from controller) mechanism so that server expects two messages from the controller (string, then a chunk object)
    #(Have not started to implement yet)Change Communication functions to just check for what type of message
    #(In Progress)New data containers
        #(Have not started to implement yet)Stack containing chunks that need to be reassigned due to a client crash
        #(In Progress)Stack of clients waiting for nextChunk
    #(In Progress)Remove data structures
        #(In Progress)Remove list of clients waiting for reply (to be replaced by stack of clients waiting for nextChunk)
        #(In Progress)Remove the list of controller messages (No longer needed since server reacts immediately)

#THINGS STILL BEING INTEGRATED FROM REVISION 9E
    #(In progress)Send extracted information over the network to the client

#THINGS STILL BEING INTEGRATED FROM REVISION 9D
    #(Have not started implementing yet) A list of what each client is currently working on
    #(Have not started implementing yet) A list of chunk objects that contains the chunk of a crashed client (chunk added when client crashes, and chunk is removed when a new client is given the chunk)

#====================================
#Imports
#====================================
#====================================
#End of Imports
#====================================

#==============================================================
#NetworkServer Class Definition
#==============================================================
    #-------------------------------------------------------------------
    #NetworkServer Class Variables
    #-------------------------------------------------------------------
    #-------------------------------------------------------------------
    #End of NetworkServer Class Variables
    #-------------------------------------------------------------------

    #-------------------------------------------------------------------
    #NetworkServer Class Constructor
    #-------------------------------------------------------------------
        #.........................................................................
        #Bind the Socket to local host and port
        #.........................................................................
        #.........................................................................
        #End of Bind the Socket to local host and port
        #.........................................................................

        #.........................................................................
        #Detect the Operating System
        #.........................................................................
        #.........................................................................
        #End of Detect the Operating System
        #.........................................................................

        #.........................................................................
        #Retrieve the local network IP Address
        #.........................................................................
        #.........................................................................
        #End of Retrieve the local network IP Address
        #.........................................................................

        #.........................................................................
        #Initialize the Record Counters
        #.........................................................................
        #.........................................................................
        #End of Initialize the Record Counters
        #.........................................................................

        #.........................................................................
        #Start Listening to the Socket
        #.........................................................................
        #.........................................................................
        #End of Start Listening to the Socket
        #.........................................................................

        #.........................................................................
        #Wait for initial client to connect
        #.........................................................................
        #.........................................................................
        #End of Wait for initial client to connect
        #.........................................................................

        #.........................................................................
        #Start of Primary Server While Loop
        #.........................................................................
            #/////////////////////////////////////////////////////////////////////////////
            #Check for input from clients
            #/////////////////////////////////////////////////////////////////////////////
            #'''GOAL: Want server to respond immeadiately when it receives a command from a client'''
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                #If Command is the Empty String (do not expect a chunk object)
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                #End of If Command is the Empty String
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                #Check for NEXT Command
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                    #************************************************************************************
                    #If it is the NEXT Command, send a nextChunk request to the controller
                    #************************************************************************************
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                #End of Check for NEXT Command
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                #Check for FOUNDSOLUTION Command
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                    #************************************************************************************
                    #(MAY be obsolete) I think this should only used in the client
                    #************************************************************************************
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                #End of Check for FOUNDSOLUTION Command
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                #Check for CRASHED Command
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                    #************************************************************************************
                    #If it is the CRASHED Command, add the chunk that client was working on to the crashed client chunk stack
                    #************************************************************************************
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                #End of Check for CRASHED Command
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                #If Command is Unknown, print Error
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                #End of If Command is Unknown, print Error
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            #/////////////////////////////////////////////////////////////////////////////
            #End of Check for input from Clients
            #/////////////////////////////////////////////////////////////////////////////

            #/////////////////////////////////////////////////////////////////////////////
            #Check for input from controller class
            #/////////////////////////////////////////////////////////////////////////////
            #'''GOAL: Want server to respond immeadiately when it receives a command from the controller class'''
            #'''GOAL: Change the recv function so that server expects two messages from controller, a string, then a chunk object'''
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                #Check for reply to next chunk command
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                    #************************************************************************************
                    #If it is the reply to next chunk command, receive the chunk object
                    #************************************************************************************

                    #************************************************************************************
                    #Once received chunk object, send info to the client in the waiting for nextChunk stack
                    #************************************************************************************
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                #End of Check for reply to next chunk command
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                #Check for reply to chunkAgain Command
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                    #************************************************************************************
                    #If it is the reply to chunkAgain command, receive the chunk object (May be obsolete if server holds the chunks)
                    #************************************************************************************
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                #End of Check for reply to chunkAgain Command
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                #Check for reply to done command
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                    #************************************************************************************
                    #(NOT SURE ABOUT THIS) Receive chunk object????
                    #************************************************************************************
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                #End of Check for reply to done command
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                #If Command is unknown, print out Error
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                #End of If Command is Unknown, print Error
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

            #/////////////////////////////////////////////////////////////////////////////
            #End of Check for input from controller class
            #/////////////////////////////////////////////////////////////////////////////

            #'''GOAL: To have this section (below) be removed, and have the above sections immeadiately respond to any received commands, instead of queuing the commands, then executing them'''
            #/////////////////////////////////////////////////////////////////////////////
            #Distribute Command(s) to Client(s) if needed
            #/////////////////////////////////////////////////////////////////////////////
            #/////////////////////////////////////////////////////////////////////////////
            #End of Distribute Command(s) to Client(s) if needed
            #/////////////////////////////////////////////////////////////////////////////
            #'''GOAL: Remove the section above'''

            #/////////////////////////////////////////////////////////////////////////////
            #Check to see if another client is trying to connect
            #/////////////////////////////////////////////////////////////////////////////
            #/////////////////////////////////////////////////////////////////////////////
            #End of Check to see if another client is trying to connect
            #/////////////////////////////////////////////////////////////////////////////
        #.........................................................................
        #End of Primary Server While Loop
        #.........................................................................
        #.........................................................................
        #Finally Block (where socket is closed)
        #.........................................................................
            #/////////////////////////////////////////////////////////////////////////////
            #Close the Socket
            #/////////////////////////////////////////////////////////////////////////////
            #/////////////////////////////////////////////////////////////////////////////
            #End of Close the Socket
            #/////////////////////////////////////////////////////////////////////////////

            #/////////////////////////////////////////////////////////////////////////////
            #Issue DONE command to all clients
            #/////////////////////////////////////////////////////////////////////////////
            #/////////////////////////////////////////////////////////////////////////////
            #End of Issue DONE command to all clients
            #/////////////////////////////////////////////////////////////////////////////

            #/////////////////////////////////////////////////////////////////////////////
            #Print List of Crashed Clients
            #/////////////////////////////////////////////////////////////////////////////
            #/////////////////////////////////////////////////////////////////////////////
            #End of Print list of Crashed Clients
            #/////////////////////////////////////////////////////////////////////////////

            #/////////////////////////////////////////////////////////////////////////////
            #Print Stack of Clients Waiting for nextChunk
            #/////////////////////////////////////////////////////////////////////////////
            #/////////////////////////////////////////////////////////////////////////////
            #End of Print Stack of clients waiting for nextChunk
            #/////////////////////////////////////////////////////////////////////////////

            #'''GOAL: Remove this data structure (below) and replace with new data structures (Listed right above this)'''
            #/////////////////////////////////////////////////////////////////////////////
            #Print list of clients waiting for a reply
            #/////////////////////////////////////////////////////////////////////////////
            #/////////////////////////////////////////////////////////////////////////////
            #End of Print list of Clients waiting for a reply
            #/////////////////////////////////////////////////////////////////////////////
            #'''GOAL: Remove the above data structure'''

            #'''GOAL: Remove this data structure (below) since no longer needed'''
            #/////////////////////////////////////////////////////////////////////////////
            #Print list of Controller Messages
            #/////////////////////////////////////////////////////////////////////////////
            #/////////////////////////////////////////////////////////////////////////////
            #End of print list of Controller Messages
            #/////////////////////////////////////////////////////////////////////////////
            #'''GOAL: Remove the above data structure'''

            #/////////////////////////////////////////////////////////////////////////////
            #Print Command Records
            #/////////////////////////////////////////////////////////////////////////////
            #/////////////////////////////////////////////////////////////////////////////
            #End of print command Records
            #/////////////////////////////////////////////////////////////////////////////

        #.........................................................................
        #End of Finally Block (where socket is closed)
        #.........................................................................

    #-------------------------------------------------------------------
    #End of NetworkServer Class Constructor
    #-------------------------------------------------------------------

    #-------------------------------------------------------------------
    #Defined Communication Functions
    #-------------------------------------------------------------------
        #.........................................................................
        #Server-Controller Communication Functions
        #.........................................................................
            #/////////////////////////////////////////////////////////////////////////////
            #Outbound Functions
            #/////////////////////////////////////////////////////////////////////////////
            #/////////////////////////////////////////////////////////////////////////////
            #End of Outbound Functions
            #/////////////////////////////////////////////////////////////////////////////

            #/////////////////////////////////////////////////////////////////////////////
            #Inbound Functions
            #/////////////////////////////////////////////////////////////////////////////
            #/////////////////////////////////////////////////////////////////////////////
            #End of Inbound Functions
            #/////////////////////////////////////////////////////////////////////////////
        #.........................................................................
        #End of Server-Controller Communication Functions
        #.........................................................................

        #.........................................................................
        #Server-Client Communication Functions
        #.........................................................................
            #/////////////////////////////////////////////////////////////////////////////
            #Outbound Functions
            #/////////////////////////////////////////////////////////////////////////////
            #/////////////////////////////////////////////////////////////////////////////
            #End of Outbound Functions
            #/////////////////////////////////////////////////////////////////////////////

            #/////////////////////////////////////////////////////////////////////////////
            #Inbound Functions
            #/////////////////////////////////////////////////////////////////////////////
            #/////////////////////////////////////////////////////////////////////////////
            #End of Inbound Functions
            #/////////////////////////////////////////////////////////////////////////////
        #.........................................................................
        #End of Server-Client Communication Functions
        #.........................................................................
    #-------------------------------------------------------------------
    #End of Defined Communication Functions
    #-------------------------------------------------------------------
#==============================================================
#End of NetworkServer Class Definition
#==============================================================

