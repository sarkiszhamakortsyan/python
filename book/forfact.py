#!/usr/bin/python3

import math

n = int(input('Enter an integer >= 0: '))

fact = 1

for i in range(2, n + 1):
    fact = fact * i 
print(str(n) + ' factorial is ' + str(fact))
