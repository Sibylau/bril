import json
import sys

TERMINATORS = 'jmp', 'br', 'ret'

def form_blocks(body):
  cur_block = []

  for instr in body:
    if 'op' in instr: # An actual instruction
      cur_block.append(instr)

      # check for terminator
      if instr['op'] in TERMINATORS:
        yield cur_block
        cur_block = []
    else: # A label
      yield cur_block
      cur_block = [instr]
  yield cur_block

# global dead code elimination (intra-procedure)
# remove instructions that defines a var that's never been used
def elm_var(prog):
  for func in prog['functions']:
    change = True
    while change:
      change = False
      used = []
      for instr in func['instrs']:
        if 'args' in instr:
          used.extend(instr['args'])
      for instr in func['instrs']:
        if 'dest' in instr and instr['dest'] not in used:
          func['instrs'].remove(instr)
          change = True
      # print(func)
  # print(prog)
  return prog

# local dead code elimination
# eliminate re-assignments within single basic block
def elm_reassign(prog):
  for func in prog['functions']:
    change = True
    while change:
      change = False
      for block in form_blocks(func['instrs']):
        # func['instrs'].remove(block[0])
        # print(prog)
        last_def = {}
        for instr in block:
          # remove used args first
          if 'args' in instr:
            for arg in instr['args']:
              if arg in last_def:
                del last_def[arg]
          # remove reassignments
          if 'dest' in instr and instr['dest'] in last_def:
            func['instrs'].remove(last_def[instr['dest']])
            change = True
          # update last-def map
          if 'dest' in instr:
            last_def[instr['dest']] = instr
              
        # print(prog)
  return prog

def print_json(prog_update, filename):
  with open(filename, 'w') as json_file:
    json.dump(prog_update, json_file)
  with open(filename, 'r') as f:
    print(f.read())

if __name__ == '__main__':
  prog = json.load(sys.stdin)
  prog_out_0 = elm_var(prog)
  prog_out = elm_reassign(prog_out_0)
  print_json(prog_out, 'simple_dse_out')

