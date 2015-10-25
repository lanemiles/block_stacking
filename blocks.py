import sys


def can_stack(top, bottom):
    return (top[0] < bottom[0]) and (top[1] < bottom[1])


def good_perms(lst):
    mega_list = []
    for block in lst:
        permutations = perms(block)
        for perm in permutations:
            if perm[0] <= perm[1] and perm not in mega_list:
                mega_list.append(perm)
    return mega_list


def perms(lst):

    # first, create all perms
    if len(lst) == 1:
        return [lst]

    output = []
    first = lst[0]
    rest = perms(lst[1:])
    for perm in rest:
        length = len(perm)
        for i in range(0, length+1):
            output.append(perm[0:i] + [first] + perm[i:])

    # now, remove when fist val is > second value
    return output


def parse_input_file(path):
    block_types = []

    with open(path, 'r') as input_file:
        input_list = input_file.readlines()

        for index, value in enumerate(input_list[1:]):
            block_types.append(value.replace("\n", "").split(" "))
            block_types[index] = [int(block_types[index][0]), int(block_types[index][1]), int(block_types[index][2])]

    return block_types


def main():
    infile = sys.argv[1]
    outfile = sys.argv[2]

    block_types = parse_input_file(infile)
    block_perms = good_perms(block_types)

    # sort list based on area
    block_perms.sort(key=lambda x: x[0] * x[1], reverse=True)

    # begin dynamic programming
    blocks = []
    path = []
    temp_height = []

    # base case
    blocks.append((block_perms[0][2], None))

    # fill in rest of table
    for i in range(1, len(block_perms)):

        # for all lesser blocks, if stackable, compute total height if stacked
        for q in range(0, i):

            if can_stack(block_perms[i], block_perms[q]):
                temp_height.append((blocks[q][0] + block_perms[i][2], q))
            elif block_perms[i][2] not in temp_height:
                temp_height.append((block_perms[i][2], None))

        # pick the maximum total height
        max_height = max(temp_height, key=lambda x: x[0])
        temp_height = []
        blocks.append(max_height)

    # get max tower height
    (max_tower_height, below_block_index) = max(blocks, key=lambda x: x[0])

    # get top block's index
    cur_block_index = blocks.index((max_tower_height, below_block_index))

    # build up path
    while cur_block_index is not None:
        path.append(cur_block_index)
        cur_block_index = blocks[cur_block_index][1]

    # print descriptive sentence
    print "The tallest tower has", len(path), "blocks and a height of", max_tower_height

    # print to output file
    with open(outfile, 'w') as output:

        # print number of blocks
        output.write(str(len(path)) + "\n")

        # print out blocks in path
        for x in reversed(path):
            to_print = ""
            for dim in block_perms[x]:
                to_print += str(dim) + " "
            to_print = to_print[:-1] + "\n"
            output.write(to_print)


main()
