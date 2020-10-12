import json
import sys
from dominance import *
from modelcfg import *
from simple_dse import elm_var

def list2block(func, name2block):
  func['instrs'] = []
  for name, block in name2block.items():
    label = {'label': name}
    func['instrs'].append(label)
    func['instrs'].extend(block)

def rename_block(entry, name2block, get_succ_out, dom_t): 
  # v_counter is an increasing counter for variable names
  # stack saves new variable names
  v_counter = {} 
  stack = {}
  for block in name2block.values():
    for instr in block:
      if 'dest' in instr:
        stack[instr['dest']] = []
        v_counter[instr['dest']] = 0

  def _rename(block):
    # preserve an old copy of stack, a deep copy
    stack_v_old = {}
    for k, v in stack.items():
      stack_v_old[k] = []
      stack_v_old[k].extend(v)

    # update the args and give new names to dests
    for instr in name2block[block]:
      if 'args' in instr and instr['op'] != 'phi':
        for i in range(len(instr['args'])):
          old_arg = instr['args'][i]
          if old_arg in stack and stack[old_arg]:
            new_arg = stack[old_arg][-1]
            instr['args'][i] = new_arg
      if 'dest' in instr:
        old_name = instr['dest']
        new_name = old_name + '.' + str(v_counter[old_name])
        v_counter[old_name] = v_counter[old_name] + 1
        instr['dest'] = new_name
        stack[old_name].append(new_name)

    for suc in get_succ_out[block]:
      for instr in name2block[suc]:
        if instr['op'] == 'phi':
          for arg in instr['args']:
            if arg in stack.keys() and stack[arg]:
              index = instr['args'].index(arg)
              instr['args'][index] = stack[arg][-1]
              instr['labels'][index] = block
              break

    for b in dom_t[block]:
      _rename(b)
    
    stack.update(stack_v_old)
  
  _rename(entry)


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
              defs[instr['dest']] = [name]
            elif name not in defs[instr['dest']]:
              defs[instr['dest']].append(name)
            var_type[instr['dest']] = instr['type']

    dom_t = dom_tree(dom)
    dom_front = dom_frontier(dom, get_pred_out)
    entry = (set(vertices) - set().union(*dom_t.values())).pop()

    # Step 1: insert phi nodes
    for var, block_name in defs.items():
      for b in block_name:
        for df_b in dom_front[b]:
          if (name2block[df_b])[0]['op'] != 'phi' or \
            (name2block[df_b])[0]['dest'] != var:
            phi_instr = {"args": [], "dest": var, \
              "labels": [], "op": "phi", "type": var_type[var]}
            name2block[df_b].insert(0, phi_instr)
            for pred in get_pred_out[df_b]:
              (name2block[df_b])[0]['args'].append(var)
              (name2block[df_b])[0]['labels'].append(pred)

          if df_b not in block_name:
            block_name.append(df_b)

    # Step 2: rename variables
    rename_block(entry, name2block, get_succ_out, dom_t)   

    list2block(func, name2block) 

if __name__ == "__main__":
  prog = json.load(sys.stdin)
  to_ssa(prog)
  new_prog = elm_var(prog)
  print(json.dumps(new_prog))
