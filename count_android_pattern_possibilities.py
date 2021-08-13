#!/usr/bin/env python3
import functools
import multiprocessing
"""
Returns the number of possible combinations for patterns of a certain length
with a certain grid size.
"""

functools.lru_cache(maxsize=None)


def next_steps(size, i_init, j_init):
    assert size >= 2
    i_pos = [i_init - 1, i_init, i_init + 1]
    j_pos = [j_init - 1, j_init, j_init + 1]
    all_pos = set()
    for i in i_pos:
        if i < 0 or size <= i:
            continue
        for j in j_pos:
            if i == i_init and j == j_init:
                continue
            if j < 0 or size <= j:
                continue
            all_pos.add((i, j))
    return all_pos


# functools.lru_cache(maxsize=None)
def count(current_state, size, remaining_length, i, j, current_length):
    # count how many paths there are starting from i,j with this remaining length
    if remaining_length <= 1:
        return remaining_length

    s = 0
    for new_pos in next_steps(size, i, j):
        new_state = current_state.copy()
        if new_pos not in new_state:
            new_state[new_pos] = True
            i, j = new_pos
            s += count(new_state, size, remaining_length -
                       1, i, j, current_length + 1)

    return s


def run_with_starting_pos(length, size, i, j):
    current_state = dict()
    current_state[(i, j)] = True
    return count(current_state, size, length, i, j, 0)


def main(size=3, length=3):
    args = [(length, size, i, j) for i in range(size) for j in range(size)]
    with multiprocessing.Pool() as p:
        return sum(p.starmap(run_with_starting_pos, args))


if __name__ == '__main__':
    # XXX: plot the patterns in the terminal
    import time
    import cProfile
    import pstats
    import io
    pr = cProfile.Profile()
    pr.enable()

    # as a reference
    print(2 ** 80)
    print(26 ** 18)

    start_time = time.time()

    for i_length in range(1, 10):
        print("For length: " + str(i_length))
        print(main(size=6, length=i_length))


    print("--- %s seconds ---" % (time.time() - start_time))
    pr.disable()
