import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

rom_1 = input()
rom_2 = input()

values = (
          ["IV", 4, 1],
          ["IX", 9, 1],
          ["XL", 40, 1],
          ["XC", 90, 1],
          ["CD", 400, 1],
          ["CM", 900, 1],
          ["I", 1, 3],
          ["V", 5, 1],
          ["X", 10, 3],
          ["L", 50, 1],
          ["C", 100, 3],
          ["D", 500, 1],
          ["M", 1000, 4])
def rom_to_dec(rom):
    dec = 0
    i = 0
    while i < len(rom):
        for value in values:
            value_len = len(value[0])
            if i < len(rom) - value_len + 1 and value[0] == rom[i:i+value_len]:
                for _ in range(1, value_len):
                   i += 1 # skip some
                dec += value[1]
                break
        i += 1
    return dec
def find_closest_value(to_dec):
    dist = float('inf')
    best_value = None
    for value in filter(lambda val: val[2] > 0, values):
        dist_curr = to_dec - value[1]
        if 0 <= dist_curr < dist:
            dist = dist_curr
            best_value = value
    return best_value
def dec_to_rom(dec):
    rom = ""
    while dec > 0:
        value = find_closest_value(dec)
        value[2] -= 1
        dec -= value[1]
        rom += value[0]
    return rom
summed = rom_to_dec(rom_1) + rom_to_dec(rom_2)
print(dec_to_rom(summed))