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

def mycfg(prog):
  for func in prog['functions']:
    blocks = []
    for block in form_blocks(func['instrs']):
      blocks.append(block)
    for block in blocks:
      last = block[-1]
      if last['op'] == 'jmp':
        block['suc'] = last['labels']
      elif last['op'] == 'br':
        block['suc1'] = last['labels'][0]
        block['suc2'] = last['labels'][1]
      elif last['op'] == 'ret':
        block['suc'] = last['labels']
      else:
        block['suc'] = block+1
    # for block in blocks:
    #   print(block)
  return blocks

if __name__ == '__main__':
  prog = json.load(sys.stdin)
  blocks = mycfg(prog)

