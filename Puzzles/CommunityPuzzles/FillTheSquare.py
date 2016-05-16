import sys
import math
import numpy as np
from itertools import product

n = int(input())


def index(x, y, x_delta=0, y_delta=0):
    if 0 <= x + x_delta < n and 0 <= y + y_delta < n:
        return (y + y_delta) * n + (x + x_delta)
    return y * n + x  # self is default


# Our values live in the field F2 consisting of values 0 and 1
# represented as False and True.

# Build nxn connection matrix C representing top, left, right, lower
conn = [[False] * n * n for _ in range(n * n)]
for i, j in product(range(n), repeat=2):
    curr_index = index(i, j)
    for neighbor in [(-1, 0), (1, 0), (0, 0), (0, -1), (0, 1)]:
        conn[index(i, j, *neighbor)][curr_index] = True

lights = [False] * n * n  # for light state, right hand side b
for j in range(n):
    row = input()
    for i, state in enumerate(row):
        # even though True stands for "light" reverse it here
        lights[index(i, j)] = False if state == '*' else True

# Solve for x in: Cx=b in the  field F_2 of two numbers 0 and 1
# for this we cannot use linalg solve as this solves in real numbers
# Naive Gauss:
for y in range(n * n):
    # Ensure there is a True in row y
    if not conn[y][y]:
        # Search a True to swap to row y
        for k in range(y + 1, n * n):
            if conn[k][y]:
                conn[y], conn[k] = conn[k], conn[y]  # swap
                lights[y], lights[k] = lights[k], lights[y]
                break
    # Eliminate other Trues that are not in row y
    for k in range(n * n):
        if k != y and conn[k][y]:
            # adding row y on row k is equivalent to XOR
            conn[k] = [val1 ^ val2 for val1, val2 in zip(conn[k], conn[y])]
            lights[k] ^= lights[y]

for j in range(n):
    for i in range(n):
        print('.X'[lights[index(i, j)]], end='')
    print("")