# This script checks if an individual is divisible by 7, in the Numberphile way
# (see https://www.youtube.com/watch?v=Ki-M1DJIZsk)
from functools import cache


def check_divisible_by_7(number, return_remainder=False):
    mapping = [0, 3, 6, 2, 5, 1, 4]
    mapping2 = [0, 1, 2, 3, 4, 5, 6, 0, 1, 2, 3, 4, 5, 6, 0, 1, 2, 3, 4, 5, 6]

    loc = 0
    for digit in str(number)[:-1]:
        loc += int(digit)
        loc = mapping[mapping2[loc]]
    loc = mapping2[loc + int(str(number)[-1])]

    return loc if return_remainder else loc == 0


numbers = [7, 14, 140, 392, 1234, 3929, 123123, 891723987123, 891723987126, 90182734981274987123987123987123]
for number in numbers:
    print(f'{number}: {check_divisible_by_7(number), check_divisible_by_7(number, return_remainder=True)}')


@cache
def make_mapping(divisor):
    mapping = [divmod(10 * x, divisor)[1] for x in range(divisor)]
    mapping2 = [*range(divisor)] * 3
    return mapping, mapping2


def check_divisible_by_k(number, k=7, return_remainder=False):

    mapping, mapping2 = make_mapping(k)
    loc = 0
    for digit in str(number)[:-1]:
        loc += int(digit)
        loc = mapping[mapping2[loc]]
    loc = mapping2[loc + int(str(number)[-1])]

    return loc if return_remainder else loc == 0


numbers = [7, 14, 140, 392, 1234, 3933, 123123, 891723987123, 891723987126, 90182734981274987123987123987128]
try_k = [7, 13, 31, 43, 117]
for k in try_k:
    print(f'\nRunning for divisor {k}:')
    for number in numbers:
        print(f'{number}: {check_divisible_by_k(number, k), check_divisible_by_k(number, k, return_remainder=True)}')

