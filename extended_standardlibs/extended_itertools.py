import copy
import functools
from functools import partial
from itertools import pairwise, permutations, cycle
from collections import deque, defaultdict, Counter
from unittest import TestCase


def pairwise_py(iterable):
    # pairwise('ABCDEFG') → AB BC CD DE EF FG
    iterator = iter(iterable)
    a = next(iterator, None)
    for b in iterator:
        yield a, b
        a = b


def n_wise_alt(iterable, n=2):

    iterator1 = iter(iterable)
    iterator2 = iter(iterable)
    for _ in range(2):
        next(iterator2)
    for a in pairwise(iterator1):
        print(a, next(iterator2))
        # yield a, next(iterator2)
    # To experiment with, this can work for n=3?


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


def permutations_ref(iterable, r=None):
    # permutations('ABCD', 2) → AB AC AD BA BC BD CA CB CD DA DB DC
    # permutations(range(3)) → 012 021 102 120 201 210

    pool = tuple(iterable)
    n = len(pool)
    r = n if r is None else r
    if r > n:
        return

    indices = list(range(n))
    cycles = list(range(n, n-r, -1))
    yield tuple(pool[i] for i in indices[:r])

    while n:
        for i in reversed(range(r)):
            cycles[i] -= 1
            if cycles[i] == 0:
                indices[i:] = indices[i+1:] + indices[i:i+1]
                cycles[i] = n - i
            else:
                j = cycles[i]
                indices[i], indices[-j] = indices[-j], indices[i]
                yield tuple(pool[i] for i in indices[:r])
                break
        else:
            return


def derangements_range(n):
    """Yield successive distinct derangements of the range up to *n*.

        >>> sorted(derangements_range(3))
        [(1, 2, 0), (2, 0, 1)]

    Ignoring output order, this is equal to but significantly faster
    than ``derangements(range(n))``.

    """
    if n == 2:
        yield 1, 0
    elif n <= 1:
        yield from []
    else:
        lag1 = derangements_range(n - 1)
        for lag in lag1:
            for split in range(len(lag)):
                yield lag[0:split] + (n - 1,) + lag[split + 1 :] + (
                    lag[split],
                )

        lag2 = derangements_range(n - 2)
        for lag in lag2:
            yield lag + (n - 1, n - 2)
            for k in range(n - 3, -1, -1):
                i = lag.index(k)
                lag = lag[:i] + (k + 1,) + lag[i + 1 :]
                yield lag[:k] + (n - 1,) + lag[k:] + (k,)


def derangements_fast(iterable, r=None, by_index=True):
    """Yield successive derangements of the elements in *iterable*.

    A derangement is a permutation in which no element appears at its original
    index. Suppose Alice, Bob, Carol, and Dave are playing Secret Santa.
    The code below outputs all of the different ways to assign gift recipients
    such that nobody is assigned to himself or herself:

        >>> for d in derangements(['Alice', 'Bob', 'Carol', 'Dave']):
        ...    print(', '.join(d))
        Bob, Alice, Dave, Carol
        Bob, Carol, Dave, Alice
        Bob, Dave, Alice, Carol
        Carol, Alice, Dave, Bob
        Carol, Dave, Alice, Bob
        Carol, Dave, Bob, Alice
        Dave, Alice, Bob, Carol
        Dave, Carol, Alice, Bob
        Dave, Carol, Bob, Alice

    For numeric inputs, the input *by_index* can be used to either restrict by
    original input index, or by value of the element

        >>> sorted(derangements([1, 0, 2]))
        [(0, 2, 1), (2, 1, 0)]
        >>> sorted(derangements([0, 1, 2], by_index=False))
        [(1, 2, 0), (2, 0, 1)]

    If *r* is given, only the *r*-length derangements are yielded.

        >>> sorted(derangements(range(3), 2))
        [(1, 0), (1, 2), (2, 0)]
        >>> sorted(derangements([0, 2, 3], 2, by_index=False))
        [(2, 0), (2, 3), (3, 0), (3, 2)]

    Note that in case of duplicates in input, these are treated as separate
    entries with the same restriction in the derangements. For example:

        >>> for d in derangements(['Alice', 'Bob', 'Carol', 'Alice']):
        ...    print(', '.join(d))
        Bob, Alice, Alice, Carol
        Bob, Alice, Alice, Carol
        Carol, Alice, Alice, Bob
        Carol, Alice, Alice, Bob

    Here Alice is excluded from both original positions of Alice, and also
    the results are duplicated which is in line with how duplicates are
    handled by ``itertools.permutations``. If deduplicated derangements
    are needed, use ``distinct_derangements``.
    """
    pool = tuple(iterable)
    if by_index:
        pool_unique = tuple(unique_everseen(pool))
        pool_ind = tuple([pool_unique.index(x) for x in pool])
        indices = pool_ind
    else:
        pool_ind = pool
        indices = tuple(range(len(pool)))
    return compress(
        permutations(pool, r=r),
        map(
            all,
            map(
                map,
                repeat(operator.ne),
                repeat(indices),
                permutations(pool_ind, r=r),
            ),
        ),
    )


