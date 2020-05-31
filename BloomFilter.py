from BitHash import BitHash
from BitVector import BitVector

class BloomFilter(object):
    # Return the estimated number of bits needed in a Bloom Filter that 
    # will store numKeys keys, using numHashes hash functions, and that 
    # will have a false positive rate of maxFalsePositive.
    # See Slide 12 for the math needed to do this.  
    # You use equation B to get the desired phi from P and d
    # You then use equation D to get the needed N from d, phi, and n
    # N is the value to return from bitsNeeded
    def __bitsNeeded(self, numKeys, numHashes, maxFalsePositive):
        phi = 1- (maxFalsePositive**(1/numHashes))
        N = int(numHashes/(1-phi**(1/numKeys)))
        return N
    
    # Create a Bloom Filter that will store numKeys keys, using 
    # numHashes hash functions, and that will have a false positive 
    # rate of maxFalsePositive.
    # All attributes must be private.
    def __init__(self, numKeys, numHashes, maxFalsePositive):
        # will need to use __bitsNeeded to figure out how big
        # of a BitVector will be needed
        self.__numHashes =numHashes 
        self.__numKeys = numKeys 
        self.__falsePositive = maxFalsePositive
        self.__numBitsSet = 0
        self.__bitVectorSize = self.__bitsNeeded(numKeys,numHashes,maxFalsePositive)
        self.__bitVector = BitVector(size = self.__bitVectorSize)

#decide which attributes it will need in order to work the other ones. 
    
    # insert the specified key into the Bloom Filter.
    # Doesn't return anything, since an insert into 
    # a Bloom Filter always succeeds!
    def insert(self, key):
        H = 0
        for i in range (self.__numHashes):
            H = BitHash(key, H)
            pos = H % self.__bitVectorSize
            if self.__bitVector[pos] !=1:
                self.__numBitsSet +=1 
                self.__bitVector[pos] = 1
        
            
            
    # Returns True if key MAY have been inserted into the Bloom filter. 
    # Returns False if key definitely hasn't been inserted into the BF.   
    def find(self, key):
        H = 0
        for i in range (self.__numHashes):
            H = BitHash(key, H)
            pos = H % self.__bitVectorSize
            if self.__bitVector[pos] !=1:
                return False 
        return True 
       
    # Returns the PROJECTED current false positive rate based on the
    # ACTUAL current number of bits set in this Bloom Filter. 
    # This is NOT the same thing as trying to use the Bloom Filter and
    # actually measuring the proportion of false positives that 
    # are actually encountered.
    # In other words, you use equation A to give you P from d and phi. 
    # What is phi in this case? it is the ACTUAL measured current proportion 
    # of bits in the bit vector that are still zero. 
    def falsePositiveRate(self):
        phi = (self.__bitVectorSize-self.__numBitsSet)/self.__bitVectorSize
        P = ((1 - phi)**self.__numHashes)*100
        return P
       
    # Returns the current number of bits ACTUALLY set in this Bloom Filter
    # WHEN TESTING, MAKE SURE THAT YOUR IMPLEMENTATION DOES NOT CAUSE
    # THIS PARTICULAR METHOD TO RUN SLOWLY.
    def numBitsSet(self):
        return self.__numBitsSet
# tell client how many bits are set in the underlyin bit vector. 

       

def __main():
    numKeys = 100000
    numHashes = 4
    maxFalse = .05
    
    # create the Bloom Filter
    B = BloomFilter(numKeys,numHashes,maxFalse)
    
    # read the first numKeys words from the file and insert them 
    # into the Bloom Filter. Close the input file.
    
    file = open("wordlist.txt")
    word = file.readline()
    for i in range(numKeys):
        B.insert(word)
        word = file.readline()
    file.close()
    # Print out what the PROJECTED false positive rate should 
    # THEORETICALLY be based on the number of bits that ACTUALLY ended up being set
    # in the Bloom Filter. Use the falsePositiveRate method.
    print("Theoretical False Positive Rate using the Bloom Filter Method = ", B.falsePositiveRate())
    # Now re-open the file, and re-read the same bunch of the first numKeys 
    # words from the file and count how many are missing from the Bloom Filter, 
    # printing out how many are missing. This should report that 0 words are 
    # missing from the Bloom Filter. Don't close the input file of words since
    # in the next step we want to read the next numKeys words from the file. 
    file = open("wordlist.txt")
    word = file.readline()
    count = 0
    for i in range(numKeys):
        test = B.find(word)
        if not test:
            count+=1
        word = file.readline()
    print ("count = ", count, "# Count should be zero")
    # Now read the next numKeys words from the file, none of which 
    # have been inserted into the Bloom Filter, and count how many of the 
    # words can be (falsely) found in the Bloom Filter.
    count = 0 
    for i in range(numKeys):
        test = B.find(word)
        if test:
            count+=1
        word = file.readline()  
    file.close()    
    # Print out the percentage rate of false positives.
    # THIS NUMBER MUST BE CLOSE TO THE ESTIMATED FALSE POSITIVE RATE ABOVE
    print("Actual False Positive Rate = ", (count/numKeys)*100)

if __name__ == '__main__':
    __main()       

