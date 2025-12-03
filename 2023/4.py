import re

from aoc import puzzle

# puzzle.test_answer_one = 13
# puzzle.test_answer_two = 30

data = puzzle.lines()

card_re = re.compile(r"Card .*: (.*) \| (.*)$")
total = 0
for i in data:
    match = card_re.search(i)
    assert match is not None
    winning = match.group(1).split()
    have = match.group(2).split()
    count = 0
    for i in have:
        if i in winning:
            count += 1
    # print(f"{winning=} | {have=} | {count=}")
    if count > 0:
        total += 2 ** (count - 1)

puzzle.submit_one(total)


card_re = re.compile(r"Card .*: (.*) \| (.*)$")
counts: list[int] = []
for i in data:
    match = card_re.search(i)
    assert match is not None
    winning = match.group(1).split()
    have = match.group(2).split()
    count = 0
    for i in have:
        if i in winning:
            count += 1
    counts.append(count)

copies = [1] * len(counts)
for i, j in enumerate(counts):
    current_count = copies[i]
    for k in range(i + 1, i + 1 + j):
        copies[k] += current_count

puzzle.submit_two(sum(copies))