class DerangementsRangeTests(TestCase):

    RANGE_NUM = 8

    def test_range_manual(self):
        actual = sorted(derangements_range(4))
        expected = [
            (1, 0, 3, 2),
            (1, 2, 3, 0),
            (1, 3, 0, 2),
            (2, 0, 3, 1),
            (2, 3, 0, 1),
            (2, 3, 1, 0),
            (3, 0, 1, 2),
            (3, 2, 0, 1),
            (3, 2, 1, 0),
        ]
        self.assertListEqual(actual, expected)

    def test_range(self):
        range_in = range(self.RANGE_NUM)
        actual = set(derangements_range(self.RANGE_NUM))
        expected = set(
            [
                x
                for x in permutations(range_in)
                if not any(x[i] == i for i in range_in)
            ]
        )
        self.assertSetEqual(actual, expected)

    def test_ref_impl(self):
        actual = set(derangements_range(self.RANGE_NUM))
        expected = set(derangements(range(self.RANGE_NUM)))
        self.assertSetEqual(actual, expected)



def derangements(iterable, r=None, restrict: [list | tuple | dict | None ] = None):
    """Yield successive derangements of the elements in *iterable*.

            >>> sorted(derangements([0, 1, 2]))
            [(1, 2, 0), (2, 0, 1)]

    Equivalent to yielding from ``permutations(iterable)``, except all
    permutations removed that have at least one integer k assigned at index k.

    If *r* is given, only the *r*-length derangements are yielded.

        >>> sorted(derangements(range(3), 2))
        [(1, 0), (1, 2), (2, 0)]
        >>> sorted(derangements([0, 2, 3], 2))
        [(2, 0), (2, 3), (3, 0), (3, 2)]

    *iterable* doesn't strictly need to consist of integers, but for
    non-integer iterables ``permutations`` will be equivalent but faster:

        >>> set(derangements(["a", 2.5, 1j])) == \
                set(permutations(["a", 2.5, 1j]))
        True

    There can be a use case in mixed iterables though:

        >>> list(derangements([0, 1, "green"]))
        [(1, 0, 'green'), (1, 'green', 0), ('green', 0, 1)]

    Note that in case of duplicates in input, these are treated as separate
    entries with the same restriction in the derangements. For example:

        >>> sorted(derangements([0, 0, 1]))
        [(1, 0, 0), (1, 0, 0)]

    If deduplicated derangements are needed, use``distinct_derangements``.

    """
    if restrict is None:
        restrict = list(range(len(iterable)))

    if type(restrict) in (list, tuple):
        for p in permutations(iterable, r=r):
            if any(x == p[i] for i, x in enumerate(restrict) if ((i < r) if r is not None else True)):
                continue
            yield p
    else:  # dict
        for p in permutations(iterable, r=r):
            if any(k == p[v] for k, vs in restrict.items() for v in vs if ((v < r) if r is not None else True)):
                continue
            yield p


def random_derangement_full(int_iterable, r=None, k=1):
    n = len(int_iterable)
    if r is None:
        r = n
    count = 0
    while count < k:
        v = list(int_iterable)
        for j in range(n - 1, -1, -1):
            p = random.randint(0, j)
            if v[p] == j:
                break
            else:
                v[j], v[p] = v[p], v[j]
        else:
            if v[0] != 0:
                yield tuple(v[:r])
                count += 1

