# This video replicates constructing the Twin Primes that meet the Goldbach Conjecture, based on the Numberphile video
# https://www.youtube.com/watch?v=Gojd8mTl3Do
# Next to this, it constructs a list for each number how many options there are to use twin primes.
from itertools import pairwise, combinations_with_replacement


def get_primes(N):
    primes = []
    for num in range(2, N + 1):
        for i in range(2, int(num ** 0.5) + 2):
            if (num % i) == 0:
                break
        else:
            primes.append(num)
    return primes


def get_twin_primes(N):
    primes = get_primes(N)
    twin_primes = set()
    for i, j in pairwise(primes):
        if j - i == 2:
            twin_primes.update({i, j})
    return twin_primes


def main(N):

    nr_twin_primes = []
    twin_primes = get_twin_primes(N)
    exceptions = []

    for n in range(2, N, 2):
        this_twins = [x for x in twin_primes if x < n]
        this_count = 0
        for i, j in combinations_with_replacement(this_twins, 2):
            if i + j == n:
                this_count += 1
        nr_twin_primes.append(this_count)
        if this_count == 0:
            exceptions.append(n)

    return nr_twin_primes, exceptions


if __name__ == "__main__":
    N = 5000  # There are no known exceptions above 5000
    nr_twin_primes, exceptions = main(N)
    print(f'Number of exceptions up until {N}: {len(exceptions)}')
    print(nr_twin_primes)

    # Potential next steps in case I am interested:
    # - graph of n vs nr_twin_primes (incl smoothed fit, perhaps a Neural Network mean/var estimation?)
    # - graph of n vs nr_twin_primes/n or n vs nr_twin_primes/nr_primes to show if that converges somehow

    # It would be cool to use some model to form a (parametrized?) specification of the probability that there are no
    # exceptions for a given n, convert that into a cumulative statement starting from n=10000000 or whatever, and show
    # that this cumulative probability does not converge to 1 but a lower value, which shows that this specification
    # would imply that indeed it is possible (and based on the probability limit, perhaps even likely) that there are no
    # more exceptions outside the 35 that are known.
