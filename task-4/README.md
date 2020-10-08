# Data Flow Analysis

This folder contains python implementation for data flow analysis.

`df_livar.py`  
This file only implements live variable analysis. 

`df.py`  
This code tries to abstract a generic framework for data flow analysis using worklist algorithm.
It currently contains live variable analysis and available expression analysis. 
It's supposed to be as brief as possible to extend support for other kinds of data flow analysis. 
To do so, the developer needs to come up with the new transfer functions, add it under the corresponding trans_func function, 
and specify directions <backward, forward> and merge functions <join, meet>. 

Live variable analysis and availale expression analysis functions are shown below:

<img src="https://github.com/Sibylau/bril/blob/scratch/task-4/snapshots/live.PNG" width="600"> 

<img src="https://github.com/Sibylau/bril/blob/scratch/task-4/snapshots/aval_expr.PNG" width="600"> 
