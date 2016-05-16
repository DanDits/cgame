import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.


# game loop
while True:
    heights = [int(input()) for _ in range(8)]
    print(heights.index(max(heights)))
