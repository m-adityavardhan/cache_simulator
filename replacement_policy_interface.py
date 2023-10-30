class ReplacementPolicy:
    def update(self,block,set):
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