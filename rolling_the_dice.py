#!/usr/bin/python

import random

min = 1
max = 6

roll_again = "yes"
#roll_dice = raw_input("Do you want to roll the dice: ")

while roll_again == "yes" or roll_again == "y":
	print "Rolling the dices ... "
	print "The values are ... "
	print random.randint(min, max)
	print random.randint(min, max)

        roll_again = raw_input("Roll the dices again?")
