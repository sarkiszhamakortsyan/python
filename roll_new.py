#!/usr/bin/python

import sys
import os
import random

min = 1
max = 6

roll_dice = "yes"

try:
    if roll_dice == "yes" or roll_dice == "y":
        print (" ")
        print ("Rolling the dices ... ")
        print ("The values are ... ")
        print (" ")
        print random.randint(min, max)
        print random.randint(min, max)
        print (" ")
    elif roll_again == "no" or roll_again == "n":
        print (" ")
        print ("Program is shutting down ... ")
        print (" ")
        sys.exit()
    else:
        print ("Please type YES or NO ")
except KeyboardInterrupt:
    print ("\n")
    print ("Program is shutting down ...")
    print ("\n")
