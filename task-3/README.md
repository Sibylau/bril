# Local Value Numbering

This folder contains python implementation for local value numbering.

#### `simple_dse.py` 
This codefile performs simple dead code elimination like reassignments. 
#### `lvn.py` 
The base version does local value numbering which removes dead code in copy propagation and common subexpression elimination cases. It supports commutativity in instruction operands.  
For common subexpression elimination:  
<img src="https://github.com/Sibylau/bril/blob/scratch/task-3/snapshots/lvn_subex.PNG" width="600">

The awareness of commutativity in operands:  
<img src="https://github.com/Sibylau/bril/blob/scratch/task-3/snapshots/lvn_commut.PNG" width="600">

However it can't do const propagation:  
<img src="https://github.com/Sibylau/bril/blob/scratch/task-3/snapshots/lvn.PNG" width="600">

#### `lvn-const-prop.py` 
This implementation will propagate constants to a chain of assignments:  
<img src="https://github.com/Sibylau/bril/blob/scratch/task-3/snapshots/lvn_const_prop.PNG" width="600"> 
#### `lvn-const-fold.py` 
This version will compute at compile time the results of instructions as long as operands are known as constants:  
<img src="https://github.com/Sibylau/bril/blob/scratch/task-3/snapshots/lvn_const_fold.PNG" width="600"> 
