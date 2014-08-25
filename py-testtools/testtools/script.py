import ast
import os
import marshal

__metaclass__ = type

class Script:

    def __init__(self, source, filename='<unknown>'):

        # Parse source to tree, edit, compile and save resulting code.
        self.filename = filename
        tree = ast.parse(source, filename=self.filename)
        edit_body_exprs(edit_expr, tree)
        self.code = compile(tree, self.filename, 'exec')


# This function helps defined the tranformation we want.
def edit_expr(expr):
    '''Start making the changes I want.'''

    value = expr.value

    # Filter the comparisons for change.
    if type(value) is ast.Compare:
        return  log_compare(value)
    else:
        return expr             # Leave unchanged.


# This function helps defined the tranformation we want.
def log_compare(node):

    # TODO: I think this is done, but is it?
    # Replace compare node with log._compare.
    # Produce the ops.
    ops = node.ops
    ops_arg = [type(op).__name__ for op in ops]

    # Produce the values.
    values = [node.left] + node.comparators
    val_args = [
        marshal.dumps(compile(ast.Expression(v), '', 'eval'))
        for v in values
        ]

    # Done so return new node.
    format = '_evaluator_.compare(locals(), {0}, {1})'.format
    # TODO: Clean up this mess.
    # TODO: Check that body appears just where I expect.
    if 0:
        # TODO: Produces
        # Expression(body=Call(func=Attribute(value=Name(id='log'
        new_tree = ast.parse(format(ops_arg, val_args), mode='eval')
    else:
        # TODOD: Produces
        # Module(body=[Module(body=[Expr(value=Call( ...
        new_tree = ast.parse(format(ops_arg, val_args), mode='exec')

    # Strip off unwanted boilerplate.
    return new_tree.body[0]


# This utility function is based on ast module.
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


if __name__ == '__main__':


    # Here's how to create a script from a file.
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'test_add.py')
    with open(filename) as f:
        script = Script(f.read())

    # Here's a dummy log, for testing Script.
    class DummyEvaluator:

        def __init__(self):
            self.store = []

        def compare(self, *argv):
            self.store.append(argv[1:]) # Discard local_dict.

    # Here we create and test a script.
    s = Script('2 + 2 == 5')
    evaluator = DummyEvaluator()
    eval(s.code, dict(_evaluator_=evaluator))
    data = evaluator.store[0]
    assert data[0] == ['Eq']
    assert data[1] \
        == [marshal.dumps(compile(s, '', 'eval')) for s in ('2 + 2', '5')]
