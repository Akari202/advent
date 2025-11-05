import numpy as np
from scipy.ndimage import label, binary_dilation

with open("12 input test", "r") as file:
    plot_map = np.array([[j for j in i.replace("\n", "")] for i in file])

plants = set(plot_map.flatten())

print(plot_map)
print(plants)

def calculate_cost(array):
    labeled_array, num_features = label(array)
    cost = 0
    for region_label in range(1, num_features + 1):
        region = (labeled_array == region_label)
        area = np.sum(region)

        top = np.roll(region, shift=-1, axis=0)
        bottom = np.roll(region, shift=1, axis=0)
        left = np.roll(region, shift=-1, axis=1)
        right = np.roll(region, shift=1, axis=1)
        perimeter = np.sum(region & ~top) + \
                np.sum(region & ~bottom) + \
                np.sum(region & ~left) + \
                np.sum(region & ~right)

        cost += area * perimeter
        # print(f"Cost of region {area} * {perimeter} = {area * perimeter}")

    return cost


total_cost = 0
for i in plants:
    plots = (plot_map == i)
    # plot_pad = np.pad(plots.astype(int), [(1, 1), (1, 1)], mode="constant", constant_values=0)
    # for m, j in enumerate(plots[:]):
    #     for n, k in enumerate(j):
    #         if not k:
    #             print(" ", end="")
    #         else:
    #             print(plot_map[m][n], end="")
    #     print("")
    cost = calculate_cost(plots)
    # print(f"For plant {i} cost {cost}")
    total_cost += cost
    # break

print(f"Part One: {total_cost}")


def print_array(array):
    array_int = array.astype(int)
    print("+", end="")
    for _ in range(array_int.shape[0]):
        print("-", end="")
    print("+")
    for i in array_int:
        print("|", end="")
        for j in i:
            if j == 0:
                print(" ", end="")
            else:
                print(j, end="")
        print("|")
    print("+", end="")
    for _ in range(array_int.shape[0]):
        print("-", end="")
    print("+")


def calculate_cost(array):
    print_array(array)
    labeled_array, num_features = label(array)
    cost = 0
    for region_label in range(1, num_features + 1):
        region = (labeled_array == region_label)
        area = np.sum(region)

        padded = np.pad(region, pad_width=1, mode="constant", constant_values=False)
        # boundary = (
        #     (padded & ~np.roll(padded, shift=1, axis=0)) |
        #     (padded & ~np.roll(padded, shift=-1, axis=0)) |
        #     (padded & ~np.roll(padded, shift=1, axis=1)) |
        #     (padded & ~np.roll(padded, shift=-1, axis=1))
        # )
        edges = [
                padded & ~np.roll(padded, shift=-1, axis=0),
                padded & ~np.roll(padded, shift=1, axis=0),
                padded & ~np.roll(padded, shift=-1, axis=1),
                padded & ~np.roll(padded, shift=1, axis=1)
                ]

        sides = 0
        for i in edges:
            for j in i:


        # boundary_points = np.argwhere(boundary)
        # visited = set()
        # current_point = tuple(boundary_points[0])  # Start at the first boundary point
        # directions = []
        # moves = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        # while current_point not in visited:
        #     visited.add(current_point)
        #     for d_idx, move in enumerate(moves):
        #         next_point = (current_point[0] + move[0], current_point[1] + move[1])
        #         if next_point in map(tuple, boundary_points):
        #             if len(directions) == 0 or directions[-1] != d_idx:
        #                 directions.append(d_idx)
        #             current_point = next_point
        #             break

        region_cost = area * sides
        cost += region_cost

        print(f"Region {region_label}: Area = {area}, Sides = {sides}, Cost = {region_cost}")

    return cost


total_cost = 0
for i in plants:
    print(i)
    plots = (plot_map == i)
    total_cost += calculate_cost(plots)

print(f"Part Two: {total_cost}")


