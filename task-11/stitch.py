import json
import sys
from modelcfg import *
from opt import *

def stitch(instrs, source_file):
  

if __name__ == "__main__":
  trace_name = sys.argv[1]
  trace_file = open(trace_name, 'r')
  source_name = sys.argv[2]
  source_file = open(source_name, 'wr')
  prog = json.load(source_file)
  lines = trace_file.read().splitlines()
  instrs = simple_dse(lines)
  stitch(instrs, source_file)
  trace_file.close()
  source_file.close()