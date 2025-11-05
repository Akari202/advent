import numpy as np
from tqdm import tqdm

def to_num(position):
    if position == ".":
        return 0
    elif position == "#":
        return -1
    elif position == "^":
        return 1


def print_map(map):
    for i in map:
        for j in i:
            if j > 0:
                print("X", end="")
            elif j == 0:
                print(".", end="")
            elif j < 0:
                print("#", end="")
        print("")


def direction(rotation):
    rotation = rotation % 4
    if rotation < 0:
        rotation = 4 + rotation
    match rotation:
        case 1:
            return (-1, 0)
        case 0:
            return (0, 1)
        case 3:
            return (1, 0)
        case 2:
            return (0, -1)


with open("6 input", "r") as file:
    map = np.array([[to_num(i) for i in line.strip("\n")] for line in file])
map_part_two = np.copy(map)

position = np.where(map == 1)
position = np.array((int(position[0][0]), int(position[1][0])))
rotation = 1
try:
    while not np.any(np.add(position, np.array(direction(rotation))) < 0):
        if map[tuple(np.add(position, np.array(direction(rotation))))] < 0:
            rotation -= 1
        else:
            position = np.add(position, np.array(direction(rotation)))
            map[tuple(position)] += 1
        # print(f"{position=}, {rotation=} -> {rotation % 4}, {direction(rotation)}, {map[tuple(position)]}, {np.max(map)}, {np.any(position < 0)}")
        # print_map(map)
except IndexError:
    # print("oops")
    pass

# print(map.shape)

print(f"Part One: {(map > 0).sum()}")

def test_loop():
    position = np.where(map == 1)
    position = np.array((int(position[0][0]), int(position[1][0])))
    rotation = 1
    try:
        while not np.any(np.add(position, np.array(direction(rotation))) < 0):
            if map[tuple(np.add(position, np.array(direction(rotation))))] < 0:
                rotation -= 1
            else:
                position = np.add(position, np.array(direction(rotation)))
                map[tuple(position)] += 1

            if np.max(map) > 5:
                return 1
    except IndexError:
        pass
    return 0

obstacle_count = 0
for i in tqdm(range(map.shape[0])):
    for j in tqdm(range(map.shape[1]), leave=False):
        map = np.copy(map_part_two)
        if map[i, j] != 0:
            continue
        else:
            map[i, j] = -1
            obstacle_count += test_loop()

print(f"Part Two: {obstacle_count}")


