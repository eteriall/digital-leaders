"""Пояснение ко второму тесту. Сначала нужно завезти в тупик два вагона 4 и 1. После этого вывезти один вагон из
тупика на путь отправления. После чего завезти весь оставшийся поезд в тупик и вывезти весь состав из тупика на путь
отправления.
"""

n = int(input())
r = list(map(int, input().split()))

if n < 3:
    print("YES")
else:
    right = r[:]
    left = []
    t = []
    err = 0

    t += [right.pop(0)]

    while right:
        if (len(t) > 0 and right[0] < t[-1]) or not t:
            t += [right.pop(0)]
        else:
            if not left:
                left += [t.pop(-1)]
            else:
                if left[-1] < t[-1]:
                    left += [t.pop(-1)]
                else:
                    print('NO')
                    err = 1
                    break
    if not err:
        while t:
            if not left:
                left += [t.pop(-1)]
            else:
                if left[-1] < t[-1]:
                    left += [t.pop(-1)]
                else:
                    print('NO')
                    err = 1
                    break
    if not err:
        if left == sorted(r):
            print('YES')
        else:
            print('NO')







