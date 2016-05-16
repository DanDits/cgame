import sys
import math

n = int(input())

remainder_positions = {}

curr = 1
digits = []
repeating_remainder = -1
while curr != 0 and repeating_remainder == -1:
    if curr < n:
        fillers = math.ceil(math.log(n / curr, 10))
        for i in range(fillers):
            if curr in remainder_positions:
                repeating_remainder = remainder_positions[curr]
                break
            remainder_positions[curr] = len(digits)
            curr *= 10
            if fillers > 1 and i != fillers - 1:
                digits.append(0)
    if repeating_remainder == -1:
        digit = curr // n
        curr %= n
        digits.append(digit)
digits = list(map(str, digits))
if repeating_remainder == -1:
    print("0." + "".join(digits))
else:
    result = "0." + "".join(digits[:repeating_remainder])
    result += "(" + "".join(digits[repeating_remainder:]) + ")"
    print(result)
