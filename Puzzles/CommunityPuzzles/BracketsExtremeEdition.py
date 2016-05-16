import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

expression = input()
brackets = {"(":")", "[":"]", "{":"}"}
bstack = []
correct = True
for char in expression:
    if char in brackets:
        bstack.append(brackets[char])
    elif char in brackets.values():
        if len(bstack) > 0 and bstack[-1] == char:
            del bstack[-1] # correct
        else:
            correct = False
            break
correct &= len(bstack) == 0

print(("false", "true")[correct])
