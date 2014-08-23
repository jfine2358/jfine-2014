'''When run, self-test the testtools module.'''

import ast
import os

dirname = os.path.dirname(__file__)

filename = os.path.join(dirname, 'test_add.py')
with open(filename) as f:
    tree = ast.parse(f.read())


if 0:
    print(ast.dump(tree))

    for line in tree.body:
        print(ast.dump(line))