def random_derangement_int(n, r=None, k=1, early=True):
    """Return *k* random *r* length permutation of the elements in range(*n*).

        For more details, see ``random_derangement``.
        """
    return random_derangement(range(n), r=r, k=k, early=True)


def random_derangement(int_iterable, r=None, k=1, early=True):
    """Return *k* random *r* length permutation of the elements in *iterable*.

        If *r* is not specified or is ``None``, then *r* defaults to the length of
        *int_iterable*. It is also reduced to the length of *int_iterable* if the
        specified value is too big.
        If *k* is not specified, then *k* defaults to 1.

            >>> random_derangement(range(5), k=2)  # doctest:+SKIP
            [(2, 3, 0, 4, 1), (4, 3, 1, 0, 2)]

            >>> random_derangement(range(5), 3, k=3)  # doctest:+SKIP
            [(2, 4, 1), (1, 3, 4), (3, 4, 1)]

        For *r*=None, this is equivalent to taking a random selection from
        ``derangements(int_iterable)``, *k* times. In case of
        *r* < len(*int_iterable*), *early* toggles exit behavior: either
        yield early when *r* elements have succesfully been generated, or
        continue to get all len(*int_iterable*) and then trim to first
        *r* elements. This can impact the probability of each option:

        >>> Counter(random_derangement([0, 0, 1, 2], r=2, k=10000, early=False))  # doctest:+SKIP
        Counter({(2, 0): 4924, (1, 0): 2542, (1, 2): 2534})
        >>> Counter(random_derangement([0, 0, 1, 2], r=2, k=10000, early=True))  # doctest:+SKIP
        Counter({(2, 0): 4030, (1, 0): 3960, (1, 2): 2010})

        """
    n = len(int_iterable)
    if r is None or r > n:
        r = n
    n_success = 0
    while n_success < k:
        v = list(int_iterable)
        for j in range(r if early else n):
            p = random.randint(j, n - 1)
            if v[p] == j:
                break
            else:
                v[j], v[p] = v[p], v[j]
        else:
            if (v[r-1] != r - 1) if early else (v[n-1] != n-1):
                yield tuple(v[:r])
                n_success += 1


def derangement_unique(elements):
    list_unique = Counter(elements)
    length_list = len(elements)  # will become depth in the next function
    placeholder = [0]*length_list  # will contain the result
    return derangement_unique_helper(elements, list_unique, placeholder, length_list-1)

def derangement_unique_helper(elements, list_unique, result_list, depth):
    if depth < 0:   # arrived at a solution
        yield tuple(result_list)
    else:
        # consider all elements and how many times they should still occur
        for el, count in list_unique.items():
            # ... still required and not breaking the derangement requirement
            if count > 0 and el != elements[depth]:
                result_list[depth] = el  # assignment element
                list_unique[el] -= 1   # substract number needed
                # loop for all possible continuations
                for g in derangement_unique_helper(elements, list_unique, result_list, depth-1):
                    yield g
                list_unique[el] += 1


@functools.cache
def test2(iterable, n=None):

    if n is None:
        n = len(iterable)
    if n == 2:
        return tuple(derangements(iterable))
    lst = list()
    for j in range(n):
        # Try all elements as last element and solve for remainder
        # - If j == len(iterable) -> skip
        if iterable[j] == n-1:
            continue
        this = tuple(iterable[:j]) + tuple(iterable[j+1:])
        for y in test2(tuple(this), n-1):
            lst.append(tuple(y + (iterable[j],)))
    return lst


def test(k):
    for j in range(k-1):
        this = [x for x in range(k) if x != j]
        for y in derangements(this):
            yield y + (j,)


