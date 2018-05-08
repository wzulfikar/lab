> Fri, 27 Apr 2018 at 5:48:07 MYT

### Lesson 1: Introduction and Efficiency

1. common dimension to think in efficiency: time and space, ie. how long it takes for the program to finish and how much storage it needs
2. efficiency of code is described with big O notation: `O(n)` (in linear time)
3. example of big o notations:
    - `O(log(n))`
    - `O(1)` (aka `(On + 1)`)
    - `O(n+1)`
    - etc.
4. the `n` in `O(n)` represents the length of an input to your function
5. when we talk about efficiency, we often talk about the worst case scenario. for example, if we were talking about the best case scenario in alphabet, then we'll take `1` as best scenario (1 is minimum letter in alphabet) and `26` as the worst case scenario (26 is total number of alphabet)
6. average case means the average of best and worst case. in point number 5, the average case would be the number between 1 to 26, which is 13. hence, 13 is the average case.
7. best case, worst case and average case may not always approximate nicely. thus, you should specify (ie. to your interviewer) which case you're talking about
8. in interview, space efficiency is usually asked less than time efficiency
9. example of notation for space efficiency: `O(3n)` (ie. a function to copy input string 3 times)
12. big o cheatsheet: http://bigocheatsheet.com
11. sample code to practice on calculating efficiency using big o notation:

```py
"""input manatees: a list of "manatees", where one manatee is represented by a dictionary
a single manatee has properties like "name", "age", et cetera
n = the number of elements in "manatees"
m = the number of properties per "manatee" (i.e. the number of keys in a manatee dictionary)"""

# O(n) aka. linear
def example1(manatees):
    for manatee in manatees:
        print manatee['name']

# O(1) aka. constant
def example2(manatees):
    print manatees[0]['name']
    print manatees[0]['age']

# O(nm): each property multiple by each manatee
def example3(manatees):
    for manatee in manatees:
        for manatee_property in manatee:
            print manatee_property, ": ", manatee[manatee_property]

# O(n^2) aka. n squared (iterating over `manatess` list twice)
def example4(manatees):
    oldest_manatee = "No manatees here!"
    for manatee1 in manatees:
        for manatee2 in manatees:
            if manatee1['age'] < manatee2['age']:
                oldest_manatee = manatee2['name']
            else:
                oldest_manatee = manatee1['name']
    print oldest_manatee
```
