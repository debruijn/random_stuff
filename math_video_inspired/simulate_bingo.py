# This script aims to simulate the probability that the 1st winning line in Bingo is horizontal, for different sizes of
# participant groups. This is inspired by the "infinite size" calculations in the Standupmaths video TODO

import random

size_grid = 5
nrs_per_col = 15
center_is_free = False

nr_participants = 100
nr_replications = 1000

count_win = [0, 0, 0]  # Horizontal, vertical, diagonal


class BingoGrid:

    def __init__(self, size=5, center_free=True, nrs_per_col=15):
        self.size = size
        self.nr_col = nrs_per_col
        self.grid = [random.sample(range(self.nr_col*i, self.nr_col*(i+1)), self.size) for i in range(self.size)]

        self.checked = [[False]*self.size for _ in range(self.size)]
        if center_free:
            self.checked[(self.size-1)//2][(self.size-1)//2] = True

    def check_num(self, num):
        which_j = [self.grid[i].index(num) if num in self.grid[i] else -1 for i in range(self.size)]
        which_i = [x>=0 for x in which_j].index(True) if any([x>=0 for x in which_j]) else -1
        if which_i >= 0:
            self.checked[which_i][which_j[which_i]] = True
            return self.check_winner()
        return -1

    def check_winner(self):
        if any(all(x) for x in self.checked):
            return 1
        if any(all([self.checked[j][i] for j in range(self.size)]) for i in range(self.size)):
            return 0
        if all(self.checked[i][i] for i in range(self.size)):
            return 2
        if all(self.checked[i][self.size-i-1] for i in range(self.size)):
            return 2
        return -1


for _ in range(nr_replications):

    # Simulate bingo cards for each participant
    cards = [BingoGrid(center_free=center_is_free) for _ in range(nr_participants)]

    # Randomly order the nums drawn
    nums = list(range(nrs_per_col*size_grid))
    random.shuffle(nums)

    while len(nums) > 0:
        this_num = nums.pop()
        check = [x.check_num(this_num) for x in cards]
        if any(x >= 0 for x in check):
            which = [x >= 0 for x in check].index(True)
            count_win[check[which]] += 1
            break

print(count_win)
