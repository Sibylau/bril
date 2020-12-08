import json
import sys
from modelcfg import *
from opt import *

def stitch(instrs, prog):
  for func in prog['functions']:
    if func['name'] == "main":
      instr = {"op": "commit"}
      instrs.append(instr)
      instr = {"op": "ret"}
      instrs.append(instr)
      instr = {"label": "failed"}
      instrs.append(instr)
      func['instrs'] = instrs + func['instrs']
      instr = {"op": "speculate"}
      func['instrs'].insert(0, instr)
        
  return prog

if __name__ == "__main__":
  trace_name = sys.argv[1]
  trace_file = open(trace_name, 'r')
  lines = []
  while True:
    line = trace_file.readline()
    if len(line) == 0:
      break
    line = json.loads(line)
    if isinstance(line, dict):
      lines.append(line)
  instrs = simple_dse(lines)

  prog = json.load(sys.stdin)
  stitch(instrs, prog)
  trace_file.close()
  print(json.dumps(prog))
