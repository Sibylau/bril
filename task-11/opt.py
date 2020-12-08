import json
import sys
from modelcfg import *

def simple_dse(lines):
  change = True
  while change:
    change = False
    used = []
    for instr in lines:
      if 'args' in instr:
        used.extend(instr['args'])
    for instr in lines:
      if 'dest' in instr and instr['dest'] not in used:
        lines.remove(instr)
        change = True
  return lines

if __name__ == "__main__":
  file_name = sys.argv[1]
  trace_file = open(file_name, 'r')
  lines = []
  while True:
    line = trace_file.readline()
    if len(line) == 0:
      break
    line = json.loads(line)
    if isinstance(line, dict):
      lines.append(line)
  instrs = simple_dse(lines)
  print(instrs)
  trace_file.close()
