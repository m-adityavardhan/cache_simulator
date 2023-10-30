import sys,math,copy


class FIFO:
    def update(self,block,tagSet):
        pass

    def allocate(self,address,tag,set,tagSet):
        isAllocated = False
        removedBlock = 0
        for tagBlock in tagSet:
            if tagBlock['tag'] == -1:
                removedBlock = tagBlock
                tagSet.remove(tagBlock)
                tagSet.append({'tag':tag})
                isAllocated = True
                break          
        if (not isAllocated):
            removedBlock = tagSet.pop(0)
            tagSet.append({'tag':tag})
        for index,setBlock in enumerate(set):
            if setBlock['tag'] == removedBlock['tag']: 
                removedSetBlock = setBlock
                set.remove(setBlock)
                set.insert(index,{'tag':tag,'isDirty':False,'address':address})
                return removedSetBlock

        
class LRU(FIFO):
    def update(self,block,tagSet):
        movedBlock = 0
        for tagBlock in tagSet:
            if tagBlock['tag'] == block['tag']:
                movedBlock = tagBlock
                break
        tagSet.remove(movedBlock)
        tagSet.append(movedBlock)


class Cache:
    def __init__(self, blockSize, size, assoc, replacementPolicy, inclusionPolicy):
        self.blockSize = blockSize
        self.size = size
        self.assoc = assoc
        if(self.assoc == 0 and self.size !=0):
            self.assoc = int(self.size//self.blockSize)
        self.replacementPolicy = replacementPolicy
        self.inclusionPolicy = inclusionPolicy

        if(self.size != 0):
            self.noOfSets = int(self.size//(self.assoc*self.blockSize))
            self.noOfIndexBits = int(math.log2(self.noOfSets))
            self.noOfOffsetBits = int(math.log2(self.blockSize))
            self.noOfTagBits = 32-self.noOfIndexBits-self.noOfOffsetBits
        else:
            self.noOfSets = 0
            self.noOfIndexBits = 0
            self.noOfOffsetBits = 0
            self.noOfTagBits = 0
        
        self.initiateCache()

        self.readCount = 0
        self.writeCount = 0
        self.readMissCount = 0
        self.writeMissCount = 0
        self.writeBackCount = 0
        self.writeBackToMemCount = 0


    def initiateCache(self):
        self.cache = [[{'tag' : -1,'isDirty':False,'address':0}]*self.assoc for _ in range(self.noOfSets)]
        self.tagCache = [[{'tag' : -1}]*self.assoc for _ in range(self.noOfSets)]
    
    def attachInnerCache(self,innerCache):
        self.innerCache = innerCache

    def attachOuterCache(self,outerCache):
        self.outerCache = outerCache

    def getTagAndIndex(self,address):
        binary = bin(int(address, 16))[2:].zfill(32)
        tagBits , indexBits  = binary[:self.noOfTagBits], binary[self.noOfTagBits:self.noOfTagBits+self.noOfIndexBits]
        if indexBits == '':
            indexBits = '0'
        return tagBits , indexBits
    
    def inValidate(self,address):
        tag,index = self.getTagAndIndex(address)
        for block in self.cache[int(index,2)]:
            if tag == block['tag']:
                block['tag'] = -1
                if block['isDirty']:
                    self.writeBackCount += 1
                    self.writeBackToMemCount +=1
                block['isDirty'] = False
                break
        for tagBlock in self.tagCache[int(index,2)]:
            if tag == tagBlock['tag']:
                tagBlock['tag'] = -1
                tagBlock['isDirty'] = False
                break

    def handleMiss(self,address,tag,index):
        victimBlock = self.replacementPolicy.allocate(address,tag, self.cache[int(index,2)],self.tagCache[int(index,2)])
        if(victimBlock['tag'] != -1):
            victimAddress = victimBlock['address']
            if victimBlock['isDirty']:
                self.writeBackCount += 1
                self.outerCache.write(victimAddress)
            if self.inclusionPolicy == '1':
                try:
                    self.innerCache.inValidate(victimAddress)
                except:
                    pass
        try:
            self.outerCache.read(address)
        except:
            pass
        
    def read(self,address):
        if not self.size:
            return
        
        self.readCount += 1
        tag,index = self.getTagAndIndex(address)
        isMiss = True
        
        for block in self.cache[int(index,2)]:    
            if tag == block['tag']:
                self.replacementPolicy.update(block,self.tagCache[int(index,2)])
                isMiss = False
                break
        
        if isMiss:
            self.readMissCount += 1
            self.handleMiss(address,tag,index)
            

    def write(self,address):
        if not self.size:
            return
        
        self.writeCount += 1
        tag,index = self.getTagAndIndex(address)
        isMiss = True

        for block in self.cache[int(index,2)]:
            if tag == block['tag']:
                block['isDirty'] = True
                self.replacementPolicy.update(block,self.tagCache[int(index,2)])
                isMiss = False
                break
        
        if isMiss:
            self.writeMissCount += 1
            self.handleMiss(address,tag,index)
            for block in self.cache[int(index,2)]:
                if tag == block['tag']:
                    block['isDirty'] = True


           

blockSize = int(sys.argv[1])
l1Size = int(sys.argv[2])
l1Assoc = int(sys.argv[3])
l2Size = int(sys.argv[4])
l2Assoc = int(sys.argv[5])
replacementPolicy = sys.argv[6]
inclusionPolicy = sys.argv[7]
traceFile = sys.argv[8]


processor = Cache(0,0,0,0,0)
memory = Cache(0,0,0,0,0,)
L1 = Cache(blockSize,l1Size,l1Assoc,LRU() if replacementPolicy == '0' else FIFO(),inclusionPolicy)
L2 = Cache(blockSize,l2Size,l2Assoc,LRU() if replacementPolicy == '0' else FIFO(),inclusionPolicy)
L1.attachInnerCache(processor)
L1.attachOuterCache(L2)
L2.attachInnerCache(L1)
L2.attachOuterCache(memory)

f = open(traceFile, "r")
for instruction in f:
    if instruction[0]=='r':
        L1.read(instruction[2:])
    else:
        L1.write(instruction[2:])
f.close()


print("===== Simulator configuration =====")
print('''BLOCKSIZE:             {}
L1_SIZE:               {}
L1_ASSOC:              {}
L2_SIZE:               {}
L2_ASSOC:              {}
REPLACEMENT POLICY:    {}
INCLUSION PROPERTY:    {}
trace_file:            {}'''.format(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5],"LRU" if sys.argv[6]=='0' else "FIFO","non-inclusive" if sys.argv[7]=='0' else "inclusive",sys.argv[8]))
print('===== L1 contents =====')
for index,set in enumerate(L1.cache):
    o=''
    for block in set:
        o += '{} {}'.format(hex(int(block['tag'],2))[2:],'D  ' if block['isDirty'] else '   ')
    print("Set\t{}:\t".format(index)+o)
if L2.size:
    print('===== L2 contents =====')
    for index,set in enumerate(L2.cache):
        o=''
        for block in set:
            o += '{} {}'.format(hex(int(block['tag'],2))[2:],'D   ' if block['isDirty'] else '    ')
        print("Set\t{}:\t".format(index)+o)

a = L1.readCount
b = L1.readMissCount
c = L1.writeCount
d = L1.writeMissCount
e = (L1.readMissCount+L1.writeMissCount)/(L1.readCount+L1.writeCount)
f = L1.writeBackCount
g = L2.readCount
h = L2.readMissCount
i = L2.writeCount
j = L2.writeMissCount
try:
    k = h/g
except:
    k = 0
l = L2.writeBackCount
if L2.size:
    m = h + j + l + L1.writeBackToMemCount
else:
    m = b + d + f
print('''===== Simulation results (raw) =====
a. number of L1 reads:        {}
b. number of L1 read misses:  {}
c. number of L1 writes:       {}
d. number of L1 write misses: {}
e. L1 miss rate:              {:6f}
f. number of L1 writebacks:   {}
g. number of L2 reads:        {}
h. number of L2 read misses:  {}
i. number of L2 writes:       {}
j. number of L2 write misses: {}
k. L2 miss rate:              {:6f}
l. number of L2 writebacks:   {}
m. total memory traffic:      {}'''.format(a,b,c,d,e,f,g,h,i,j,k,l,m))


    


     
