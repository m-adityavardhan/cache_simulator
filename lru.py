from replacement_policy import ReplacementPolicy
       
class LRU(ReplacementPolicy):
    # For each HIT in cache update the tag store appropriately w.r.t replacement policy
    def update(self,block,tagSet):
        # Getting the HIT block in tagStore
        movedBlock = 0
        for tagBlock in tagSet:
            if tagBlock['tag'] == block['tag']:
                movedBlock = tagBlock
                break
        # Moving the Hit block to end of the list so that LRU block will always be in first place
        tagSet.remove(movedBlock)
        tagSet.append(movedBlock)

