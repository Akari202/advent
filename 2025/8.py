from logging import debug
from math import prod
from operator import itemgetter

from aoc import puzzle
from scipy.cluster.hierarchy import DisjointSet
from vec_utils_py import Vec3d, VecList

# puzzle.test_answer_one = 40
# puzzle.test_answer_two = 25272
data = [Vec3d(*i) for i in puzzle.csv_values()]
if puzzle.is_test():
    connections = 10
else:
    connections = 1000

length = len(data)
debug(f"{length = }")
sets = DisjointSet(data)
lists = []
for i, j in enumerate(data):
    vec_list = VecList(data[:i] + data[i + 1 :])
    distances = vec_list.distance_to(j)
    for k in zip(distances, vec_list):
        lists.append([k[0], j, k[1]])
        # debug(f"{j} | {k[0]} | distance = {k[1]}")


debug(f"{len(lists) = }")
lists.sort(key=itemgetter(0))
connected = []
iterator = iter(lists)
for _ in range(connections):
    while (
        (i := next(iterator)) is not None
        and not tuple(i[1:]) in connected
        and not sets.merge(*i[1:])
    ):
        connected.append((i[1], i[2]))
        connected.append((i[2], i[1]))
    subsets = [len(i) for i in sets.subsets()]
    subsets.sort(reverse=True)
    debug(subsets)
# iterator = iter(lists)
# for _ in range(connections):
#     while (i := next(iterator)) is not None and not sets.merge(*i[1:]):
#         pass
#     subsets = [len(i) for i in sets.subsets()]
#     subsets.sort(reverse=True)
#     debug(subsets)

debug(sets.subsets())
sizes = [len(i) for i in sets.subsets()]
sizes.sort()
puzzle.submit_one(prod(sizes[-3:]))

for i in iterator:
    if sets.merge(*i[1:]) and len(sets.subsets()) == 1:
        last = i

puzzle.submit_two(int(last[1].x * last[2].x))
