from logging import debug

from aoc import puzzle

# puzzle.test_answer_one = 3
# puzzle.test_answer_two = 6
data = puzzle.lines()

dial_position = 50
count = 0
for i in data:
    direction = i[:1]
    distance = int(i[1:])
    if direction == "L":
        dial_position = (((dial_position - distance) % 100) + 100) % 100
    elif direction == "R":
        dial_position = (((dial_position + distance) % 100) + 100) % 100

    debug(f"{dial_position = } | {direction = } | {distance = }")
    if dial_position == 0:
        count += 1

puzzle.submit_one(count)

dial_position = 50
count = 0
for i in data:
    direction = i[:1]
    distance = int(i[1:])
    count += distance // 100
    distance %= 100
    if direction == "L":
        if dial_position - distance <= 0 and dial_position != 0:
            count += 1
        dial_position = (((dial_position - distance) % 100) + 100) % 100
    elif direction == "R":
        if dial_position + distance >= 100:
            count += 1
        dial_position = (((dial_position + distance) % 100) + 100) % 100

    debug(f"{dial_position = } | {direction = } | {distance = } | {count = } | {i = }")

puzzle.submit_two(count)
