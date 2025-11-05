from tqdm import tqdm

with open("9 input", "r") as file:
    filesystem_map = file.readline().replace("\n", "0")

filesystem = [[int(filesystem_map[i]), int(filesystem_map[i + 1]), int(i / 2)] for i in range(0, len(filesystem_map), 2)]
filesystem_map = []
for i in filesystem:
    id = i[2]
    for j in range(i[0]):
        filesystem_map.append(id)
    for k in range(i[1]):
        filesystem_map.append(".")

length = len(filesystem_map)
last = length - 1
for i in range(length):
    # print(filesystem_map)
    # print(i)
    # print(filesystem_map[i])
    # print(last)
    # print(filesystem_map[last])
    if filesystem_map[i] == ".":
        while True:
            if isinstance(filesystem_map[last], int):
                filesystem_map[last], filesystem_map[i] = filesystem_map[i], filesystem_map[last]
                break
            else:
                last -= 1
    if i >= last:
        filesystem_map[last], filesystem_map[i] = filesystem_map[i], filesystem_map[last]
        # print(filesystem_map[i - 10:i + 10])
        break

# print(filesystem_map)
# print(f"{filesystem_map[:15]}...{filesystem_map[-15:]}")

checksum = 0
for i, j in enumerate(filesystem_map):
    if j == ".":
        pass
        # break
    else:
        # print(j, end="")
        checksum += j * i
# print("")

print(f"Part One: {checksum}")
# print(checksum - 6519155389266)

def prind_filesystem(filesystem, do_print=True):
    filesystem_map = []
    for i in filesystem:
        id = i[2]
        for j in range(i[0]):
            filesystem_map.append(id)
        for k in range(i[1]):
            filesystem_map.append(".")
    if do_print:
        for i, j in enumerate(filesystem_map):
            print(j, end="")
        print("\n")
    return filesystem_map


# print(filesystem)

length = len(filesystem)
max_id = length
fudge = 0
for i in tqdm(range(length)):
    index = length - i - 1 + fudge
    entry = filesystem[index]
    size = entry[0]
    # print(f"{i} -> {index}: {entry}")
    for j, k in enumerate(filesystem):
        if k[1] >= size and j < index:
            # print(f"Inserting at {j}")
            filesystem[index - 1][1] += entry[1] + entry[0]
            entry[1] = k[1] - size
            k[1] = 0
            filesystem.pop(index)
            filesystem.insert(j + 1, entry)
            fudge += 1
            break
    # print(filesystem)
    # prind_filesystem(filesystem)

    # if i > 3:
        # break

filesystem_map = prind_filesystem(filesystem, do_print=False)

checksum = 0
for i, j in enumerate(filesystem_map):
    if j != ".":
        checksum += j * i

print(f"Part Two: {checksum}")
