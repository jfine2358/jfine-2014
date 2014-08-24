'''When run, self-test the testtools module.'''

import ast
import os

try:
    import astkit as tmp
    ast_render = tmp.render.SourceCodeRenderer.render
    del tmp
except ImportError:
    ast_render = ast.dump

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
        value = getattr(line, 'value', None)
        if value is None:
            continue

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


def edit_body_exprs(fn, tree):
    '''Use fn to edit expressions used as statements.
    '''

    # TODO: I don't like this use of subclassing.
    class Transformer(ast.NodeTransformer):

        def generic_visit(self, node):

            body = getattr(node, 'body', None)
            if body is None:
                super(Transformer, self).generic_visit(node)
                return node
            else:
                node.body = [
                    fn(line)
                    if type(line) is ast.Expr
                    else self.generic_visit(line)
                    for line in body
                    ]
                return node

    # We're editing the tree, not visiting it.
    return Transformer().visit(tree)


def subst(expr):
    '''Simply replace by a dummy expression.'''

    print(ast_render(expr))

    return  ast.parse('an_expression_was_here')


edit_body_exprs(subst, tree)


if ast_render:
    print(ast_render(tree))
