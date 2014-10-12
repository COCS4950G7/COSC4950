#   Dictonary.py

#   Uses a dictionary file to attempt to crack the hash.
#   Simply reads through the file line by line, and tries each entry.
#   Possible source for passwords are 'top most used passwords' lists

# Updated on 10/12/2014:
#   Chris Hamm is working on this section.
#   added in comments and some thoughts

class Dictionary():
    # needs to take parameters like lowercase alpha, uppercase alpha, numerical. special symbols, etc

    #class variables
    done = False

    #need to create constructor
        #create flags for local variables
            #possible flags
                #a-z
                #A-Z
                #0-9
                #special symbols !@#$%^&*()_+-=\|/ etc
                #All ASCII characters (includes all of the above)
    #need to correct import file based on set flag values
    #need to use password read from file and try to get the matching hash until found or end of file
    #needs to output progress also