'''When run, self-test the testtools module.'''

import ast
import os

dirname = os.path.dirname(__file__)

filename = os.path.join(dirname, 'test_add.py')
with open(filename) as f:
    tree = ast.parse(f.read())


if 0:
    print(ast.dump(tree))


def add(x, y):
    return x + y


if 1:
    # Pick out and evaluate all suitable expressions.
    for line in tree.body:
        value = line.value

        if type(value) is ast.Compare:
            ops = value.ops
            # Make a test for this.
            if [op for op in ops if type(op) is not ast.Eq]:
                raise ValueError

            aaa = [value.left] + value.comparators

            bbb = [
                compile(ast.Expression(aa), '', 'eval')
                for aa in aaa
                ]

            print(tuple(
                    eval(bb, dict(add=add))
                    for bb in bbb
                    ))
