# Local Value Numbering

This folder contains python implementation for local value numbering.

- `simple_dse.py` performs simple dead code elimination like reassignments. 
- `lvn.py` does local value numbering which removes dead code in copy propagation and common subexpression elimination cases. It supports commutativity in instruction operands.
- `lvn-const-prop.py` will propagate constants to a chain of assignments
- `lvn-const-fold.py` will compute at compile time the results of instructions as long as operands are known as constants.
