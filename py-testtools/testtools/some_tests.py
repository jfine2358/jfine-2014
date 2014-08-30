Eq() != Eq()                    # Just like object().

# One per line.
dpe('1') == 'Num(n=1)'
dpe('1 < 2') == 'Compare(left=Num(n=1), ops=[Lt()], comparators=[Num(n=2)])'

# Same but as a loop.
for s, t in (
    ('1', Num(1)),
    ('1 < 2', Compare(Num(1), [Lt()], [Num(2)])),
    ):
    dpe(s) == ast.dump(t)
