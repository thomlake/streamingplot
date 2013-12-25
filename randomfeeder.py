"""
author:
    tllake 
email:
    <thom.l.lake@gmail.com>
date:
    2013.12.25
file:
    randomfeeder.py
description:
    Generate random data, used to demo streamplot.py
"""

from random import randint, random, gauss, choice
from string import printable
numlines = [3, 2, 1]
#numlines = [3, 2, 1, 5, 2]
#numlines = [3, 2, 1, 5, 2, 2]
#numlines = [3, 2, 1, 5, 2, 2, 3]
#numlines = [3, 2, 1, 5, 2, 7, 11, 9]
#numlines = [5]

def randstr():
    return ''.join([choice(printable) for i in range(randint(5, 20))])

data = [[gauss(0, 1) for i in range(num)] for num in numlines]
print '>>', '; '.join(' '.join(str(x) for x in row) for row in data)

#while True:
for i in range(100):
    data = [[gauss(0, 1) + x for x in row] for row in data]
    if random() < 0.1: 
        print randstr()
    print '>>', '; '.join(' '.join(str(x) for x in row) for row in data)
    


