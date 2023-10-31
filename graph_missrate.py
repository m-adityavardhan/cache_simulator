import matplotlib.pyplot as plt
from cache import Cache
from lru import LRU
from fifo import FIFO
from display import displayOutput           

l2Size,l2Assoc = 0 ,0
blockSize = 32

missRates=[]
for power in range(10,21):
    missRates.append([])
    for l1Assoc in [1,2,4,8,pow(2,power)//32]:
        # Instantiating L1 and L2 Cache along with dummy caches for processor and memory
        processor = Cache(0,0,0,0,0)
        memory = Cache(0,0,0,0,0,)
        L1 = Cache(blockSize,pow(2,power),l1Assoc,LRU(),'0')
        L2 = Cache(blockSize,l2Size,l2Assoc,LRU(),'0')
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
        missRates[-1].append(e)

mr = []
for j in range(5):
  mr.append([])
  for i in range(11):
    mr[-1].append(missRates[i][j])

print("Compulsory Miss Rate(1MB - Fully Associativity) is ",mr[-1][-1])
assoc = [1, 2, 4, 8,'fully']
x = range(10,21)
for index,res in enumerate(mr):
  plt.plot(x, res, label=f"{assoc[index]} Associativity")
plt.legend()
plt.xlabel("log2(Size)")
plt.ylabel("Miss Rate")
plt.show()

ht= [[0.114797, 0.140329, 0.14682, 0.15082, 0.155484],
 [0.12909, 0.161691, 0.154496, 0.180686, 0.176515],
 [0.147005, 0.181131, 0.185685, 0.189065, 0.182948],
 [0.16383, 0.194195, 0.211173, 0.212911, 0.198581],
 [0.198417, 0.223917, 0.233936, 0.254354, 0.205608],
 [0.233353, 0.262446, 0.27125, 0.288511, 0.22474],
 [0.294627, 0.300727, 0.319481, 0.341213, 0.276281],
 [0.3668, 0.374603, 0.38028, 0.401236, 0.322486],
 [0.443812, 0.445929, 0.457685, 0.458925, 0.396009],
 [0.563451, 0.567744, 0.564418, 0.578177, 0.475728],
 [0.69938, 0.706046, 0.699607, 0.705819, 0.588474]]

htt = []
for j in range(5):
  htt.append([])
  for i in range(11):
    htt[-1].append(ht[i][j])
htt

AAT=[]
for i in range(5):
  r=[]
  for j in range(11):
    r.append(htt[i][j]+missr[i][j]*100)
  AAT.append(r)
AAT

assoc = [1, 2, 4, 8,'fully']

x = range(10,21)
for index,res in enumerate(AAT):
  plt.plot(x, res, label=f"{assoc[index]} Associativity")

plt.legend()
plt.xlabel("log2(Size)")
plt.ylabel("AAT")
plt.show()

