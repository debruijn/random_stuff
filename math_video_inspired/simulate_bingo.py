# This script aims to simulate the probability that the 1st winning line in Bingo is horizontal, for different sizes of
# participant groups. This is inspired by the "infinite size" calculations in the Standupmaths video:
# https://www.youtube.com/watch?v=AHP1T8fTxpQ

import random
from functools import cache
from itertools import chain, islice
from collections import Counter
from parfor import pmap

size_grid = 5
nrs_per_col = 15
center_is_free = False
nr_replications = 10000
track_diagonal_wins = False
run_parallel = True


def check_num(checked, grid, num):
    for i, x in enumerate(grid):
        if x == num:
            return checked + 2**i
    return checked


def batched(iterable, n):
    iterator = iter(iterable)
    while batch := tuple(islice(iterator, n)):
        yield batch

@cache
def check_winner(checked):
    bin_checked = bin(checked)[2:].zfill(25)
    if sum(x == "1" for x in bin_checked) < 5:
        return -1

    if any([all(y=='1' for y in x) for x in batched(bin_checked, 5)]):
        return 1
    if any([all(y=='1' for y in islice(bin_checked, i, None, 5)) for i in range(5)]):
        return 0
    if track_diagonal_wins:
        if all(x=='1' for x in islice(bin_checked, 0, None, 6)):
            return 2
        if all(x=='1' for x in islice(bin_checked, 4, 21, 4)):
            return 2

    return -1


def run_bingo(i=0, nr_participants=10):
    # Simulate bingo cards for each participant
    cards = [list(chain(*[random.sample(range(nrs_per_col * i, nrs_per_col * (i + 1)), size_grid) for i in range(size_grid)]))
             for _ in range(nr_participants)]
    if center_is_free:
        for card in cards:
            card[12] = -1
    checks = [2**12 if center_is_free else 0 for _ in range(nr_participants)]

    # Randomly order the nums drawn
    nums = list(range(nrs_per_col*size_grid))
    random.shuffle(nums)

    for this_num in nums:
        checks = [check_num(checks[i], cards[i], this_num) for i in range(len(cards))]
        check_victory = [check_winner(x) for x in checks]
        if any(x >= 0 for x in check_victory):
            which = [x >= 0 for x in check_victory].index(True)
            return check_victory[which]


if __name__ == "__main__":
    import time

    for nr_p in [10, 100, 1000, 10000]:
        ts = time.time()
        if run_parallel:
            type_win = pmap(fun=run_bingo, iterable=range(nr_replications), args=(nr_p,))
        else:
            type_win = [run_bingo() for _ in range(nr_replications)]
        te = time.time()
        print(f'\nRuntime for {nr_p} participants: {te - ts:2.4f} sec')
        counter_win = Counter(type_win)
        print(f'Horizontal wins: {counter_win[0]}, vertical wins: {counter_win[1]}, diagonal wins: {counter_win[2]})\n')

    print(f"According to the video, this should converge to 73.7% vs 26.3% for when each possible bingo card has been"
          f"handed out.")
