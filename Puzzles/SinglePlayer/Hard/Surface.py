import sys
import math
from collections import deque


# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.
class WaterMarker:
    def __init__(self, size=1):
        self.size = size
        self.links = []

    def get_size(self):
        # need to combine every connected marker, cannot do this recursivly do to stack overflow for big test
        summed = 0
        q = deque()
        q.append((None, self))
        connected = []
        while len(q) > 0:
            exclude, marker = q.popleft()
            if marker in connected:
                continue
            connected.append(marker)
            summed += marker.size
            for link in marker.links:
                if link != exclude and link not in connected:
                    q.append((marker, link))
        for marker in connected:
            marker.size = summed
            marker.links = []
        return summed

    def link_to(self, marker):
        if marker not in self.links and marker != self:
            self.links.append(marker)
            marker.links.append(self)

    def __str__(self):
        return str(self.get_size())

    def __repr__(self):
        return str(self.get_size())


land = WaterMarker(0)
l = int(input())
h = int(input())

field = []
for i in range(h):
    field_row = list()
    field.append(field_row)
    for j in range(l):
        field_row.append(land)


def debug_field():
    print("FIELD:", file=sys.stderr)
    for i in range(h):
        print(field[i], file=sys.stderr)


for i in range(h):
    row = input()
    field_row = field[i]
    for j, char in enumerate(row):
        if char == "O":
            # water here, lets see if we can link this to another lake
            # first check left side
            linked_to_left, linked_to_top = False, False
            if j > 0 and field_row[j - 1] is not land:
                linked_to_left = True
                field_row[j] = field_row[j - 1]
                field_row[j].size += 1
            # then check last row
            if i > 0 and field[i - 1][j] is not land:
                linked_to_top = True
                if not linked_to_left:
                    field_row[j] = field[i - 1][j]
                    field_row[j].size += 1
                else:
                    # link upper marker to new lower marker, size already got increased
                    field[i - 1][j].link_to(field_row[j])
            if not linked_to_left and not linked_to_top:
                # new water here!
                field_row[j] = WaterMarker()

n = int(input())
for i in range(n):
    x, y = [int(j) for j in input().split()]
    print(field[y][x].get_size())
