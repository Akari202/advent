from functools import cache
from logging import debug

from aoc import puzzle
from utils import Node

# puzzle.test_answer_one = 5
# puzzle.test_answer_two = 2
data = puzzle.lines()

devices: dict[str, list[str]] = {}
for i in data:
    split = i.split(": ")
    name = split[0]
    subs = split[1].split(" ")
    devices[name] = subs


class WireNode(Node):
    def __init__(self, name: str, depth: int = 0):
        super().__init__(name)
        if self.value == end:
            global count
            count += 1
        elif self.value != "out" and depth < 19:
            self.add_children(depth)

    def add_children(self, depth: int):
        for i in devices[self.value]:
            if i != start:
                self.children.append(WireNode(i, depth=depth + 1))


count = 0
start = "you"
end = "out"
tree = WireNode(start)
if puzzle.is_test():
    debug(f"tree = \n{tree}")
debug(f"{count = }")
puzzle.submit_one(count)

if puzzle.is_test():
    with open("2025/data/11 test 2", "r") as file:
        data = [i.strip() for i in file.readlines()]

    devices: dict[str, list[str]] = {}
    for i in data:
        split = i.split(": ")
        name = split[0]
        subs = split[1].split(" ")
        devices[name] = subs

# dot -Tpng '.\2025\data\11 graph.dot' > '.\2025\data\11 graph.png'
graph_file = puzzle.path.parent / "data" / "11 graph.dot"
if not graph_file.exists():
    output = 'digraph G {\nfft [style="filled", fillcolor="blue"];\ndac [style="filled", fillcolor="blue"];\nout [style="filled", fillcolor="red"];\nsvr [style="filled", fillcolor="green"];\nyou [style="filled", fillcolor="lightgreen"];'
    for i in devices.keys():
        for j in devices[i]:
            output += f"\n    {i} -> {j};"
    output += "\n}\n"
    with open(graph_file, "w") as file:
        file.write(output)

# sequences = [("svr", "fft"), ("fft", "dac"), ("dac", "out")]
# count = 1
# for i in sequences:
#     visits = {}
#     visits[i[0]] = count
#     done = False
#     while not done:
#         debug(visits)
#         keys = list(visits.keys())
#         skip = False
#         for j in keys:
#             base = visits.pop(j)
#             if j == i[1]:
#                 count = base
#                 debug(
#                     f"{i[0]} to {i[1]} has {base} paths for a total of {count} possible paths"
#                 )
#                 done = True
#                 break
#             for k in devices[j]:
#                 visits[k] = base + visits.get(k, 0)
#
# debug(count)
# puzzle.submit_two(count)


@cache
def recurse(name: str, fft: bool, dac: bool) -> int:
    if name == end:
        if fft and dac:
            return 1
        else:
            return 0
    else:
        count = 0
        for i in devices[name]:
            count += recurse(i, fft or name == "fft", dac or name == "dac")
        return count


start = "svr"
end = "out"
count = recurse(start, False, False)
debug(f"{count = }")
puzzle.submit_two(count)
