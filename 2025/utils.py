from typing import Optional

import numpy as np


LETTERS = [x for x in "abcdefghijklmnopqrstuvwxyz"]
VOWELS = {"a", "e", "i", "o", "u"}
CONSONANTS = set(x for x in LETTERS if x not in VOWELS)


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
