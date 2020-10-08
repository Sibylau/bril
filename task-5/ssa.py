import json
import sys
from dominance import *

def to_ssa(prog):
  for func in prog['functions']:
    name2block = block_map(form_blocks(func['instrs']))
    get_succ_out = get_succ(name2block)
    get_pred_out = get_pred(get_succ_out)
    vertices = [name for name in name2block.keys()]

    # initialize dom to be the whole set, otherwise cannot cover 
    # certain vertices
    dom = {name:set(vertices) for name in vertices}
    defs = {}
    var_type = {}
    change = True
    while change:
      change = False
      for name, block in name2block.items():
        dom_set = [dom[pred] for pred in get_pred_out[name]]
        update_set = set()
        if dom_set:
          update_set = dom_set[0].intersection(*dom_set)
        update_set = update_set.union({name})
        if update_set != dom[name]:
          dom[name] = update_set
          change = True
        for instr in block:
          if 'dest' in instr:
            if instr['dest'] not in defs:
              defs[instr['dest']] = set({name})
            else:
              defs[instr['dest']].add(name)
            var_type[instr['dest']] = instr['type']

    dom_front = dom_frontier(dom, get_pred_out)
    print("dom_front: ", dom_front)
    print("v_defs: ", defs)

    for var, block_name in defs.items():
      for b in block_name:
        for df_b in dom_front[b]:
          if (name2block[df_b])[0]['op'] != 'phi' or \
            (name2block[df_b])[0]['dest'] != var:
            phi_instr = {"args": [var], "dest": var, \
              "labels": [b], "op": "phi", "type": var_type[var]}
            name2block[df_b].insert(0, phi_instr)
          else:
            (name2block[df_b])[0]['args'].append(var)
            (name2block[df_b])[0]['labels'].append(b)
          block_name.add(df_b)
          print(name2block[df_b])

  return prog

    


# def out_of_ssa(prog):
#   return 

if __name__ == "__main__":
  prog = json.load(sys.stdin)
  new_prog = to_ssa(prog)
