import sys
import math
import numpy as np
from numpy.linalg import norm
from itertools import product, count


def debug(text, *params, **keyword_params):
    print(text.format(*params, **keyword_params), file=sys.stderr)


MAX_ROT_DIFF_PER_STEP = 15
GRAVITY = 3.711
LANDING_WIDTH = 1000


def read_surface_and_landing():
    surface_n = int(input())  # the number of points used to draw the surface of Mars.
    landing_x = []
    landing_y = -1
    for i in range(surface_n):
        # land_x: X coordinate of a surface point. (0 to 6999)
        # land_y: Y coordinate of a surface point.
        # By linking all the points together in a sequential fashion, you form the surface of Mars.
        land_x, land_y = [int(j) for j in input().split()]
        if landing_y == land_y and land_x - landing_x[0] >= LANDING_WIDTH:
            landing_x.append(land_x)
        elif len(landing_x) < 2:
            landing_y = land_y
            landing_x = [land_x]
    landing_x = np.array(landing_x)
    debug("Landing area {} on height {}. Total surface points {}.", landing_x, landing_y, surface_n)
    return landing_x, landing_y


infinite = float("Inf")


def get_accel(rot, thrust):
    rot_in_rad = rot * math.pi / 180
    return np.array([math.sin(-rot_in_rad) * thrust, math.cos(rot_in_rad) * thrust - GRAVITY])


# Any positive integer, should be <= MAX_ANGLE_DIFF_PER_STEP and must be dividend of 90
rotation_delta = MAX_ROT_DIFF_PER_STEP
possible_rotations = [i * rotation_delta for i in range(-6, 7)]
possible_thrusts = [i for i in range(0, 5)]
possible_rot_thrusts = [(rot, thrust) for rot, thrust in product(possible_rotations, possible_thrusts)]
possible_accels = [get_accel(rot, thrust) for rot, thrust in possible_rot_thrusts]
extreme_descend_rot_thrusts = [(rot, thrust) for rot, thrust in possible_rot_thrusts
                               if abs(rot) == 90 or (rot == 0 and thrust == 0)]
extreme_descend_accels = [get_accel(rot, thrust) for rot, thrust in extreme_descend_rot_thrusts]


def arg_min(function, parameters):
    min_value = infinite
    best_parameter = None
    best_index = -1
    for index, parameter in enumerate(parameters):
        value = function(parameter)
        if value < min_value:
            min_value = value
            best_parameter = parameter
            best_index = index
    return best_index, best_parameter


def find_closest_rot_thrust_by_norm(to_accel):
    index, accel = arg_min(lambda acc: norm(to_accel - acc), possible_accels)
    return possible_rot_thrusts[index] + (accel,)


def get_exact_rot(to_accel):
    angle = math.atan2(to_accel[1], to_accel[0])  # between -pi and pi
    # Convert to rot that represents the same angle in the circle that got offset by -GRAVITY
    # For this solve the quadratic equation (r cos(a))²+(r sin(a) + GRAVITY)² = 16 for positive r
    sin_angle = math.sin(angle)
    first_term = -GRAVITY * sin_angle
    second_term = math.sqrt(GRAVITY * GRAVITY * sin_angle * sin_angle - GRAVITY * GRAVITY + 4 * 4)
    r = max(first_term - second_term, first_term + second_term)

    real_angle = math.atan2(r * sin_angle + GRAVITY, r * math.cos(angle))
    if real_angle < 0:
        return None
    # Finally convert to rot
    rot = real_angle - math.pi / 2
    return int(rot * 180 / math.pi + 0.5)  # to degrees


def find_closest_rot_thrust(to_accel):
    if to_accel[1] >= 0:
        # We want to ascend, get exact rotation and enforce thrust=4
        rot = get_exact_rot(to_accel)
        thrust = 4
        return rot, thrust, get_accel(rot, thrust)
    # We want to descend
    rot = get_exact_rot(to_accel)  # Could be out of [-90, 90] interval
    if rot is not None:
        thrust = 4
        return rot, thrust, get_accel(rot, thrust)

    to_angle = math.atan2(to_accel[1], to_accel[0])

    def angle_diff(acc):
        angle = math.atan2(acc[1], acc[0])  # between -pi and pi
        return min(abs(angle - to_angle), abs(2 * math.pi + angle - to_angle), abs(2 * math.pi + to_angle - angle))

    index, accel = arg_min(angle_diff, extreme_descend_accels)
    return extreme_descend_rot_thrusts[index] + (accel,)


