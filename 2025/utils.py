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
