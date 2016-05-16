import sys
import math

n = int(input())
c = input()
s = int(input())
digits = [" x " +
          "x x" +
          "   " +
          "x x" +
          " x ",

          "  x" +
          "  x" +
          "   " +
          "  x" +
          "  x",

          " x " +
          "  x" +
          " x " +
          "x  " +
          " x ",

          " x " +
          "  x" +
          " x " +
          "  x" +
          " x ",

          "x x" +
          "x x" +
          " x " +
          "  x" +
          "  x",

          " x " +
          "x  " +
          " x " +
          "  x" +
          " x ",

          " x " +
          "x  " +
          " x " +
          "x x" +
          " x ",

          " x " +
          "  x" +
          "   " +
          "  x" +
          "  x",

          " x " +
          "x x" +
          " x " +
          "x x" +
          " x ",

          " x " +
          "x x" +
          " x " +
          "  x" +
          " x "]
for i, digit in enumerate(digits):
    digits[i] = digit.replace("x", c)
for i in range(5):
    line = []
    for c in ("%d" % n):
        digit = digits[int(c)]
        spread_digit = digit[3 * i] + digit[3 * i + 1] * s + digit[3 * i + 2]
        line.append(spread_digit)
    line = " ".join(line).rstrip()
    if i == 0 and line[0] == ' ': line = '.' + line[1:]
    for _ in range(max(1, (i % 2) * s)):
        print(line)