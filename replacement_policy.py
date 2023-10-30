class ReplacementPolicy:
    def update(self,block,set):
        pass

    # When a miss occurs we need to evit a block to store the new block
    def allocate(self,address,tag,set,tagSet):
        isAllocated = False
        removedBlock = 0
        # Checking if any empty blocks are available to replace
        for tagBlock in tagSet:
            if tagBlock['tag'] == -1:
                removedBlock = tagBlock
                # If empty  is found in tag store remove it
                tagSet.remove(tagBlock)
                tagSet.append({'tag':tag})
                isAllocated = True
                break        
        # If no empty block is found replace a block using replacement policies  
        if (not isAllocated):
            # As the LRU block is always at first position and in FIFO we remove first position
            removedBlock = tagSet.pop(0)
            # Evict first block and add latest block to end
            tagSet.append({'tag':tag})
        # Update this change in cache 
        for index,setBlock in enumerate(set):
            if setBlock['tag'] == removedBlock['tag']: 
                # update the same evicted from cache as that of tag store with new data
                removedSetBlock = setBlock
                set.remove(setBlock)
                # We insert the new block at same location as old block as we need to maintain order
                set.insert(index,{'tag':tag,'isDirty':False,'address':address})
                return removedSetBlock