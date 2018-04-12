# While normal functions are defined using the def keyword,
# in Python, anonymous functions are defined using the `lambda` keyword.

print('- lambda to add two numbers', (lambda x, y: x + y)(4, 2))


def multiplier(base: int) -> int:
    return lambda x: base * x


m = multiplier(5)
print("m of 5 =", m(5))
print("m of 2 =", m(2))
