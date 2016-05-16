from math import sqrt

height = int(-0.5 + sqrt(0.25 + 2 * int(input())))

for i in range(1, height + 1):
    offset = 3 * (height - i)
    for part in (" *** ",
                 " * * ",
                 " * * ",
                 "*****"):
        print(" " * offset + " ".join((part,) * i) + " " * offset)
