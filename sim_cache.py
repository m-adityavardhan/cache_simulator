import sys
from cache import Cache
from lru import LRU
from fifo import FIFO
from display import displayOutput           

if __name__=='__main__':
    # Reading command line arguments
    blockSize = int(sys.argv[1])
    l1Size = int(sys.argv[2])
    l1Assoc = int(sys.argv[3])
    l2Size = int(sys.argv[4])
    l2Assoc = int(sys.argv[5])
    replacementPolicy = sys.argv[6]
    inclusionPolicy = sys.argv[7]
    traceFile = sys.argv[8]


    # Instantiating L1 and L2 Cache along with dummy caches for processor and memory
    processor = Cache(0,0,0,0,0)
    memory = Cache(0,0,0,0,0,)
    L1 = Cache(blockSize,l1Size,l1Assoc,LRU() if replacementPolicy == '0' else FIFO(),inclusionPolicy)
    L2 = Cache(blockSize,l2Size,l2Assoc,LRU() if replacementPolicy == '0' else FIFO(),inclusionPolicy)
    # Attaching processor to L1
    L1.attachInnerCache(processor)
    # Attaching L2 to L1
    L1.attachOuterCache(L2)
    # Attaching L1 to L2
    L2.attachInnerCache(L1)
    # Attaching meomry to L2
    L2.attachOuterCache(memory)

    f = open(traceFile, "r")
    # Read each instruction from trace file
    for instruction in f:
        if instruction[0]=='r':
            L1.read(instruction[2:])
        else:
            L1.write(instruction[2:])
    f.close()

    # Displaying the output as required
    displayOutput(L1,L2,blockSize,l1Size,l1Assoc,l2Size,l2Assoc,replacementPolicy,inclusionPolicy,traceFile)


    


     
