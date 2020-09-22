import sys
import json
import random
from simple_dse import *

table = [] # maps expressions to vars in a numbered way
var2num = {} # maps current variables to entries in table

def gen_random_num():
  yield random.sample(1000, 5)

def arithmetic_comp(operation, op1, op2):
  if operation == 'add':
    return op1 + op2
  if operation == 'mul':
    return op1 * op2
  if operation == 'sub':
    return op1 - op2
  if operation == 'div':
    return op1 / op2
  if operation == 'eq':
    return op1 == op2
  if operation == 'lt':
    return op1 < op2
  if operation == 'gt':
    return op1 > op2
  if operation == 'le':
    return op1 <= op2
  if operation == 'ge':
    return op1 >= op2
  if operation == 'and':
    return op1 and op2
  if operation == 'or':
    return op1 or op2

def lvn_const_prop(prog):
  # initialize updated prog
  prog_update = {}
  prog_update["functions"] = []

  for func in prog['functions']:
    func_name = func['name']
    build_instrs = {"instrs": [], "name": func_name}
    for block in form_blocks(func['instrs']):
      for instr in block:
        # build the value tuple
        if 'args' in instr:
          if len(instr['args']) > 1: # commutative
            value = (instr['op'], min(var2num[instr['args'][0]], var2num[instr['args'][1]]),\
                     max(var2num[instr['args'][0]], var2num[instr['args'][1]]))
          else:
            value = (instr['op'], var2num[instr['args'][0]])
        elif 'value' in instr:
          value = (instr['op'], instr['value'])

        # if the tuple is already in the table
        match = False
        for index, entry in enumerate(table):
          if 'dest' in instr and value in entry:
            var = entry[value]
            dest = instr['dest']
            val_type = instr['type']

            # insert new instruction 
            instr.clear()
            instr["args"] = [var]
            instr["dest"] = dest
            instr["op"] = "id"
            instr["type"] = val_type

            match = True
            num = index
            break

        # else the tuple is a new one
        if not match:
          if 'dest' in instr:
            new_can_var = instr['dest']
            # look backward to check repeated var names
            for index, entry in enumerate(table): 
              if instr['dest'] == list(entry.values())[0]:
                new_can_var = instr['dest'] + '.' + str(gen_random_num())
                instr['dest'] = new_can_var
                break

          # give id semantic and create a new term in the table
          if instr['op'] == 'id':
            num = var2num[instr['args'][0]]

            # const propagation
            value_tuple = list(table[num].keys())[0]
            op_type = value_tuple[0]
            const_value = value_tuple[1]
            dest = instr['dest']
            val_type = instr['type']
            if op_type == 'const':
              instr.clear()
              instr["dest"] = dest
              instr["op"] = op_type
              instr["type"] = val_type
              instr["value"] = const_value

          else:
            num = len(table)
            table.append({value: new_can_var})
            if 'args' in instr:
              comp_args = []
              for ite in range(len(instr['args'])):
                table_entry = table[var2num[instr['args'][ite]]]
                value_tuple = list(table_entry.keys())[0]
                can_var = list(table_entry.values())[0]
                instr['args'][ite] = can_var
                if value_tuple[0] == 'const':
                  comp_args.append(value_tuple[1])
                if len(comp_args) > 1:
                  const_value = arithmetic_comp(instr['op'], comp_args[0], comp_args[1])
                  dest = instr['dest']
                  val_type = instr['type']
                  instr.clear()
                  instr["dest"] = dest
                  instr["op"] = "const"
                  instr["type"] = val_type
                  instr["value"] = const_value
                  table[-1] = {("const", instr["value"]): new_can_var}
          # else:
          #   num = len(table)
          #   table.append({value: new_can_var})

          # # update instruction args
          # if 'args' in instr:
          #   comp_args = []
          #   for ite in range(len(instr['args'])):
          #     table_entry = table[var2num[instr['args'][ite]]]
          #     value_tuple = list(table_entry.keys())[0]
          #     can_var = list(table_entry.values())[0]
          #     instr['args'][ite] = can_var
          #     if value_tuple[0] == 'const':
          #       comp_args.append(value_tuple[1])
          #   # if len(comp_args) > 1:
          #   #   dest = instr['dest']
          #   #   val_type = instr['type']
          #   #   instr.clear()
          #   #   instr["dest"] = dest
          #   #   instr["op"] = "const"
          #   #   instr["type"] = val_type
          #   #   instr["value"] = arithmetic_comp(instr['op'], comp_args[0], comp_args[1])

        if 'dest' in instr:
          var2num[instr['dest']] = num

      build_instrs['instrs'].extend(block)
    prog_update['functions'].append(build_instrs)
  # print(prog)
  return prog_update

if __name__ == '__main__':
  prog = json.load(sys.stdin)
  lvn_out = lvn_const_prop(prog)
  prog_out_1 = elm_var(lvn_out)
  prog_out_2 = elm_reassign(prog_out_1)
  print_json(prog_out_2, 'lvn_const_prop_out.json')

