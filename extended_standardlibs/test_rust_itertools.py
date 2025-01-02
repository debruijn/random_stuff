import time

N = 10

from rust_itertools import permutations as permutations_rs
from itertools import permutations as permutations_py

before = time.time()
print(len(permutations_rs(list(range(N)), N)))
before2 = time.time()
print(len(list(permutations_py(list(range(N)), N))))
after = time.time()
print("Rust:", before2 - before, ", Py: ", after - before2)

from rust_itertools import distinct_permutations as distinct_permutations_rs
from more_itertools import distinct_permutations as distinct_permutations_py

before = time.time()
print(len(distinct_permutations_rs(list(range(N)), N)))
before2 = time.time()
print(len(list(distinct_permutations_py(list(range(N)), N))))
after = time.time()
print("Rust:", before2 - before, ", Py: ", after - before2)


from rust_itertools import derangements as derangements_rs
from extended_itertools import derangements as derangements_py

before = time.time()
print(len(derangements_rs(list(range(N)), N)))
before2 = time.time()
print(len(list(derangements_py(list(range(N)), N))))
after = time.time()
print("Rust:", before2 - before, ", Py: ", after - before2)

from rust_itertools import combinations as combinations_rs
from itertools import combinations as combinations_py

before = time.time()
print(len(combinations_rs(list(range(N*2)), N)))
before2 = time.time()
print(len(list(combinations_py(list(range(N*2)), N))))
after = time.time()
print("Rust:", before2 - before, ", Py: ", after - before2)

from rust_itertools import pairwise as pairwise_rs
from itertools import pairwise as pairwise_py

x = list(x[0] for x in permutations_py(list(range(N)), N))

before = time.time()
print(len(pairwise_rs(x)))
before2 = time.time()
print(len(list(pairwise_py(x))))
after = time.time()
print("Rust:", before2 - before, ", Py: ", after - before2)

from rust_itertools import powerset as powerset_rs
from more_itertools import powerset as powerset_py

before = time.time()
print(len(powerset_rs(list(range(N*2)))))
before2 = time.time()
print(len(list(powerset_py(list(range(N*2))))))
after = time.time()
print("Rust:", before2 - before, ", Py: ", after - before2)

from rust_itertools import derangements_range as derangements_range_rs
from extended_itertools import derangements_range as derangements_range_py

before = time.time()
print(len(derangements_range_rs(N)))
before2 = time.time()
print(len(list(derangements_range_py(N))))
after = time.time()
print("Rust:", before2 - before, ", Py: ", after - before2)
