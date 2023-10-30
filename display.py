def _enumarateCache(cache):
    # Constructing output string my iterating each line in cache
    for index,set in enumerate(cache.getCache()):
        outputString=''
        # For each block in set 
        for block in set:
            outputString += '{} {}'.format(hex(int(block['tag'],2))[2:],'D  ' if block['isDirty'] else '   ')
        print("Set\t{}:\t".format(index)+outputString)


def displayOutput(cache1,cache2,blockSize,l1Size,l1Assoc,l2Size,l2Assoc,replacementPolicy,inclusionPolicy,traceFile):
    a = cache1.getReadCount()
    b = cache1.getReadMissCount()
    c = cache1.getWriteCount()
    d = cache1.getWriteMissCount()
    e = (b+d)/(a+c)
    f = cache1.getWriteBackCount()
    g = cache2.getReadCount()
    h = cache2.getReadMissCount()
    i = cache2.getWriteCount()
    j = cache2.getWriteMissCount()
    try:
        k = h/g
    except:
        k = 0
    l = cache2.getWriteBackCount()
    if cache2.getSize():
        m = h + j + l + cache1.getWriteBackToMemCount()
    else:
        m = b + d + f

    print("===== Simulator configuration =====")
    print('''BLOCKSIZE:             {}
    L1_SIZE:               {}
    L1_ASSOC:              {}
    L2_SIZE:               {}
    L2_ASSOC:              {}
    REPLACEMENT POLICY:    {}
    INCLUSION PROPERTY:    {}
    trace_file:            {}'''.format(blockSize,l1Size,l1Assoc,l2Size,l2Assoc,"LRU" if replacementPolicy=='0' else "FIFO","non-inclusive" if inclusionPolicy=='0' else "inclusive",traceFile))
    print('===== L1 contents =====')
    _enumarateCache(cache1)
    if cache2.getSize:
        print('===== L2 contents =====')
        _enumarateCache(cache2)
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