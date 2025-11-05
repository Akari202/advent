import numpy as np

with open("10 input") as file:
    topo_map = np.array([[int(i) for i in row.replace("\n", "")] for row in file])


def trailhead_score(topo_map, m, n, past):
    shape = topo_map.shape
    if m < 0 or n < 0 or m >= shape[0] or n >= shape[1]:
        return set()
    fresh = topo_map[m][n]
    difference = fresh - past
    if difference != 1:
        return set()
    elif fresh == 9:
        peaks = {(int(m), int(n))}
        return peaks
    else:
        peaks = set()
        peaks.update(trailhead_score(topo_map, m + 1, n, fresh))
        peaks.update(trailhead_score(topo_map, m - 1, n, fresh))
        peaks.update(trailhead_score(topo_map, m, n + 1, fresh))
        peaks.update(trailhead_score(topo_map, m, n - 1, fresh))
        return peaks


total_score = 0
trailheads = np.where(topo_map == 0)
for i in range(len(trailheads[0])):
    m = trailheads[0][i]
    n = trailheads[1][i]
    # print(f"({trailheads[0][i]}, {trailheads[1][i]}) => {topo_map[m][n]}")
    trailhead_peaks = trailhead_score(topo_map, m, n, -1)
    total_score += len(trailhead_peaks)

print(f"Part One: {total_score}")


def trailhead_score(topo_map, m, n, past):
    shape = topo_map.shape
    if m < 0 or n < 0 or m >= shape[0] or n >= shape[1]:
        return []
    fresh = topo_map[m][n]
    difference = fresh - past
    if difference != 1:
        return []
    elif fresh == 9:
        return [(int(m), int(n))]
    else:
        peaks = []
        peaks.extend(trailhead_score(topo_map, m + 1, n, fresh))
        peaks.extend(trailhead_score(topo_map, m - 1, n, fresh))
        peaks.extend(trailhead_score(topo_map, m, n + 1, fresh))
        peaks.extend(trailhead_score(topo_map, m, n - 1, fresh))
        return peaks


total_score = 0
trailheads = np.where(topo_map == 0)
for i in range(len(trailheads[0])):
    m = trailheads[0][i]
    n = trailheads[1][i]
    trailhead_peaks = trailhead_score(topo_map, m, n, -1)
    total_score += len(trailhead_peaks)

print(f"Part Two: {total_score}")

