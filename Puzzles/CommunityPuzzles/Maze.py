w, h = [int(i) for i in input().split()]
x, y = [int(i) for i in input().split()]
maze = [[state for state in input()] for _ in range(h)]

q = [(x, y)] # start position
exits = set()
# we use breath first search and only visit neighbors with a '.'
while len(q) > 0:
    x, y = q.pop()
    if maze[y][x] != '.':
        continue
    maze[y][x] = 'X' # do not visit twice
    for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        cx, cy = x + dx, y + dy
        if not (0 <= cx < w) or not(0 <= cy < h):
            exits.add((x, y))
        elif maze[cy][cx] == ".":
            q.append((cx, cy))
exits = sorted(exits)
print(len(exits))
for exit in exits:
    print(*exit)
