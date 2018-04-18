# python's equivalent of
# javascript object spread. python >= 3.5


def hello(a: int, b: str, c: float):
    print('a:', a)
    print('b:', b)
    print('c:', c)


obj = {'a': 10, 'b': 'jack', 'c': 1.32}

# this will no work.
# TypeError: hello() missing 2 required positional arguments: 'b' and 'c'
# print(hello(obj))

# use single `*` to spread `obj` and
# map to hello args based on the order
print('- printing `hello()` using single asterisk (*obj):')
print(hello(*obj))
print()

# use double `**` to spread `obj` and
# map to hello args accordingin to `obj` keys
print('- printing `hello()` using double asterisk (**obj):')
print(hello(**obj))
print()

# this will not work because key `a` is missing (deleted)
del obj['a']
print(hello(**obj))
