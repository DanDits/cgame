import sys
import math

width, height = [int(i) for i in input().split()]

state = []

state.extend("0" * (width + 2))
for i in range(height):
    line = "0" + input() + "0"
    state.extend(line)
state.extend("0" * (width + 2))

neighbors = [-width - 3, -width - 2, -width - 1,
             -1, 1,
             width + 1, width + 2, width + 3]


def rule(index):
    alive = sum(int(state[index + neighbor]) for neighbor in neighbors)
    return (("0", "1"), state[index])[alive == 2][alive == 3]


for i in range(height):
    print("".join(rule((width + 2) * (i + 1) + j + 1) for j in range(width)))