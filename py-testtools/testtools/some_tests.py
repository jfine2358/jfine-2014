Eq() != Eq()                    # Just like object().
dpe('1') == 'Num(n=1)'
dpe('1 < 2') == 'Compare(left=Num(n=1), ops=[Lt()], comparators=[Num(n=2)])'
