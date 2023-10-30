import math

class Cache:
    # Initializing class members as private
    def __init__(self, blockSize, size, assoc, replacementPolicy, inclusionPolicy):
        self._blockSize = blockSize
        self._size = size
        self._assoc = assoc
        # Handling fully associative case, when assoc is given as 0
        if(self._assoc == 0 and self._size !=0):
            # when fully associative sets = 1 and assoc = no of blocks = size/blocksize
            self._assoc = int(self._size//self._blockSize)
        self._replacementPolicy = replacementPolicy
        self._inclusionPolicy = inclusionPolicy

        # If the size is not qual to 0 calculate the no of bits for index, tag and offset
        if(self._size != 0):
            self._noOfSets = int(self._size//(self._assoc*self._blockSize))
            self._noOfIndexBits = int(math.log2(self._noOfSets))
            self._noOfOffsetBits = int(math.log2(self._blockSize))
            self._noOfTagBits = 32-self._noOfIndexBits-self._noOfOffsetBits
        # If the size is 0 it means cache is not present
        else:
            self._noOfSets = 0
            self._noOfIndexBits = 0
            self._noOfOffsetBits = 0
            self._noOfTagBits = 0
        
        self._initiateCache()
        self._initiateCount()

    # Initiaing all counter with 0
    def _initiateCount(self):        
        self._readCount = 0
        self._writeCount = 0
        self._readMissCount = 0
        self._writeMissCount = 0
        self._writeBackCount = 0
        self._writeBackToMemCount = 0

    # Initiating cache with tag = -1 and dirty bit False for all blocks and initializing tag store with all tags = -1
    def _initiateCache(self):
        self._cache = [[{'tag' : -1,'isDirty':False,'address':0}]*self._assoc for _ in range(self._noOfSets)]
        self._tagCache = [[{'tag' : -1}]*self._assoc for _ in range(self._noOfSets)]
    
    # From the given hex address extracting the bits indicating index and tag 
    def _getTagAndIndex(self,address):
        binary = bin(int(address, 16))[2:].zfill(32)
        tagBits , indexBits  = binary[:self._noOfTagBits], binary[self._noOfTagBits:self._noOfTagBits+self._noOfIndexBits]
        # If there are no index bits then it means fully associative and map to set 0
        if indexBits == '':
            indexBits = '0'
        return tagBits , indexBits
    
    def _handleMiss(self,address,tag,index):
        # When miss occurs allocate the new address in place of victim block
        victimBlock = self._replacementPolicy.allocate(address,tag, self._cache[int(index,2)],self._tagCache[int(index,2)])
        # If replaced block is not empty block 
        if(victimBlock['tag'] != -1):
            victimAddress = victimBlock['address']
            # If evicted block is dirty do write back
            if victimBlock['isDirty']:
                self._writeBackCount += 1
                # write to L2
                self._outerCache.write(victimAddress)
            if self._inclusionPolicy == '1':
                # If inclusion policy then invalidate the address in L1
                try:
                    self._innerCache.inValidate(victimAddress)
                except:
                    pass
        # After allocating place for the block do a read to L2
        try:
            self._outerCache.read(address)
        except:
            pass

    # Link L1 to L2
    def attachInnerCache(self,innerCache):
        self._innerCache = innerCache

    # Link L2 to L1
    def attachOuterCache(self,outerCache):
        self._outerCache = outerCache
    
    def inValidate(self,address):
        tag,index = self._getTagAndIndex(address)
        # Remove the invalidated address from L1
        for block in self._cache[int(index,2)]:
            if tag == block['tag']:
                # If the invalidated block is dirty then write back directly to memory
                if block['isDirty']:
                    # self._writeBackCount += 1 (Do Not count this as normal write back as its not writing to L2)
                    self._writeBackToMemCount +=1
                # Make the block empty
                block['tag'] = -1
                block['isDirty'] = False
                break
        # Remove the invalidated address from Tag store as well
        for tagBlock in self._tagCache[int(index,2)]:
            if tag == tagBlock['tag']:
                tagBlock['tag'] = -1
                break
        
    def read(self,address):
        # If size is 0 then return as there is no cache available
        if not self._size:
            return
        
        self._readCount += 1
        # Getting tagId and index from the address
        tag,index = self._getTagAndIndex(address)
        isMiss = True
        # Check if the current tag is present in cache
        for block in self._cache[int(index,2)]:    
            if tag == block['tag']:
                # If block is present then update the tag store appropriatly w.r.t replacement policy
                self._replacementPolicy.update(block,self._tagCache[int(index,2)])
                isMiss = False
                break
        # If cache miss increase miss count and handle miss
        if isMiss:
            self._readMissCount += 1
            self._handleMiss(address,tag,index)
            

    def write(self,address):
        # If size is 0 then return as there is no cache available
        if not self._size:
            return
        
        self._writeCount += 1
        # Getting tagId and index from the address
        tag,index = self._getTagAndIndex(address)
        isMiss = True

        # Check if the current tag is present in cache
        for block in self._cache[int(index,2)]:
            if tag == block['tag']:
                # As this is as write operation mark the current block as dirty
                block['isDirty'] = True
                # If block is present then update the tag store appropriatly w.r.t replacement policy
                self._replacementPolicy.update(block,self._tagCache[int(index,2)])
                isMiss = False
                break
        # If cache miss increase miss count and handle miss
        if isMiss:
            self._writeMissCount += 1
            self._handleMiss(address,tag,index)
            # Mark the newly allocated block as dirty 
            for block in self._cache[int(index,2)]:
                if tag == block['tag']:
                    block['isDirty'] = True
  
    # Getters for the private variables
    def getBlockSize(self):
        return self._blockSize
    
    def getSize(self):
        return self._size
    
    def getAssoc(self):
        return self._assoc
    
    def getReadCount(self):
        return self._readCount
    
    def getWriteCount(self):
        return self._writeCount
    
    def getReadMissCount(self):
        return self._readMissCount
    
    def getWriteMissCount(self):
        return self._writeMissCount
    
    def getWriteBackCount(self):
        return self._writeBackCount
    
    def getWriteBackToMemCount(self):
        return self._writeBackToMemCount
    
    def getCache(self):
        return self._cache
