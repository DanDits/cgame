import sys
import math


# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

def make_species(name, horns, legs, wings, eyes):
    return {"Name": name,
            "Heads": 1,
            "Horns": horns,
            "Legs": legs,
            "Wings": wings,
            "Eyes": eyes}


animals = [make_species(*spec) for spec in
           (("Rabbits", 0, 4, 0, 2),
            ("Chickens", 0, 2, 2, 2),
            ("Cows", 2, 4, 0, 2),
            ("Pegasi", 0, 4, 2, 2),
            ("Demons", 4, 4, 2, 4))]


def max_of_type(animal, all_attrs):
    attr_values = [all_attrs[item] // animal[item] for item in all_attrs if all_attrs[item] > 0 and animal[item] > 0]
    return min(attr_values) if len(attr_values) > 0 else 0


n = int(input())
species = []
for name in input().split():
    species.append([animal for animal in animals if animal["Name"] == name][0])

combined = {}
for i in range(n):
    thing, number = input().split()
    combined[thing] = int(number)


def check_next(all_species, all_attrs, result):
    if len(all_species) == 0:
        return result if all(all_attrs[attr] == 0 for attr in all_attrs) else False
    curr_species = list(all_species)
    speci = curr_species[0]
    del curr_species[0]
    for i in range(0, max_of_type(speci, all_attrs) + 1):
        curr_combined = dict(all_attrs)
        curr_result = list(result)
        curr_result.append((speci["Name"], i))
        for attr in all_attrs:
            curr_combined[attr] -= i * speci[attr]
        res = check_next(curr_species, curr_combined, curr_result)
        if res:
            return res


res = check_next(species, combined, [])
# print("RESULT:", res, file=sys.stderr)
for animal, count in res:
    print(animal, count)
