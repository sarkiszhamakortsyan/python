#!/usr/bin/python3

import sys
import os
from math import *

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def devide(a, b):
    return a / b

def sqart(a):
    return sqrt(a)
    
print ("\n\n")
print ("##############")
print ("# CALCULATOR #")
print ("##############","\n")
print ("Choose an action: ")
print ("1. Add ")
print ("2. Subtract ")
print ("3. Multiply ")
print ("4. Devide ")
print ("5. Sqart")

try:
    choise = input("Please enter your choise: ")

    num1 = int(input("Please enter the first number: "))
    num2 = int(input("Please enter the second number: "))

    if choise == "1":
        print (num1,"+",num2,"=", add(num1,num2))
    elif choise == "2":
        print (num1,"-",num2,"=", subtract(num1,num2))
    elif choise == "3":
        print (num1,"*",num2,"=", multiply(num1,num2))
    elif choise == "4":
        print (num1,"/",num2,"=", devide(num1,num2))
    elif choise == "5":
        print ("Sqart of ", num1, "=", sqart(num1))
    else:
        print ("Please enter correct choise")
except KeyboardInterrupt:
    print ("\n\n","Program is shutting down ... ", "\n")
