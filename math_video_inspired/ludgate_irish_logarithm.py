# This video demonstrates how to do a multiplication by using only addition(*), using the Ludgate's Irish logarithm
# Summary: like how log(a*b) = log(a) + log(b), in this table you avoid multiplication by doing an addition after
# applying a "fake log-transformation", and then you revert the sum back by using a "fake exp-transformation".
# For background information (and inspiration), see the Standupmaths video https://www.youtube.com/watch?v=e1Kw3yJoNxw
# (*) Note: technically there is a "times 10" product in the code, but this is something straightforward and not in the
# same boat as calculating 98717234 x -91723498712 on top of your head.


# Initial table to transform your input digits ("log-transformation")
table1 = [50, 0, 1, 7, 2, 23, 8, 33, 3, 14]

# Secondary table to transform the sum back to find the multiplication result ("exp-transformation")
table2 = [ 1,  2,  4,  8, 16, 32, 64,  3,  6, 12,
          24, 48,  0,  0,  9, 18, 36, 72,  0,  0,
           0, 27, 54,  5, 10, 20, 40,  0, 81,  0,
          15, 30,  0,  7, 14, 28, 56, 45,  0,  0,
          21, 42,  0,  0,  0,  0, 25, 63,  0,  0,
           0,  0,  0,  0,  0,  0, 35,  0,  0,  0,
           0,  0,  0,  0,  0,  0, 49,  0,  0,  0,
           0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
           0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
           0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
           0]

debug=False


def product_(a: int, b: int) -> int:
    """Ludgate's Irish logarithm algorithm."""
    if debug:
        print(f"{a} x {b} = {table2[table1[a] + table1[b]]} because {table1[a]} + {table1[b]} = {table1[a] + table1[b]}")
    return table2[table1[a] + table1[b]]


def product(a: int, b: int) -> int:
    if a == 0 or b == 0:
        return 0
    elif a < 0 or b < 0:
        return -product(b, -a)
    elif a < 10 and b < 10:
        return product_(a, b)
    elif a >= 10:
        a1, a2 = divmod(a, 10)
        return product(a1, b) * 10 + product(a2, b)
    elif b >= 10:
        b1, b2 = divmod(b, 10)
        return product(a, b1) * 10 + product(a, b2)
    else:
        raise NotImplementedError(f"This option should not be reached for a={a} and b={b}")


if __name__ == "__main__":
    inputs = [[5, 7], [-11, 12], [232, 12312], [98717234, -91723498712]]
    for x, y in inputs:
        print(f'Applying the algorithm to find {x} x {y}: {product(x, y)}')
