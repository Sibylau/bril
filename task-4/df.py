import json
import sys
from modelcfg import *

def trans_func(alys_name, block, def_set, use_set, kill_set, avail_set, \
  in_out_set):
  ''' Transfer Function
  To support more data flow analysis, add more transfer functions here
  '''
  if alys_name == 'live':
    return use_set | (in_out_set - def_set)
  elif alys_name == 'aval_expr':
    for instr in block:
      if 'dest' in instr:
        for arg in in_out_set:
          if arg in avail_set and instr['dest'] in avail_set[arg]:
            kill_set.add(arg)
        if 'args' in instr:
          avail_set[instr['dest']] = instr['args']
    return (in_out_set - kill_set) | def_set

def merge_func(mode, list_in_out_set):
  ''' Merge Function
  '''
  if mode == 'join':
    return set().union(*list_in_out_set)
  elif mode == 'meet':
    if list_in_out_set:
      s1 = list_in_out_set[0]
      return s1.intersection(*list_in_out_set)
    else:
      return set()

def backward(alys_name, merge_mode, name2block, worklist, get_pred_out, \
  get_succ_out, def_set, use_set, kill_set, avail_set, in_set, out_set):
  ''' Direction - backward
  '''
  while worklist:
    block = worklist.pop() # pick the last block first
    succ = get_succ_out[block]
    pred = get_pred_out[block]
    list_in_set = [in_set[keys] for keys in succ]
    out_set[block] = merge_func(merge_mode, list_in_set)
    new_in_set = trans_func(alys_name, name2block[block], def_set[block], \
      use_set[block], kill_set[block], avail_set, out_set[block])
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

def forward(alys_name, merge_mode, name2block, worklist, get_pred_out, \
  get_succ_out, def_set, use_set, kill_set, avail_set, in_set, out_set):
  ''' Direction - forward
  '''
  while worklist:
    block = worklist.pop() # pick the last block first
    succ = get_succ_out[block]
    pred = get_pred_out[block]
    list_out_set = [out_set[keys] for keys in pred]
    # print(list_out_set)
    in_set[block] = merge_func(merge_mode, list_out_set)
    new_out_set = trans_func(alys_name, name2block[block], def_set[block], \
      use_set[block], kill_set[block], avail_set, in_set[block])
    if new_out_set != out_set[block]:
      out_set[block] = new_out_set
      worklist = list(set().union(worklist, succ))
    # print('in_set->',in_set)
    # print('out_set->',out_set)
    # print('worklist->', worklist)

  for key, value in in_set.items():
    print(key,':')
    print('  in:', value)
    print('  out:', out_set[key])

# def init(alys_name, worklist):
#   if alys_name == 'live':
#     in_set = {key: set() for key in worklist}
#     out_set = {key: set() for key in worklist}
#   elif alys_name == 'aval_expr':
#     in_set = {key: {} for key in worklist}
#     out_set = {key: {} for key in worklist}
#   return in_set, out_set

def df(prog, alys_name, direction, merge_mode):
  
  for func in prog['functions']:
    name2block = block_map(form_blocks(func['instrs']))
    get_succ_out = get_succ(name2block)
    get_pred_out = get_pred(get_succ_out)

    # init facts to be empty sets - applies to limited dataflow analysis
    worklist = [ _ for _ in get_succ_out]
    in_set = {key: set() for key in worklist}
    out_set = {key: set() for key in worklist}

    # compute local affects of instructions
    define_set = {}# maps a basic block to vars defined by it
    use_set = {}   # maps a basic block to vars used before written to 
    kill_set = {key: set() for key in worklist}
    avail_set = {}

    for name, block in name2block.items():
      define_set[name] = set()
      use_set[name] = set()
      for instr in block:
        if 'args' in instr:
          if instr['args'][0] not in define_set[name]:
            use_set[name].add(instr['args'][0])
          if len(instr['args']) > 1 and \
            instr['args'][1] not in define_set[name]:
            use_set[name].add(instr['args'][1])
        if 'dest' in instr:
          define_set[name].add(instr['dest'])
        
    if direction == 'backward':
      backward(alys_name, merge_mode, name2block, worklist, get_pred_out, \
        get_succ_out, define_set, use_set, kill_set, avail_set, in_set, out_set)
    elif direction == 'forward':
      forward(alys_name, merge_mode, name2block, worklist, get_pred_out, \
        get_succ_out, define_set, use_set, kill_set, avail_set, in_set, out_set)
    else:
      print('Input Error: Unknown Direction')
      
if __name__ == '__main__':
  prog = json.load(sys.stdin)
  if len(sys.argv) > 1:
    if sys.argv[1] == 'live':
      df(prog, 'live', 'backward', 'join')
    elif sys.argv[1] == 'aval_expr':
      df(prog, 'aval_expr', 'forward', 'meet')
    else:
      print('Input Error:', sys.argv[1], 'is not implemented')
  else: 
    # set default to be live variable analysis
    df(prog, 'live', 'backward', 'join')

