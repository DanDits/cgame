import sys
w, h = [int(i) for i in input().split()]
board = []
for i in range(h):
    board.append(list(input()))
    if 'B' in board[-1]:
        start_index = board[-1].index("B")
        start = (start_index, i)
        board[i][start_index] = 0

from collections import deque
q = deque()
q.append(start)
found = False
while len(q) > 0:
    #print("Current board", board, file=sys.stderr)
    cx,cy = q.popleft()
    curr = board[cy][cx]
    for dx,dy in [(-1,-2),(-2,-1),(1,-2),(2,-1),(1,2),(2,1),(-1,2),(-2,1)]:
        if 0 <= cx + dx < w and 0 <= cy + dy < h:
            tar = board[cy + dy][cx + dx]
            if tar == 'E':
                found = True
                print(curr + 1)
                q.clear()
                break
            elif tar == '.':
                board[cy + dy][cx + dx] = curr + 1
                q.append((cx + dx, cy + dy))
if not found:
    print("Impossible")