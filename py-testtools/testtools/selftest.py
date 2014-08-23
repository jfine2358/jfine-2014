'''When run, self-test the testtools module.'''

import ast
import os

dirname = os.path.dirname(__file__)

filename = os.path.join(dirname, 'test_add.py')
with open(filename) as f:
    tree = ast.parse(f.read())


if 0:
    print(ast.dump(tree))

if 1:
    for line in tree.body:
        # Each line has a name, which determines its type.
        name = type(line.value).__name__
        print(name)