def change_by_max_step(value, target_value, max_step):
    return min(max(target_value, value - max_step), value + max_step)


def linear_change(start_value, end_value, step):
    # Generates an infinite sequence in interval [start_value, end_value] with two successive points
    # being at most abs(step) from each other
    return (change_by_max_step(start_value, end_value, i * step) for i in count())


def advance_state(state, target_rot=None, target_thrust=None):
    def advance_to_target(target_rot, target_thrust):
        target_rot = target_rot if target_rot is not None else state["rot"]
        target_thrust = target_thrust if target_thrust is not None else state["thrust"]

        # Assume changes order: pos before speed before accel before fuel before rot/thrust
        state["pos"] += state["speed"]
        state["speed"] += get_accel(state["rot"], state["thrust"])
        state["fuel"] -= state["thrust"]
        state["rot"] = change_by_max_step(state["rot"], target_rot, MAX_ROT_DIFF_PER_STEP)
        state["thrust"] = change_by_max_step(state["thrust"], target_thrust, 1)
        return state["rot"] == target_rot and state["thrust"] == target_thrust

    count = 1
    while not advance_to_target(target_rot, target_thrust):
        count += 1
    return count


def copy_state(state):
    return make_state(state["pos"][0], state["pos"][1],
                      state["speed"][0], state["speed"][1],
                      state["fuel"],
                      state["rot"],
                      state["thrust"])


def make_state(x, y, speed_x, speed_y, fuel, rotate, thrust):
    return {"pos": np.array([x, y]),
            "speed": np.array([speed_x, speed_y]),
            "fuel": fuel,
            "rot": rotate,
            "thrust": thrust}


def _calculate_steps(s0, s, accel, speed):
    a = 0.5 * accel
    b = speed
    c = s0 - s
    if a == 0:
        return infinite if b == 0 or -c / b < 0 else -c / b
    discr = b * b - 4 * a * c
    if discr < 0:
        return infinite
    results = (-b + math.sqrt(discr)) / (2 * a), (-b - math.sqrt(discr)) / (2 * a)
    return int((min(results) if min(results) > 0 else max(results)) + 0.5)


def _calculate_steps_for_speed(v0, v, accel):
    if accel == 0:
        return 0 if v0 == v else infinite
    return int((v - v0) / accel + 0.5)


def estimate_steps_between_states(start_state, end_state, only_speed=False):
    accel = get_accel(start_state["rot"], start_state["thrust"])
    if only_speed:
        return np.array([_calculate_steps_for_speed(start_state["speed"][i], end_state["speed"][i], accel[i])
                         for i in range(2)])
    # Under the assumption that start state rotation and thrust and therefore the acceleration do not change
    # Also ignore the speed, rot and thrust of target state, only the position is relevant here
    # s = 1/2*a*t² + v*t + s0 for x and y direction with
    # a being the acceleration, t the steps, s0 the start position, s the target position, v the start speed
    return np.array([_calculate_steps(start_state["pos"][i], end_state["pos"][i], accel[i], start_state["speed"][i])
                     for i in range(2)])


def read_state():
    values = [int(i) for i in input().split()]
    return make_state(*values)


landing_area_x, landing_area_y = read_surface_and_landing()