def distinct_permutations(iterable, r=None):
    """Yield successive distinct permutations of the elements in *iterable*.

        >>> sorted(distinct_permutations([1, 0, 1]))
        [(0, 1, 1), (1, 0, 1), (1, 1, 0)]

    Equivalent to yielding from ``set(permutations(iterable))``, except
    duplicates are not generated and thrown away. For larger input sequences
    this is much more efficient.

    Duplicate permutations arise when there are duplicated elements in the
    input iterable. The number of items returned is
    `n! / (x_1! * x_2! * ... * x_n!)`, where `n` is the total number of
    items input, and each `x_i` is the count of a distinct item in the input
    sequence.

    If *r* is given, only the *r*-length permutations are yielded.

        >>> sorted(distinct_permutations([1, 0, 1], r=2))
        [(0, 1), (1, 0), (1, 1)]
        >>> sorted(distinct_permutations(range(3), r=2))
        [(0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1)]

    *iterable* need not be sortable, but note that using equal (``x == y``)
    but non-identical (``id(x) != id(y)``) elements may produce surprising
    behavior. For example, ``1`` and ``True`` are equal but non-identical:

        >>> list(distinct_permutations([1, True, '3']))  # doctest: +SKIP
        [
            (1, True, '3'),
            (1, '3', True),
            ('3', 1, True)
        ]
        >>> list(distinct_permutations([1, 2, '3']))  # doctest: +SKIP
        [
            (1, 2, '3'),
            (1, '3', 2),
            (2, 1, '3'),
            (2, '3', 1),
            ('3', 1, 2),
            ('3', 2, 1)
        ]
    """

    # Algorithm: https://w.wiki/Qai
    def _full(A):
        while True:
            # Yield the permutation we have
            yield tuple(A)

            # Find the largest index i such that A[i] < A[i + 1]
            for i in range(size - 2, -1, -1):
                if A[i] < A[i + 1]:
                    break
            #  If no such index exists, this permutation is the last one
            else:
                return

            # Find the largest index j greater than j such that A[i] < A[j]
            for j in range(size - 1, i, -1):
                if A[i] < A[j]:
                    break

            # Swap the value of A[i] with that of A[j], then reverse the
            # sequence from A[i + 1] to form the new permutation
            A[i], A[j] = A[j], A[i]
            A[i + 1 :] = A[: i - size : -1]  # A[i + 1:][::-1]

    # Algorithm: modified from the above
    def _partial(A, r):
        # Split A into the first r items and the last r items
        head, tail = A[:r], A[r:]
        right_head_indexes = range(r - 1, -1, -1)
        left_tail_indexes = range(len(tail))

        while True:
            # Yield the permutation we have
            yield tuple(head)

            # Starting from the right, find the first index of the head with
            # value smaller than the maximum value of the tail - call it i.
            pivot = tail[-1]
            for i in right_head_indexes:
                if head[i] < pivot:
                    break
                pivot = head[i]
            else:
                return

            # Starting from the left, find the first value of the tail
            # with a value greater than head[i] and swap.
            for j in left_tail_indexes:
                if tail[j] > head[i]:
                    head[i], tail[j] = tail[j], head[i]
                    break
            # If we didn't find one, start from the right and find the first
            # index of the head with a value greater than head[i] and swap.
            else:
                for j in right_head_indexes:
                    if head[j] > head[i]:
                        head[i], head[j] = head[j], head[i]
                        break

            # Reverse head[i + 1:] and swap it with tail[:r - (i + 1)]
            tail += head[: i - r : -1]  # head[i + 1:][::-1]
            i += 1
            head[i:], tail[:] = tail[: r - i], tail[r - i :]

    items = list(iterable)

    try:
        items.sort()
        sortable = True
    except TypeError:
        sortable = False

        indices_dict = defaultdict(list)

        for item in items:
            indices_dict[items.index(item)].append(item)

        indices = [items.index(item) for item in items]
        indices.sort()

        equivalent_items = {k: cycle(v) for k, v in indices_dict.items()}

        def permuted_items(permuted_indices):
            return tuple(
                next(equivalent_items[index]) for index in permuted_indices
            )

    size = len(items)
    if r is None:
        r = size

    # functools.partial(_partial, ... )
    algorithm = _full if (r == size) else partial(_partial, r=r)

    if 0 < r <= size:
        if sortable:
            return algorithm(items)
        else:
            return (
                permuted_items(permuted_indices)
                for permuted_indices in algorithm(indices)
            )

    return iter(() if r else ((),))


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

    print(list(n_wise_alt(test, 3)))

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
