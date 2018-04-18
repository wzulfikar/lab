from typing import NamedTuple  # python >= 3.6.0
import time


class Person(NamedTuple):
    name: str
    age: int
    gender: str
    married: bool = False  # default value (python >= 3.6.1)


# initialize person `eve` with all args
eve = Person(name='Eve', age=31, gender='female', married=True)
print(type(eve))
print(eve)
print()

# initialize person `bob` omitting default arg `married`
bob = Person(name='Bob', age=21, gender='male')
print(type(bob))
print(bob)
print()


# this will not work:
# TypeError: __new__() missing 1 required positional argument: 'gender'
try:
    dan = Person(name='Dan', age=22)
except TypeError as e:
    print('failed to initialize person `dan`:\n', e)
