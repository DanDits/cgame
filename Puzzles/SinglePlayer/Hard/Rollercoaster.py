import sys
import math
from collections import deque


def debug(text, *params, **keyword_params):
    print(text.format(*params, **keyword_params), file=sys.stderr)


places, c, n = [int(i) for i in input().split()]
start_q = deque((int(input()) for i in range(n)))
debug("Places in roller coaster={}, possible runs={}, groups={}", places, c, n)
total_people = sum(start_q)


def next_ride(q):
    left_places = places
    for _ in range(n):
        curr_group = q.popleft()
        if left_places < curr_group:
            q.appendleft(curr_group)  # they dont want to be seperated, so stop
            break
        q.append(curr_group)  # they line up at the end (after the ride...)
        left_places -= curr_group
    return places - left_places  # number of people on ride and money they paid


def simple():
    q = deque(start_q)
    earned = 0
    for i in range(c):
        earned += next_ride(q)
    return earned


def fast():
    q = deque(start_q)
    permutations = []
    earned_by_ride = []
    people_ridden = 0
    zyklus_start_index = -1
    zyklus_length = 0
    zyklus_earned = 0
    for i in range(n + 1):
        curr_q = tuple(q)
        if people_ridden < total_people or curr_q not in permutations:
            permutations.append(curr_q)
            curr_people = next_ride(q)
            earned_by_ride.append(curr_people)
            people_ridden += curr_people
        else:
            zyklus_start_index = permutations.index(curr_q)
            zyklus_length = len(permutations) - zyklus_start_index
            zyklus_earned = sum(earned_by_ride[zyklus_start_index:])
            break
    debug("Zyklus index {}, zyklus length {}, zyklus earned {}", zyklus_start_index, zyklus_length, zyklus_earned)
    total_rides = c
    pre_zyklus_rides = min(zyklus_start_index, total_rides)
    earned = sum(earned_by_ride[0:pre_zyklus_rides])
    total_rides -= pre_zyklus_rides

    total_zyklen = int(total_rides / zyklus_length)
    earned += total_zyklen * zyklus_earned
    total_rides -= total_zyklen * zyklus_length

    earned += sum(earned_by_ride[zyklus_start_index:zyklus_start_index + total_rides])
    return earned


print(fast())
