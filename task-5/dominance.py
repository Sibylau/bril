import json
import sys
from modelcfg import *

def dominators(prog, mode):
  for func in prog['functions']:
    name2block = block_map(form_blocks(func['instrs']))
    get_succ_out = get_succ(name2block)
    get_pred_out = get_pred(get_succ_out)
    vertices = [name for name in name2block.keys()]

    # initialize dom to be the whole set, otherwise cannot cover 
    # certain vertices
    dom = {name:set(vertices) for name in vertices}
    change = True
    while change:
      change = False
      for name in name2block.keys():
        dom_set = [dom[pred] for pred in get_pred_out[name]]
        update_set = set()
        if dom_set:
          update_set = dom_set[0].intersection(*dom_set)
        update_set = update_set.union({name})
        if update_set != dom[name]:
          dom[name] = update_set
          change = True
    print(dom)
    if mode == 'dom':
      print(dom)
    elif mode == 'dom_tree':
      print(dom_tree(dom))
    elif mode == 'dom_frontier':
      print(dom_frontier(dom, get_pred_out))
  return dom

def dom_tree(dom):
  ''' Return a mapping from a node to its child in a 
  dominance tree
  '''
  # transform to a strict dominance mapping
  strict_dom = {}
  for node, dom_set in dom.items():
    strict_dom[node] = dom_set - {node}

  dom_tree = {name: set() for name in strict_dom.keys()}
  for node, dom_set in strict_dom.items():
    direct_dom = dom_set - {node}
    for name in dom_set:
      if name != node:
        direct_dom = direct_dom - strict_dom[name]
    for name in direct_dom:
      dom_tree[name].add(node)
  # print(dom_tree)
  return dom_tree

def dom_frontier(dom, get_pred_out):
  ''' Return a mapping from a node to its dominance frontier
  '''
  nodes = set(node for node in dom.keys())
  dom_front = {name: set() for name in nodes}

  for node, dom_set in dom.items():
    non_dom = nodes - dom_set
    for pred in get_pred_out[node]:
      front_dominators = non_dom.intersection(dom[pred])
      for front_dom in front_dominators:
        dom_front[front_dom].add(node)
  # print(dom_front)
  return dom_front


if __name__ == '__main__':
  prog = json.load(sys.stdin)
  if len(sys.argv) > 1:
    dominators(prog, sys.argv[1])
  else:
    dominators(prog, 'dom')
