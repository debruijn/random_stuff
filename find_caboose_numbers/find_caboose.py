# This script aims to describe Caboose numbers, or better, how much numbers meet the Caboose property
# For background, see this Numberphile video: https://www.youtube.com/watch?v=gM5uNcgn2NQ

# (Also known as Euler's lucky numbers, but that is less fun. See https://en.wikipedia.org/wiki/Lucky_numbers_of_Euler)

from functools import cache

N = 200  # Max number to check
run_to_N = False  # Whether to run k from 1 to n or from 1 to N, for each n. Use False for the traditional definition.


@cache
def is_prime(x):
    for k in range(2, int(x**0.5)+1):
        if x/k == int(x/k):
            return False
    return True


counts = [0, 0]
found_any = False
for n in range(2, N+1):
    counts.append(sum([is_prime(k**2 - k + n) for k in range(1, N if run_to_N else n)]))
    if counts[n] == n-1:
        if not found_any:
            print('Caboose number found: ')
            found_any = True
        print(f'{n}')

near_hits = {i: counts[i]/(i-1) for i in range(2, n) if 0.5 < counts[i]/(i-1) < 1}
print('\nNumbers close to being Caboose:')
[print(f'{k} with {v*100:.2f}%') for k, v in near_hits.items()]
