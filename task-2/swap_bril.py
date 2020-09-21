import json
import sys

# swap the order of arguments for every instructions 
# taking 2 arguments as inputs
def swap_bril():
  prog = json.load(sys.stdin)
  for func in prog['functions']:
    for instr in func['instrs']:
      if 'args' in instr and len(instr['args']) == 2:
        instr['args'][0], instr['args'][1] = \
        instr['args'][1], instr['args'][0]
        
    dest_instr = [val for idx, val in enumerate(func['instrs']) if 'dest' in val]
    # dest_val = [inst['dest'] for inst in dest_instr]
    insert_pt = [idx for idx, val in enumerate(func['instrs']) if 'dest' in val]
    for i, idx in enumerate(insert_pt):
      new_instr = {'args': [dest_instr[i]['dest']], 'op': 'print'}
      func['instrs'].insert(idx + i + 1, new_instr)

  # write out to 'swap_out.json' file
  with open('swap_out.json', 'w') as json_file:
    json.dump(prog, json_file)
  with open('swap_out.json', 'r') as f:
    print(f.read())

if __name__ == '__main__':
  swap_bril()