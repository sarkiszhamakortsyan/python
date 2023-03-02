#!/usr/bin/python3

import os
import sys
import math

print("\nAQUARIUM CALCULATOR\n\n")

try:
    hight = float(input("Enter the hight in sm: "))
    depth = float(input("Enter the depth in sm: "))
    lenght = float(input("Enter the lenght in sm: "))

    print("\nThe result is:", hight * depth * lenght / 1000, "liters")
    print("The result is:", hight * depth * lenght / 1000 * 3.7854, "US gallons")
    print("The result is:", hight * depth * lenght / 1000 * 4.5461, "UK gallons\n")

except KeyboardInterrupt:
    print ("\n\nShutting down ...\n")
