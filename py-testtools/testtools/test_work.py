'''Test driver for rewriting code so far.'''

import ast
import os

from evaluator import Evaluator
from script import Script


if __name__ == '__main__':

    # Boilerplate.
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'some_tests.py')

    with open(filename) as f:
        script = Script(f.read())

    # Create the globals_dict we will test.
    evaluator = Evaluator()
    script.run(evaluator, dict(
            Eq = ast.Eq,
            a = 5,
            ))

    # Report on the outcome.
    success_count = 0
    for val in evaluator.data:
        if val is None:
            success_count += 1

    print('Total of {0} tests, {1} success'.format(len(evaluator.data), success_count))

    for i, val in enumerate(evaluator.data, 1):
        if val is not None:
            print((i, val))
