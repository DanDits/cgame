import sys

rows = 6
grid = [list(input()) for _ in range(rows)]
columns = len(grid[0])


def make_turn(player, column):
    for row in range(rows - 1, -1, -1):
        if grid[row][column] == '.':
            copied = list(grid)
            copied[row] = list(copied[row])
            copied[row][column] = player
            return copied


def has_won(g, player):
    for row in range(rows):
        for column in range(columns):
            for dx, dy in ((0, -1), (1, -1), (1, 0), (1, 1)):
                no_win = False
                for i in range(0, 4):
                    r, c = row + i * dx, column + i * dy
                    if not (0 <= r < rows and 0 <= c < columns and g[r][c] == player):
                        no_win = True
                        break
                if not no_win:
                    return True
    return False


for player in ('1', '2'):
    winners = []
    for column in range(len(grid[0])):
        g = make_turn(player, column)
        if g and has_won(g, player):
            winners.append(str(column))
    if len(winners) > 0:
        print(" ".join(winners))
    else:
        print("NONE")