import sys
import math
from itertools import chain

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

numbers = [int(number) for number in input()[1:-1].split(",")]
numbers.sort()

def next_entry():
    range_start = -1
    last_number = -1
    def give():
        if range_start == last_number:
            return (str(range_start),)
        else:
            return str(range_start), str(last_number)
    for number in chain(numbers, [None]):
        if last_number + 1 != number:
            if range_start != -1:
                if range_start == last_number:
                    yield (str(range_start),)
                elif range_start == last_number - 1:
                    yield (str(range_start),)
                    yield (str(range_start + 1),)
                else:
                    yield str(range_start), str(last_number)
            range_start = number
        last_number = number
print(",".join(("-".join(nums) for nums in next_entry())))
