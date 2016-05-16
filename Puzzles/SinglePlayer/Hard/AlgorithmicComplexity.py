import sys
import math
from itertools import repeat

complexity_names = ["O(1)", "O(log n)", "O(n)", "O(n log n)",
                    "O(n^2)", "O(n^2 log n)", "O(n^3)", "O(2^n)"]
complexities = [lambda x: 1,
                lambda x: math.log(x),
                lambda x: x,
                lambda x: x * math.log(x),
                lambda x: x * x,
                lambda x: x * x * math.log(x),
                lambda x: x**3,
                lambda x: 2**x]
# Compute the factors of how the data differs from the actual function output
# for each complexity. If the factors are (almost) a constant, pick this complexity.
complexity_to_factors=[[] for _ in range(len(complexities))]
n = int(input())
for i in range(n):
    num, t = [int(j) for j in input().split()]
    for index in range(len(complexities)):
        complexity_to_factors[index].append(t / complexities[index](num))

for factors in complexity_to_factors:
    factors.sort()
    #winsorise factors by cutting off too big or small and replace with next closest
    cut_perc = 3 # Cut x percent of smallest and biggest factors (anormal data)
    min_keep = int(n * cut_perc / 100) + 1
    max_keep = int(n * (100 - cut_perc) / 100)
    factors[: min_keep] = [factors[min_keep]] * min_keep
    factors[max_keep + 1:] = [factors[max_keep]] * (n - (max_keep + 1))
complexities_means = [sum(factors) / n for factors in complexity_to_factors]
complexities_variances = [sum(((factor - mean) ** 2 for factor in complexity_to_factors[i])) / n for i, mean in enumerate(complexities_means)]
complexities_std = [math.sqrt(var) for var in complexities_variances]
# Check the variation coefficients instead of std to standardize the measure
complexities_varcoeff = [std / mean if mean > 0. else float('inf') for std, mean in zip(complexities_std, complexities_means)]

varcoeff_index = complexities_varcoeff.index(min(complexities_varcoeff))
print(complexity_names[varcoeff_index])