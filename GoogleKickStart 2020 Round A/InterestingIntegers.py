# Problem
# Let us call an integer interesting if the product of its digits is divisible by the sum of its digits. You are given two integers A and B.
# Find the number of interesting integers between A and B (both inclusive).
# Input
# The first line of the input gives the number of test cases, T. T lines follow.
# Each line represents a test case and contains two integers: A and B.
# Output
# For each test case, output one line containing Case #x: y, where x is the test case number (starting from 1) and y is the number of
# interesting integers between A and B (inclusive).
# Limits
# Time limit: 20 seconds.
# Memory limit: 1 GB.
# 1≤T≤100.
# Test Set 1
# 1≤A≤B≤105.
# Test Set 2
# 1≤A≤B≤1012.
# Sample
# Sample Input
# 4
# 1 9
# 91 99
# 451 460
# 501 1000
# Sample Output
# Case #1: 9
# Case #2: 0
# Case #3: 5
# Case #4: 176
# In Sample Case #1, since the product and the sum of digits are the same for single-digit integers, all integers between 1 and 9 are interesting.
# In Sample Case #2, there are no interesting integers between 91 and 99.
# In Sample Case #3, there are five interesting integers between 451 and 460:
# 451 (product of its digits is 4×5×1=20, sum of its digits is 4+5+1=10).
# 453 (product of its digits is 4×5×3=60, sum of its digits is 4+5+3=12).
# 456 (product of its digits is 4×5×6=120, sum of its digits is 4+5+6=15).
# 459 (product of its digits is 4×5×9=180, sum of its digits is 4+5+9=18).
# 460 (product of its digits is 4×6×0=0, sum of its digits is 4+6+0=10).

# Solution1

def sum_digits3(n):
    r = 0
    while n:
        r, n = r + n % 10, n // 10
    return r


def getProduct(n):
    product = 1

    while n != 0:
        product = product * (n % 10)
        n = n // 10

    return product


test_case = int(input())

for test in range(test_case):
    string = input()
    string = string.split()
    A = int(string[0])
    B = int(string[1])

    count = 0

    for num in range(A, B + 1):
        prod = getProduct(num)
        summ = sum_digits3(num)
        if prod % summ == 0:
            count += 1

    print("Case #" + str(test + 1) + ": " + str(count))


# Solution2

def ok(n):
    one = 1
    two = 0
    while n > 0:
        i = n % 10
        one *= i
        two += i
        n //= 10
    return one % two == 0


import heapq

# from math import ceil
# key gen
pq = [(1, 0)]
NMAX = 12  # 13
SMAX = 9 * NMAX + 9  # 120
PMAX = 9 ** NMAX * 9  # 9**12
keys = []
recent = 0
while pq:
    i, d = heapq.heappop(pq)
    cand = [(_ * i, d + 1) for _ in range(2, 9 + 1)]
    flag = True
    if recent != i:
        keys.append(i)
        if d < NMAX:
            for j in cand:
                if j[0] <= PMAX:
                    heapq.heappush(pq, j)
        recent = i

keys = [0] + keys
keyset = set(keys)

dp = [[{p: 0 for p in keys} for _ in range(SMAX)] for _ in range(NMAX)]
for s in range(1, SMAX):
    for p in keys:
        dp[0][s][p] = (1 if (p % s == 0) else 0)
for n in range(1, NMAX + 1):
    for s in range(1, 9 * (NMAX - n) + 1):
        for p in keys:
            if p > 9 ** (NMAX - n):
                break
            for i in range(9 + 1):
                if s + i >= SMAX:
                    break
                if p * i not in keyset:
                    continue
                dp[n][s][p] += dp[n - 1][s + i][p * i]

for case in range(1, int(input()) + 1):
    a, b = map(int, input().split())
    ans = 0
    while a <= b:
        mult = 10 ** 14
        while (a % mult != 0) or a + mult > b + 1:
            mult //= 10
        x, y = a, a + mult - 1
        # print(f'{x=} {y=}')
        n = len(str(x))
        m = n
        s = 0
        p = 1
        for i in range(m):
            if str(x)[i] == str(y)[i]:
                s += int(str(x)[i])
                p *= int(str(x)[i])
                n -= 1
        # print(f'{n=} {s=} {p=} {dp[n][s][p]=}')
        ans += dp[n][s][p]
        a = a + mult
    print(f'Case #{case}: {ans}')
