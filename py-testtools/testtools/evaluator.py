'''Evaluate expressions
'''

from trytools import try_eval
import operator

__metaclass__ = type


compare_dict = dict(
    # TODO: Finish this dict.
    Eq = operator.eq,
    Lt = operator.lt,
    )


class Evaluator:

    def __init__(self):

        self.data = []


    def compare(self, locals_dict, globals_dict, ops, codes):

        # TODO: Special case a single operation.
        # TODO: If you special case that, make sure you test.
        clean = True
        values = []
        for code in codes:
            val_or_exc = try_eval(code, globals_dict, locals_dict)
            if val_or_exc.exception:
                clean = False
            values.append(val_or_exc)

        comparisons = []
        for left, op, right in zip(values, ops, values[1:]):

            # TODO: Might raise exception.
            if left.exception or right.exception:
                comp = None
            else:
                comp = bool(compare_dict[op](left.value, right.value))
                if not comp:
                    clean = False
            comparisons.append(comp)

        if clean:
            self.data.append(None)
        else:
            self.data.append(values)


if __name__ == '__main__':

    from script import Script
    from trytools import ReturnValue, ExceptionInstance

    s = Script('''2 + 2 == 5; 2 + 2 == 4; 1 + '' < 4 ; 2 < 3''')
    expect = [
        [ReturnValue(4), ReturnValue(5)],
        None,
        [
            ExceptionInstance(
                TypeError("unsupported operand type(s) for +: 'int' and 'str'",)
                ),
            ReturnValue(4)
            ],
        None
        ]

    evaluator = Evaluator()
    s.run(evaluator)
    actual = evaluator.data

    assert TypeError('') != TypeError('')

    for i in range(4):
        if i == 2:
            continue            # TypeError('') != TypeError('')
        assert actual[i] == expect[i]
