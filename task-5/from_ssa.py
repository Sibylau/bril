import json
import sys
from dominance import *
from modelcfg import *
from simple_dse import elm_var

TERMINATORS = 'jmp', 'br', 'ret'

def list2block(func, name2block):
  func['instrs'] = []
  for name, block in name2block.items():
    label = {'label': name}
    func['instrs'].append(label)
    func['instrs'].extend(block)


def from_ssa(prog):
  for func in prog['functions']:
    name2block = block_map(form_blocks(func['instrs']))
    get_succ_out = get_succ(name2block)
    get_pred_out = get_pred(get_succ_out)
    vertices = [name for name in name2block.keys()]
    for name, block in name2block.items():
      for instr in block:
        if instr['op'] == 'phi':
          for pred in get_pred_out[name]:
            last_instr = name2block[pred][-1]
            dest_var = instr['dest']
            type_var = instr['type']
            args = instr['args'][instr['labels'].index(pred)]
            new_instr = {"args": [args], "dest": dest_var, "op": "id",\
               "type": type_var}
            if last_instr['op'] in TERMINATORS:
              name2block[pred].insert(-1, new_instr)
            else:
              name2block[pred].append(new_instr)
          block.remove(instr)
    # print(name2block)
    list2block(func, name2block)


if __name__ == "__main__":
  prog = json.load(sys.stdin)
  from_ssa(prog)
  print(json.dumps(prog))
