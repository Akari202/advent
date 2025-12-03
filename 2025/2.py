from logging import debug

from aoc import puzzle

# puzzle.test_answer_one = 1227775554
# puzzle.test_answer_two = 4174379265
data = puzzle.csv_lines()[0]

count = 0
for i in data:
    split = [int(i) for i in i.split("-")]
    for j in range(split[0], split[1] + 1):
        j_str = str(j)
        j_len = len(j_str)
        if j_len % 2 != 0:
            continue
        mid = j_len // 2
        debug(f"{j = } | {j_len = } | {mid = } | {j_str[:mid] = } | {j_str[mid:] = }")
        if j_str[:mid] == j_str[mid:]:
            count += j

puzzle.submit_one(count)


count = 0
for i in data:
    split = [int(i) for i in i.split("-")]
    for j in range(split[0], split[1] + 1):
        j_str = str(j)
        j_len = len(j_str)
        for k in range(j_len):
            if k != 0 and j_len % k != 0:
                continue
            sub = j_str[:k]
            comp = ""
            if k == 0:
                repeats = j_len
            else:
                repeats = j_len // k
            for _ in range(repeats):
                comp += sub
            if comp == j_str:
                count += j
                debug(f"{j = } | {j_len = } | {k = } | {sub = } | {comp = }")
                break

puzzle.submit_two(count)
