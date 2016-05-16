import sys
import math

n = int(input())


def get_triangle(size):
    return [(" " * (size - i) + "*" * (2 * i - 1), " " * (size - i)) for i in range(1, size + 1)]


triangle_lines = get_triangle(n)
offset = " " * n
for i, line in enumerate(triangle_lines):
    print(offset + line[0] if i > 0 else "." + (" " * (n - 1)) + line[0])
for line in triangle_lines:
    print("".join(line) + " " + line[0])
