import json
import sys
from modelcfg import *

def trans_func(alys_name, def_set, use_set, kill_set, in_out_set):
  if alys_name == 'live':
    return use_set | (in_out_set - kill_set)

def df_livar(prog):
  ''' Live variable analysis'''
  
  for func in prog['functions']:
    name2block = block_map(form_blocks(func['instrs']))
    get_succ_out = get_succ(name2block)
    get_pred_out = get_pred(get_succ_out)

    # print(get_pred_out)
    # print(get_succ_out)

    # init
    worklist = [ _ for _ in get_succ_out]
    in_set = {key: set() for key in worklist}
    out_set = {key: set() for key in worklist}
    define_set = {}# maps a basic block to those vars defined by it
    use_set = {}   # maps a basic block to those vars used by it 
    # avail_set = {} # maps a variable to its most recent definitions
    kill_set = {}  # maps a basic block to those vars killed by it

    for name, block in name2block.items():
      define_set[name] = set()
      use_set[name] = set()
      kill_set[name] = set()
      for instr in block:
        if 'args' in instr:
          if instr['args'][0] not in define_set[name]:
            use_set[name].add(instr['args'][0])
          if len(instr['args']) > 1 and \
            instr['args'][1] not in define_set[name]:
            use_set[name].add(instr['args'][1])
        if 'dest' in instr:
          define_set[name].add(instr['dest'])
          kill_set[name].add(instr['dest'])
          # for key, value in avail_set.items():
          #   if instr['dest'] == key:
          #     kill_set[name].add(key)
            # if any args in avail_set has been redefined,
            # the dest is considered to be killed
            # if instr['dest'] in value:
            #   kill_set[name].add(key)
          # if 'args' in instr:
          #   avail_set[instr['dest']] = instr['args']
          # else:
          #   avail_set[instr['dest']] = []
        
            
      # print(name, ', define_set->', define_set)
      # print(name, ', use_set->', use_set)
      # print(name, ', avail_set->', avail_set)
      # print(name, ', kill_set->', kill_set)

    while worklist:
      block = worklist.pop() # compute the last block first
      succ = get_succ_out[block]
      pred = get_pred_out[block]
      list_in_set = [in_set[keys] for keys in succ]
      out_set[block] = set().union(*list_in_set)
      new_in_set = trans_func('live', define_set[block], use_set[block], \
        kill_set[block], out_set[block])
      if new_in_set != in_set[block]:
        in_set[block] = new_in_set
        worklist = list(set().union(worklist, pred))
      # print('in_set->',in_set)
      # print('out_set->',out_set)
      # print('worklist->', worklist)

    for key, value in in_set.items():
      print(key,':')
      print('  in:', value)
      print('  out:', out_set[key])
      

if __name__ == '__main__':
  prog = json.load(sys.stdin)
  df_livar(prog)
