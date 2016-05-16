import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

width, height = [int(i) for i in input().split()]
columns = [[] for _ in range(width)]
for _ in range(height):
    for col, symbol in enumerate(input()):
        columns[col].append(symbol)
for column in columns:
    column.sort(reverse=True)
for i in range(height):
    print("".join(col[i] for col in columns))

