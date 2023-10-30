import math

class Cache:
    def __init__(self, blockSize, size, assoc, replacementPolicy, inclusionPolicy):
        self._blockSize = blockSize
        self._size = size
        self._assoc = assoc
        if(self._assoc == 0 and self._size !=0):
            self._assoc = int(self._size//self._blockSize)
        self._replacementPolicy = replacementPolicy
        self._inclusionPolicy = inclusionPolicy

        if(self._size != 0):
            self._noOfSets = int(self._size//(self._assoc*self._blockSize))
            self._noOfIndexBits = int(math.log2(self._noOfSets))
            self._noOfOffsetBits = int(math.log2(self._blockSize))
            self._noOfTagBits = 32-self._noOfIndexBits-self._noOfOffsetBits
        else:
            self._noOfSets = 0
            self._noOfIndexBits = 0
            self._noOfOffsetBits = 0
            self._noOfTagBits = 0
        
        self._initiateCache()
        self._initiateCount()

    def _initiateCount(self):        
        self._readCount = 0
        self._writeCount = 0
        self._readMissCount = 0
        self._writeMissCount = 0
        self._writeBackCount = 0
        self._writeBackToMemCount = 0

    def _initiateCache(self):
        self._cache = [[{'tag' : -1,'isDirty':False,'address':0}]*self._assoc for _ in range(self._noOfSets)]
        self._tagCache = [[{'tag' : -1}]*self._assoc for _ in range(self._noOfSets)]
    
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

    def attachInnerCache(self,innerCache):
        self._innerCache = innerCache

    def attachOuterCache(self,outerCache):
        self._outerCache = outerCache

    def _getTagAndIndex(self,address):
        binary = bin(int(address, 16))[2:].zfill(32)
        tagBits , indexBits  = binary[:self._noOfTagBits], binary[self._noOfTagBits:self._noOfTagBits+self._noOfIndexBits]
        if indexBits == '':
            indexBits = '0'
        return tagBits , indexBits
    
    def inValidate(self,address):
        tag,index = self._getTagAndIndex(address)
        for block in self._cache[int(index,2)]:
            if tag == block['tag']:
                block['tag'] = -1
                if block['isDirty']:
                    self._writeBackToMemCount +=1
                block['isDirty'] = False
                break
        for tagBlock in self._tagCache[int(index,2)]:
            if tag == tagBlock['tag']:
                tagBlock['tag'] = -1
                tagBlock['isDirty'] = False
                break

    def _handleMiss(self,address,tag,index):
        victimBlock = self._replacementPolicy.allocate(address,tag, self._cache[int(index,2)],self._tagCache[int(index,2)])
        if(victimBlock['tag'] != -1):
            victimAddress = victimBlock['address']
            if victimBlock['isDirty']:
                self._writeBackCount += 1
                self._outerCache.write(victimAddress)
            if self._inclusionPolicy == '1':
                try:
                    self._innerCache.inValidate(victimAddress)
                except:
                    pass
        try:
            self._outerCache.read(address)
        except:
            pass
        
    def read(self,address):
        if not self._size:
            return
        
        self._readCount += 1
        tag,index = self._getTagAndIndex(address)
        isMiss = True
        
        for block in self._cache[int(index,2)]:    
            if tag == block['tag']:
                self._replacementPolicy.update(block,self._tagCache[int(index,2)])
                isMiss = False
                break
        
        if isMiss:
            self._readMissCount += 1
            self._handleMiss(address,tag,index)
            

    def write(self,address):
        if not self._size:
            return
        
        self._writeCount += 1
        tag,index = self._getTagAndIndex(address)
        isMiss = True

        for block in self._cache[int(index,2)]:
            if tag == block['tag']:
                block['isDirty'] = True
                self._replacementPolicy.update(block,self._tagCache[int(index,2)])
                isMiss = False
                break
        
        if isMiss:
            self._writeMissCount += 1
            self._handleMiss(address,tag,index)
            for block in self._cache[int(index,2)]:
                if tag == block['tag']:
                    block['isDirty'] = True
