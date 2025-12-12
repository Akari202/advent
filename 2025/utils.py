import itertools
from collections.abc import Generator, Iterable, Iterator
from logging import error
from typing import Any, Optional

import numpy as np
from numpy._typing import NDArray


LETTERS = [x for x in "abcdefghijklmnopqrstuvwxyz"]
VOWELS = {"a", "e", "i", "o", "u"}
CONSONANTS = set(x for x in LETTERS if x not in VOWELS)


class Node:
    def __init__(self, value: str):
        self.children: list[Node] = []
        self.value: str = value

    def __str__(self, level: int = 0) -> str:
        out = f"{"⋮ " * level}{self.value}\n"
        for child in self.children:
            out += child.__str__(level + 1)
        return out

    def __iter__(self) -> Iterator[Node]:
        return iter(self.children)

    def depth_first(self) -> Generator[Node]:
        yield self
        for i in self:
            yield from i.depth_first()

    def is_leaf(self) -> bool:
        return len(self.children) == 0


def expand(
    index: tuple[int, int],
    shape: Optional[tuple[int, int]] = None,
    center: bool = False,
) -> list[tuple[int, int]]:
    values: list[tuple[int, int]] = [
        i
        for i in [
            (index[0] - 1, index[1] - 1),
            (index[0] - 1, index[1] + 0),
            (index[0] - 1, index[1] + 1),
            (index[0] + 0, index[1] - 1),
            (index[0] + 0, index[1] + 1),
            (index[0] + 1, index[1] - 1),
            (index[0] + 1, index[1] + 0),
            (index[0] + 1, index[1] + 1),
        ]
        if min(i) >= 0 and not (shape is not None and min(np.subtract(shape, i)) < 1)
    ]

    if center:
        values.append(index)
    return values


def get_polygon_centroid_area(points: list[list[int]]) -> tuple[tuple[int, int], float]:
    x = [p[0] for p in points]
    y = [p[1] for p in points]
    x.append(points[0][0])
    y.append(points[0][1])
    area = 0
    Cx = 0
    Cy = 0
    for i in range(len(points)):
        step = x[i] * y[i + 1] - x[i + 1] * y[i]
        area += step
        Cx += (x[i] + x[i + 1]) * step
        Cy += (y[i] + y[i + 1]) * step
    area *= 0.5
    Cx /= 6.0 * area
    Cy /= 6.0 * area
    return ((Cx, Cy), abs(area))


def generate_combos(values: Iterable[Any], max: int = 10) -> Generator[tuple[Any]]:
    depth = 0
    while depth < max:
        depth += 1
        for i in itertools.product(values, repeat=depth):
            yield i


def print_bool_array(array: NDArray):
    for i in array:
        for j in i:
            if j:
                print("#", end="")
            else:
                print(".", end="")
        print("")


def parse_bool(value: str) -> bool:
    match value:
        case "#":
            return True
        case ".":
            return False
        case _:
            error(f"Unexpected value parsed to bool: {value}")
            return False
