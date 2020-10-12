# Global Analysis and SSA

Finished dominance utilies in `dominance.py`.  

Pass sys.stdin parameter:
 - `dom`: print dominators for each basic block.
 - `dom_tree`: print a mapping from each node to its children nores in the dominator tree
 - `dom_frontier`: print domination frontier for each basic block.

Finished conversion to SSA (`to_ssa.py`) and from SSA (`from_ssa.py`). They passed the given tests:

<img src="https://github.com/Sibylau/bril/blob/scratch/task-5/snapshots/to_ssa_test.PNG" width="600"> 

This is what the converted SSA looks like for loop-orig.bril:  
<img src="https://github.com/Sibylau/bril/blob/scratch/task-5/snapshots/loop_orig.PNG" width="600"> 
 
