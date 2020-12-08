import json
import sys
from modelcfg import *

def simple_dse(lines):
  print(lines)
  change = True
  while change:
    change = False
    used = []
    for instr in lines:
      dict_instr = json.loads(instr)
      if isinstance(dict_instr, dict) and 'args' in dict_instr:
        # print(instr)
        used.extend(dict_instr['args'])
    print(used)
    for instr in lines:
      dict_instr = json.loads(instr)
      if isinstance(dict_instr, dict) and \
        'dest' in dict_instr and dict_instr['dest'] not in used:
        lines.remove(instr)
        change = True
  return lines

if __name__ == "__main__":
  file_name = sys.argv[1]
  trace_file = open(file_name, 'r')
  lines = trace_file.read().splitlines()
  instrs = simple_dse(lines)
  print(instrs)
  trace_file.close()
