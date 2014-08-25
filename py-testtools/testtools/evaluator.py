'''Evaluate expressions
'''

from trytools import try_eval

__metaclass__ = type

class Evaluator:

    def __init__(self):

        self.data = []


    def compare(self, locals_dict, globals_dict, ops, codes):

        values = [
            try_eval(code, globals_dict, locals_dict)
            for code in codes]


if __name__ == '__main__':

    from script import Script

    s = Script('2 + 2 == 5')
    evaluator = Evaluator()
    s.run(evaluator)
