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
            #possible flags (RECOMMEND USING SWITCH-CASE STATEMENTS HERE)
                #a-z (contain in array)
                #A-Z (contain in array)
                #0-9 (contain in array)
                #special symbols !@#$%^&*()_+-=\|/ etc (contain in array)
                #All ASCII characters (includes all of the above) (contains all of the arrays listed above in one big array)
    #need to correct import file based on set flag values
    #need to use password read from file and try to get the matching hash until found or end of file
    #needs to output progress also