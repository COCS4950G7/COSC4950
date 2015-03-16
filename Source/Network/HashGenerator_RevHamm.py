__author__ = 'Chris Hamm'
#HashGenerator_RevHamm

#this revision of the hash generator generates only the specified algorithm instead of all of them.
import hashlib
import sys

class hashGenerator():
    def __init__(self):
        self.inputKey= ""
        self.inputAlgorithm= ""
        #self.setInputAlgorithm()
        #self.setInpuKey()
        self.promptForInfo()

    def guiSetInputAlgorithm(self, inputAlgorithm):
        self.inputAlgorithm= inputAlgorithm

    def setInputAlgorithm(self, myAlg):
        self.inputAlgorithm= myAlg

    def setInpuKey(self, myInputKey):
        self.inputKey= myInputKey

    def promptForInfo(self):
        if(self.compareString(self.inputAlgorithm, "MD5", 0,0,len("MD5"),len("MD5")) == True):
            generatedHash= hashlib.new('MD5', self.inputKey).hexdigest()
            return str(generatedHash)
        elif(self.compareString(self.inputAlgorithm, "SHA1", 0,0, len("SHA1"), len("SHA1")) == True):
            generatedHash= hashlib.new('SHA1', self.inputKey).hexdigest()
            return str(generatedHash)
        elif(self.compareString(self.inputAlgorithm, "SHA224", 0,0, len("SHA224"), len("SHA224"))==True):
            generatedHash= hashlib.new('SHA224', self.inputKey).hexdigest()
            return str(generatedHash)
        elif(self.compareString(self.inputAlgorithm, "SHA256",0,0, len("SHA256"), len("SHA256"))==True):
            generatedHash= hashlib.new('SHA256', self.inputKey).hexdigest()
            return str(generatedHash)
        elif(self.compareString(self.inputAlgorithm, "SHA512",0,0, len("SHA512"), len("SHA512"))==True):
            generatedHash= hashlib.new('SHA512', self.inputKey).hexdigest()
            return str(generatedHash)
        else:
            print "Invalid algorithm."
            print "algorithm= '"+str(self.inputAlgorithm)+"'"


    def compareString(self,inboundStringA, inboundStringB, startA, startB, endA, endB):
        try:
            posA = startA
            posB = startB
            if((endA-startA) != (endB-startB)):
                return False
            for x in range(startA,endA):
                tempCharA= inboundStringA[posA]
                tempCharB= inboundStringB[posB]
                if(tempCharA != tempCharB):
                    return False
                posA+= 1
                posB+= 1
            return True
        except Exception as inst:
            print "========================================================================\n"
            print "Exception thrown in compareString Function: " +str(inst)+"\n"
            print "========================================================================\n"
            return False

def main(inputMode):
    hashGenerator(inputMode)

if __name__ == '__main__':
    main()