import math


x_1, y_1, r = [int(i) for i in input().split()]
x_2, y_2, R = [int(i) for i in input().split()]

dist = math.sqrt((x_1 - x_2) ** 2 + (y_1 - y_2) ** 2)
r, R = min(r,R), max(r,R)
if dist >= r + R:
    area = 0. # no intersection
elif R >= dist + r:
    area = math.pi * (r ** 2) # one in another
elif False:
    def circular_segment(radius, triang_height):
        return (radius ** 2) * math.acos(triang_height / radius) - triang_height * math.sqrt(radius ** 2 - triang_height ** 2)
    area1 = circular_segment(r, (dist ** 2 + (r ** 2) - (R ** 2)) / (2 * dist))
    area2 = circular_segment(R, (dist ** 2 + (R ** 2) - (r ** 2)) / (2 * dist))
    area = area1 + area2
else:
    part1 = r*r*math.acos((dist*dist + r*r - R*R)/(2*dist*r))
    part2 = R*R*math.acos((dist*dist + R*R - r*r)/(2*dist*R))
    part3 = 0.5*math.sqrt((-dist+r+R)*(dist+r-R)*(dist-r+R)*(dist+r+R))
    area = part1 + part2 - part3
print("{:.2f}".format(area))

