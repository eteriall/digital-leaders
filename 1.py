import random
from math import floor, ceil


def f(N, k):
    n = N
    girlfriend = 0
    boyfriend = 0

    while n > 0:
        n_new = max(0, n - k)
        boyfriend += n - n_new
        n = n_new
        g_temp = floor(n * 0.1)
        girlfriend += g_temp
        n -= g_temp
    check_val = 1 - girlfriend / N

    return boyfriend / N

n = int(input())

def bin_search_left(left, right):
    while left < right:
        mid = ceil(left + (right - left) / 2)
        if f(n, mid) < 0.5:
            left = mid + 1
        else:
            right = mid
        if right - 1 == left:
            return left
    return left


result = bin_search_left(1, min(n, 10 ** 19))
print(result, f(n, result), f(n, result -1))

