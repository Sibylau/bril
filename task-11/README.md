# Tracing JIT for Bril
I modified `../../bril-ts/brili.ts` to dump out the execution trace. Here two operations require some twist: 1) eliminate jump since the tracing is totally linear 
2) replace branches with the `guard` operations. A special case is when the conditional statement branches to the `false` direction. Then the conditional variable cannot be used
as the argument in `guard` operation directly. To walk around, I inserted an additional variable assigned to be True before the `guard` instruction.

The optimization in `opt.py` is a very simple dead code elimination, which will eliminate unused assignments. `stitch.py` glued the optimized tracing sequence to the source code 
by adding `speculate` and `commit`.

### Test
Under `task-11/test/` folder:
 - `bril2json < br.bril | ../../bril-ts/build/brili.js | tee br.trace` dumps tracing into `br.trace` file
 - `bril2json < br.bril | python ../stitch.py br.trace | ../../bril-ts/build/brili.js` runs a simple dead code elimination and passes the output to the interpreter.
 
Here's the output before tracing JIT optimization. Note that I inserted a `b_not` variable before the `guard` instruction:
<img src="https://github.com/Sibylau/bril/blob/scratch/task-11/snapshots/1.PNG" width="800">

And here's the output after optimization:
<img src="https://github.com/Sibylau/bril/blob/scratch/task-11/snapshots/2.PNG" width="850">
