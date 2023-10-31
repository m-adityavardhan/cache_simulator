import matplotlib.pyplot as plt
from cache import Cache
from lru import LRU
from fifo import FIFO
from display import displayOutput           

l1Size = 1024
l1Assoc = 4
blockSize = 32
l2Assoc = 8

missRates=[]
missRates2=[]
for inclusionPolicy in ['0','1']:
    missRates.append([])
    missRates2.append([])
    for power in range(11,17):
        # Instantiating L1 and L2 Cache along with dummy caches for processor and memory
        processor = Cache(0,0,0,0,0)
        memory = Cache(0,0,0,0,0,)
        L1 = Cache(blockSize,1024,l1Assoc,LRU(),inclusionPolicy)
        L2 = Cache(blockSize,pow(2,power),l2Assoc,LRU(),inclusionPolicy)
        # Attaching processor to L1
        L1.attachInnerCache(processor)
        # Attaching L2 to L1
        L1.attachOuterCache(L2)
        # Attaching L1 to L2
        L2.attachInnerCache(L1)
        # Attaching meomry to L2
        L2.attachOuterCache(memory)

        f = open('tests\\traces\\gcc_trace.txt', "r")
        # Read each instruction from trace file
        for instruction in f:
            if instruction[0]=='r':
                L1.read(instruction[2:])
            else:
                L1.write(instruction[2:])
        f.close()
        a = L1.getReadCount()
        b = L1.getReadMissCount()
        c = L1.getWriteCount()
        d = L1.getWriteMissCount()
        e = (b+d)/(a+c)
        g = L2.getReadCount()
        h = L2.getReadMissCount()
        k = h/g
        missRates[-1].append(e)
        missRates2[-1].append(k)

print(missRates)
print(missRates2)

httIp = 0.14682
httIP2 = [0.180686,0.189065,0.212911,0.254354,0.288511,0.341213]

AATip=[]
for i in range(2):
  r=[]
  for j in range(6):
    r.append(httIp+ missRates[i][j]*(httIP2[j]+missRates2[i][j]*100))
  AATip.append(r)
AATip

IP = ['Non-Inclusive','Inclusive']

x = range(11,17)
for index,res in enumerate(AATip):
  plt.plot(x, res, label=f"{IP[index]}")

plt.legend()
plt.xlabel("log2(Size)")
plt.ylabel("AAT")
plt.show()