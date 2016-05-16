import sys
import math

n = int(input())
x = [int(i) for i in input().split()]

zeros = 0
to_swap_zero = []
ones = 0
to_swap_ones = []
for i in range(len(x)):
    zeros += x[i] == 0
    to_swap_zero.append(zeros)
    ones += x[-i - 1] == 1
    to_swap_ones.append(ones)
to_swap_ones = list(reversed(to_swap_ones))

min_val = 0
min_diff = float('inf')
for val0, val1 in zip(to_swap_zero, to_swap_ones):
    diff = abs(val0 - val1)
    if diff < min_diff:
        min_diff = diff
        min_val = min(val0, val1)

print(min_val)