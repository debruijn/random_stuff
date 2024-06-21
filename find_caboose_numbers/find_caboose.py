# This script aims to describe Caboose numbers, or better, how much numbers meet the Caboose property
# For background, see this Numberphile video: https://www.youtube.com/watch?v=gM5uNcgn2NQ

# (Also known as Euler's lucky numbers, but that is less fun. See https://en.wikipedia.org/wiki/Lucky_numbers_of_Euler)

N = 60  # Max number to check
run_to_N = False  # Whether to run k from 1 to n or from 1 to N, for each n  TODO


def is_prime(x):
    # TODO: actually make a prime function; either use sympy package or create own function
    if x in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59):
        return True
    return False


counts = []
for n in range(1, N+1):
    counts.append(sum([is_prime(k**2 - k + n) for k in range (1, n)]))
    if counts[n-1] == n-1:
        print(f'Caboose number found: {n}!')


