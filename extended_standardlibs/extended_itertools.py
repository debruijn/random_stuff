from itertools import pairwise
from collections import deque


def pairwise_py(iterable):
    # pairwise('ABCDEFG') → AB BC CD DE EF FG
    iterator = iter(iterable)
    a = next(iterator, None)
    for b in iterator:
        yield a, b
        a = b


def n_wise(iterable, n=2):
    # n_wise('ABCDEFG', n=3) → ABC BCD CDE DEF EFG
    iterator = iter(iterable)
    a = tuple(next(iterator, None) for _ in range(n-1))

    for b in iterator:
        yield *a, b
        a = a[1:] + (b,)


def n_wise_dq(iterable, n=2):
    # n_wise_dq('ABCDEFG', n=3) → ABC BCD CDE DEF EFG
    iterator = iter(iterable)
    a = deque(next(iterator, None) for _ in range(n-1))

    for b in iterator:
        yield *a, b
        a.popleft()
        a.append(b)


def n_wise_idx(indexable, n=3):
    for i in range(len(indexable) - 3):
        yield tuple([x for x in indexable[i:i+n]])


if __name__ == "__main__":

    # TODO: This should be a list of tests and benchmarks

    test = 'ABCDEFG'

    print(list(pairwise(test)))
    print(list(pairwise_py(test)))
    print(list(n_wise(test, 2)))

    print(list(n_wise(test, 3)))
    print(list(n_wise(test, 4)))

    print(list(n_wise(test, 10)))

    print(list(n_wise_dq(test, 4)))
    print(list(n_wise_idx(test, 4)))


    import time
    import random

    test_long = [random.randint(0, 100) for _ in range(100000)]

    before = time.time_ns()
    list(pairwise(test_long))
    after1 = time.time_ns()
    list(pairwise_py(test_long))
    after2 = time.time_ns()
    list(n_wise(test_long, 2))
    after3 = time.time_ns()
    list(n_wise(test_long, 3))
    after4 = time.time_ns()
    list(n_wise(test_long, 10))
    after5 = time.time_ns()
    list(n_wise_dq(test_long, 2))
    after6 = time.time_ns()
    list(n_wise_dq(test_long, 3))
    after7 = time.time_ns()
    list(n_wise_dq(test_long, 10))
    after8 = time.time_ns()
    list(n_wise_idx(test_long, 10))
    after9 = time.time_ns()

    print(after1 - before, after2 - after1, after3 - after2, after4 - after3, after5 - after4, after6 - after5,
          after7 - after6, after8 - after7, after9 - after8)
