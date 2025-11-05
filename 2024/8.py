import numpy as np
import math
import itertools

with open("8 input", "r") as file:
    map = np.array([[i for i in line.replace("\n", "")] for line in file])

width, height = map.shape
antennas = {}
antenna_location_pairs = []
for index, i in np.ndenumerate(map):
    if i == ".":
        continue
    index_tuple = (index[1], index[0])
    if i in antennas:
        antennas[i][0].append(index_tuple)
    else:
        antennas[i] = [[index_tuple], []]
    antenna_location_pairs.append((index_tuple, i))


def calc_distance(one, two):
    return math.sqrt((one[0] - two[0]) ** 2 + (one[1] - two[1]) ** 2)

def calc_angle(one, two):
    dy = two[0] - one[0]
    dx = two[1] - one[1]
    return math.atan2(dy, dx)

def round_tuple(value):
    return (int(round(value[0])), int(round(value[1])))

def antinodes(node_one, node_two):
    distance = calc_distance(node_one, node_two)
    angle = calc_angle(node_one, node_two)
    antinode_one = (node_one[0] - distance * math.sin(angle), node_one[1] - distance * math.cos(angle))
    antinode_two = (node_two[0] + distance * math.sin(angle), node_two[1] + distance * math.cos(angle))
    # print(f"{angle=}, {distance=}: {antinode_one} => {round_tuple(antinode_one)} and {antinode_two} => {round_tuple(antinode_two)}")
    # assert calc_distance(round_tuple(antinode_one), node_one) * 2 == calc_distance(round_tuple(antinode_one), node_two) or calc_distance(round_tuple(antinode_one), node_one) == calc_distance(round_tuple(antinode_one), node_two) * 2
    # assert calc_distance(round_tuple(antinode_two), node_one) * 2 == calc_distance(round_tuple(antinode_two), node_two) or calc_distance(round_tuple(antinode_two), node_one) == calc_distance(round_tuple(antinode_two), node_two) * 2
    # print(f"Distance from antinode one {calc_distance(round_tuple(antinode_one), node_one)} and {calc_distance(round_tuple(antinode_one), node_two)}")
    return (round_tuple(antinode_one), round_tuple(antinode_two))

# count = 0
# all_anti = []
# antenna_locations = [i[0] for i in antenna_location_pairs]
# for i in antennas:
#     nodes = antennas[i][0]
#     for j in itertools.combinations(nodes, 2):
#         for k in antinodes(j[0], j[1]):
#             if width >= k[0] >= 0 and height >= k[1] >= 0:
#
#                 if not k in antennas[i][1]: #and not k in antenna_locations:
#                     antennas[i][1].append(k)
#                     if not k in all_anti:
#                         count += 1
#                         all_anti.append(k)

all_anti = set()
antenna_locations = [i[0] for i in antenna_location_pairs]

for i in antennas:
    nodes = antennas[i][0]
    for j in itertools.combinations(nodes, 2):
        for k in antinodes(j[0], j[1]):
            if 0 <= k[0] < width and 0 <= k[1] < height:
                antennas[i][1].append(k)
                all_anti.add(k)

count = len(all_anti)

# print(all_anti)
# print(antennas)
# print(antenna_location_pairs)
# print(len(all_anti))
print(f"Part One: {count}")




def antinodes(node_one, node_two):
    epsilon = 0.0001
    distance = calc_distance(node_one, node_two)
    angle = calc_angle(node_one, node_two)
    antinodes = []
    for i in range(width):
        for j in range(height):
            dist = calc_distance((i, j), node_one)
            anti = (i + dist * math.sin(angle), j + dist * math.cos(angle))
            difference = (abs(anti[0] - node_one[0]), abs(anti[1] - node_one[1]))
            if difference[0] <= epsilon and difference[1] <= epsilon:
                antinodes.append((i, j))
                continue
            anti = (i - dist * math.sin(angle), j - dist * math.cos(angle))
            difference = (abs(anti[0] - node_one[0]), abs(anti[1] - node_one[1]))
            if difference[0] <= epsilon and difference[1] <= epsilon:
                antinodes.append((i, j))
    # antinode_one = (node_one[0] - distance * math.sin(angle), node_one[1] - distance * math.cos(angle))
    # antinode_two = (node_two[0] + distance * math.sin(angle), node_two[1] + distance * math.cos(angle))
    return antinodes

all_anti = set()
antenna_locations = [i[0] for i in antenna_location_pairs]

for i in antennas:
    nodes = antennas[i][0]
    for j in itertools.combinations(nodes, 2):
        for k in antinodes(*j):
            if 0 <= k[0] < width and 0 <= k[1] < height:
                antennas[i][1].append(k)
                all_anti.add(k)

count = len(all_anti)
print(f"Part Two: {count}")

text_map = ""
for i in range(height):
    for j in range(width):
        index_tuple = (j, i)
        if index_tuple in antenna_locations:
            text_map += antenna_location_pairs[antenna_locations.index(index_tuple)][1]
        elif index_tuple in all_anti:
            text_map += "#"
        else:
            text_map += "."

    text_map += "\n"
# print(text_map)
