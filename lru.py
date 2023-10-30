from replacement_policy_interface import ReplacementPolicy
       
class LRU(ReplacementPolicy):
    def update(self,block,tagSet):
        movedBlock = 0
        for tagBlock in tagSet:
            if tagBlock['tag'] == block['tag']:
                movedBlock = tagBlock
                break
        tagSet.remove(movedBlock)
        tagSet.append(movedBlock)

