#!/usr/bin/python3

import math

n = int(input('How many number to sum? '))
total = 0
i = 1

while i <= n:
    s = input('Enter number ' + str(i) + ': ')
    total = total + int(s)
    i = i + 1
print('The sum is ' + str(total))