# game loop
debug("Starting game loop")
target_state = make_state(np.mean(landing_area_x), landing_area_y, 0, 0, 0, 0, 0)
start_speed_x = None
emergency_x_break = False
while True:
    # h_speed: the horizontal speed (in m/s), can be negative.
    # v_speed: the vertical speed (in m/s), can be negative.
    # fuel: the quantity of remaining fuel in liters.
    # rotate: the rotation angle in degrees (-90 to 90).
    # power: the thrust power (0 to 4).
    curr_state = read_state()
    if start_speed_x is None:
        start_speed_x = curr_state["speed"][0]
        if abs(start_speed_x) > 20:
            emergency_x_break = True

    debug("Current {}", curr_state)
    debug("Target {}", target_state)

    steps_without_changes = estimate_steps_between_states(curr_state, target_state)
    debug("Steps when not changing anything {})", steps_without_changes)

    if abs(curr_state["speed"][0]) < 20:
        emergency_x_break = False
    if emergency_x_break:
        debug("EMERGENCY BRAKING TO SLOW DOWN X SPEED!")
        target_rot, target_thrust, _ = find_closest_rot_thrust([-start_speed_x, 0])

        print(target_rot, target_thrust)
        continue
    dist_to_move = target_state["pos"] - curr_state["pos"]
    target_rot, target_thrust, target_accel = find_closest_rot_thrust(dist_to_move)

    power_state = copy_state(curr_state)
    steps_to_power_state = advance_state(power_state, target_rot, target_thrust)

    steps_to_target = steps_to_power_state + estimate_steps_between_states(power_state, target_state)

    debug("Steps when moving in fastest way {})", steps_to_target)

    debug("Target rot {}, target thrust {} when minimizing distance {}",
          target_rot, target_thrust, dist_to_move)
    if min(steps_to_target) < infinite:
        speed_to_change = target_state["speed"] - curr_state["speed"]
        break_rot, break_thrust, break_accel = find_closest_rot_thrust(speed_to_change)
        break_state = copy_state(power_state)
        steps_to_break_state = advance_state(break_state, break_rot, break_thrust)
        steps_to_break = steps_to_power_state + steps_to_break_state + estimate_steps_between_states(break_state,
                                                                                                     target_state,
                                                                                                     only_speed=True)

        debug("Current speed to change {}", speed_to_change)
        debug("Best rot {}, best thrust {} when asking break", break_rot, break_thrust)
        debug("Required steps for breaking {} (to break state are {})", steps_to_break, steps_to_break_state)
        if ((steps_to_break[0] >= steps_to_target[0] and (
                steps_without_changes[0] is infinite or abs(curr_state["speed"][0]) >= 15))
            or (steps_to_break[1] >= steps_to_target[1] and (steps_without_changes[1] is infinite or abs(
                curr_state["speed"][1]) >= 35))):  # TODO maybe try comparing x/y separately
            debug("NEED TO BREAK")
            target_rot = break_rot
            target_thrust = break_thrust

    dist_to_edge_x = landing_area_x - curr_state["pos"][0]
    speed_x, speed_y = curr_state["speed"]
    steps_to_landing_area_x = dist_to_edge_x[1] / speed_x if speed_x < 0 else (
    dist_to_edge_x[0] / speed_x if speed_x > 0 else infinite)
    over_landing_area = landing_area_x[0] <= curr_state["pos"][0] <= landing_area_x[1]
    if over_landing_area:
        debug("OVER LANDING AREA!")
        if abs(speed_x) <= 20:
            steps_over_land_x = dist_to_edge_x[0] / speed_x if speed_x < 0 else (
            dist_to_edge_x[1] / speed_x if speed_x > 0 else infinite)
            steps_over_land_x = 0 if steps_over_land_x < 0 else steps_over_land_x
            steps_to_land_y = _calculate_steps(curr_state["pos"][1], landing_area_y,
                                               get_accel(curr_state["rot"], curr_state["thrust"])[1],
                                               curr_state["speed"][1])
            debug("Dist to edge {}, steps over land {}, steps to land y {}", dist_to_edge_x, steps_over_land_x,
                  steps_to_land_y)
            if (abs(speed_x) <= 2 or speed_y >= 0 or abs(target_state["pos"][1] - curr_state["pos"][1]) <= 2 * abs(
                    speed_y)
                or (steps_over_land_x > 0 and steps_over_land_x >= steps_to_land_y)):
                target_rot = 0
                target_thrust = 0
            else:
                target_rot = int(math.copysign(15, speed_x))
                target_thrust = 3
            if abs(speed_y) > 30:
                target_thrust = 4
    elif 5 > steps_to_landing_area_x > 0 and abs(speed_x) <= 20:
        debug("ALMOST OVER LANDING AREA!")
        target_rot = 0
        target_thrust = 0
        if abs(speed_y) > 30:
            target_thrust = 4
    # rotate power. rotate is the desired rotation angle. power is the desired thrust power.
    print(target_rot, target_thrust)
