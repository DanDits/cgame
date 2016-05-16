import sys
import math
from itertools import combinations
from collections import deque


def debug(text, *params, **keyword_params):
    print(text.format(*params, **keyword_params), file=sys.stderr)


def read_experiments():
    n = int(input())
    experiments = []
    for i in range(n):
        j, d = [int(j) for j in input().split()]
        experiments.append((j, j + d - 1))
    return n, experiments


def sort_end_time(experiments):
    return sorted(experiments, key=lambda exp: exp[1])


def check_intersect(interval1, interval2):
    return (interval1[0] <= interval2[1] and interval1[1] >= interval2[0])


def build_graph(n, experiments):
    experiments_graph = {i: [] for i in range(n)}
    # O(n^2) with n amount of experiments
    for exp1, exp2 in combinations(range(n), 2):
        if check_intersect(experiments[exp1], experiments[exp2]):
            experiments_graph[exp1].append(exp2)
            experiments_graph[exp2].append(exp1)
    return experiments_graph


def build_graph_fast(n, sorted_experiments):
    current = []
    experiments_graph = {i: [] for i in range(n)}
    current_time = -1
    for number, exp in enumerate(sorted_experiments):
        if exp[0] > current_time:
            current_time = exp[0]
            # remove experiments that are finished
            current = [curr_exp for curr_exp in current if sorted_experiments[curr_exp][1] >= current_time]
        for curr_exp in current:
            experiments_graph[curr_exp].append(number)
            experiments_graph[number].append(curr_exp)
        current.append(number)
    return experiments_graph


n, experiments = read_experiments()
experiments = sort_end_time(experiments)
count = 0
curr_time = -1
for exp in experiments:
    if exp[0] >= curr_time:
        count += 1
        curr_time = exp[1] + 1
print(count)