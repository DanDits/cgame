import sys

n = int(input())
pairs = []
for i in range(n):
    x, y = [int(j) for j in input().split()]
    pairs.append((x, y))
def min_max(axis):
    if len(pairs) == 0:
        return -1, 1
    return (min(0, min(pairs, key=lambda x:x[axis])[axis]) - 1,
        max(0, max(pairs, key=lambda x:x[axis])[axis]) + 1)
minmax_x = min_max(0)
minmax_y = min_max(1)

for y in range(minmax_y[1], minmax_y[0] - 1, -1):
    line = []
    for x in range(minmax_x[0], minmax_x[1] + 1):
        if (x,y) in pairs:
            line.append("*")
        elif y == 0 and x == 0:
            line.append("+")
        elif y == 0:
            line.append("-")
        elif x == 0:
            line.append("|")
        else:
            line.append(".")
    print("".join(line))