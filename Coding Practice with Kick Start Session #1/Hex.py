# hein and John Nash. It has a similar idea, but does not assume you have played Hex. This game is played on an N×N
# board, where each cell is a hexagon. There are two players: Red side (using red stones) and Blue side (using blue
# stones). The board starts empty, and the two players take turns placing a stone of their color on a single cell
# within the overall playing board. Each player can place their stone on any cell not occupied by another stone of
# any color. There is no requirement that a stone must be placed beside another stone of the same color. The player
# to start first is determined randomly (with equal probability among the two players). The upper side and lower
# sides of the board are marked as red, and the other two sides are marked as blue. For each player, the goal of the
# game is to connect the two sides marked with their color by forming a connected path using stones of their color.
# The first player to achieve this wins. Note that the four corners are considered connected to both colors. The game
# ends immediately when one player wins. Given a game state, help someone new to the game determine the status of a
# game board. Say one of the following: Impossible: If it was impossible for two players to follow the rules and to
# have arrived at that game state. Red wins: If the player playing the red stones has won. Blue wins: If the player
# playing the blue stones has won. Nobody wins: If nobody has yet won the game. Note that a game of Hex cannot end
# without a winner! Note that in any impossible state, the only correct answer is Impossible, even if red or blue has
# formed a connected path of stones linking the opposing sides of the board marked by their colors. Here is a an
# example game on a 6×6 gameboard where blue won. Blue was the first player to move, and placed a blue stone at cell
# marked as 1. Then Red placed at cell 2, then blue at cell 3, etc. After the 11-th stone is placed, blue wins. Input
# The first line of input gives the number of test cases, T. T test cases follow. Each test case start with the size
# of the side of the board, N. This is followed by a board of N rows and N columns consisting of only B, R,
# and . characters. B indicates a cell occupied by blue stone, R indicates a cell occupied by red stone,
# and . indicates an empty cell. Output For each test case, output one line containing Case x: y, where x is the case
# number (starting from 1) and y is the status of the game board. It can be "Impossible", "Blue wins", "Red wins",
# or "Nobody wins" (excluding the quotes). Note that the judge is case-sensitive, so answers of "impossible",
# "blue wins", "red wins", and "nobody wins" will be judged incorrect. Limits Time limit: 30 seconds. Memory limit: 1
# GB. 1≤T≤100. Test Set 1 1≤N≤10. Test Set 2 1≤N≤100.
#
# Sample Input
# 7
# 1
# .
# 1
# B
# 1
# R
# 2
# BR
# BB
# 4
# BBBB
# BBB.
# RRR.
# RRRR
# 4
# BBBB
# BBBB
# RRR.
# RRRR
# 6
# ......
# ..R...
# BBBBBB
# ..R.R.
# ..RR..
# ......
# Sample Output
# Case #1: Nobody wins
# Case #2: Blue wins
# Case #3: Red wins
# Case #4: Impossible
# Case #5: Blue wins
# Case #6: Impossible
# Case #7: Blue wins

# Solution

INF = float("inf")


class Dinic:
    def __init__(self, n):  # vertexes from 0 to n-1 inclusive
        self.lvl = [0] * n
        self.ptr = [0] * n
        self.q = [0] * n
        self.adj = [[] for _ in range(n)]

    def add_edge(self, a, b, c, rcap=0):  # vertex a connects to vertex b with edge capacity c
        self.adj[a].append([b, len(self.adj[b]), c, 0])
        self.adj[b].append([a, len(self.adj[a]) - 1, rcap, 0])

    def dfs(self, v, t, f):
        if v == t or not f:
            return f
        for i in range(self.ptr[v], len(self.adj[v])):
            e = self.adj[v][i]
            if self.lvl[e[0]] == self.lvl[v] + 1:
                p = self.dfs(e[0], t, min(f, e[2] - e[3]))
                if p:
                    self.adj[v][i][3] += p
                    self.adj[e[0]][e[1]][3] -= p
                    return p
            self.ptr[v] += 1
        return 0

    def calc(self, s, t):  # return max flow from s to t
        flow, self.q[0] = 0, s
        for l in range(31):  # l = 30 maybe faster for random data
            while True:
                self.lvl, self.ptr = [0] * len(self.q), [0] * len(self.q)
                qi, qe, self.lvl[s] = 0, 1, 1
                while qi < qe and not self.lvl[t]:
                    v = self.q[qi]
                    qi += 1
                    for e in self.adj[v]:
                        if not self.lvl[e[0]] and (e[2] - e[3]) >> (30 - l):
                            self.q[qe] = e[0]
                            qe += 1
                            self.lvl[e[0]] = self.lvl[v] + 1

                p = self.dfs(s, t, INF)
                while p:
                    flow += p
                    p = self.dfs(s, t, INF)

                if not self.lvl[t]:
                    break
        return flow


def getMaxFlow(grid, n, player):
    sources = []
    sinks = []
    if player == 1:
        for j in range(1, n - 1):
            sources.append((0, j))
            sinks.append((n - 1, j))
    else:
        for i in range(1, n - 1):
            sources.append((i, 0))
            sinks.append((i, n - 1))

    dinic = Dinic((n ** 2 + 5) * 2)

    def nodeEntry(i, j):
        return i * n + j

    def nodeExit(i, j):
        return i * n + j + n * n

    src = 2 * n * n
    sink = 2 * n * n + 1
    # connect n ** 2 + 1 to sources
    for i, j in sources:
        dinic.add_edge(src, nodeEntry(i, j), 1)
    # connect sinks to n ** 2 + 2
    for i, j in sinks:
        dinic.add_edge(nodeExit(i, j), sink, 1)
    # create graph
    for i in range(n):
        for j in range(n):
            dinic.add_edge(nodeEntry(i, j), nodeExit(i, j), 1)
            # create 2 nodes within each hexagon and connect them with a capacity of 1
            # (so each hexagon may only allow 1 unit to flow through)
            if grid[i][j] == player:
                for ii, jj in ((i - 1, j), (i - 1, j + 1), (i, j - 1),
                               (i, j + 1), (i + 1, j - 1), (i + 1, j)):
                    if 0 <= ii < n and 0 <= jj < n and grid[ii][jj] == player:
                        dinic.add_edge(nodeExit(i, j), nodeEntry(ii, jj), 1)
    maxFlow = dinic.calc(src, sink)
    return maxFlow


def padBoard(grid, n):
    grid2 = [[0 for _ in range(n + 2)] for __ in range(n + 2)]
    for i in range(1, n + 1):
        grid2[i][0] = grid2[i][n + 1] = 2
    for j in range(1, n + 1):
        grid2[0][j] = grid2[n + 1][j] = 1
    for i in range(n):
        for j in range(n):
            grid2[i + 1][j + 1] = grid[i][j]
    return grid2


# denote 1 as red, 2 as blue

def main():
    t = int(input())
    for case in range(1, t + 1):
        n = int(input())
        grid = []
        r = b = 0
        for _ in range(n):
            row = []
            for c in input():
                if c == 'R':
                    row.append(1)
                    r += 1
                elif c == 'B':
                    row.append(2)
                    b += 1
                else:
                    row.append(-1)
            grid.append(row)
        if abs(r - b) > 1:
            print('Case #{}: Impossible'.format(case))
            continue
        grid2 = padBoard(grid, n)
        rmf = getMaxFlow(grid2, n + 2, 1)
        bmf = getMaxFlow(grid2, n + 2, 2)
        if rmf > 1 or bmf > 1 or (rmf > 0 and bmf > 0):
            ans = 'Impossible'
        elif rmf > 0:
            if r < b:
                ans = 'Impossible'
            else:
                ans = 'Red wins'
        elif bmf > 0:
            if b < r:
                ans = 'Impossible'
            else:
                ans = 'Blue wins'
        else:
            ans = 'Nobody wins'
        print('Case #{}: {}'.format(case, ans))

    return


import sys

# input=sys.stdin.buffer.readline #FOR READING PURE INTEGER INPUTS (space separation ok)
input = lambda: sys.stdin.readline().rstrip("\r\n")  # FOR READING STRING/TEXT INPUTS.


def oneLineArrayPrint(arr):
    print(' '.join([str(x) for x in arr]))


def multiLineArrayPrint(arr):
    print('\n'.join([str(x) for x in arr]))


def multiLineArrayOfArraysPrint(arr):
    print('\n'.join([' '.join([str(x) for x in y]) for y in arr]))


def readIntArr():
    return [int(x) for x in input().split()]


# def readFloatArr():
#     return [float(x) for x in input().split()]

def makeArr(defaultValFactory, dimensionArr):  # eg. makeArr(lambda:0,[n,m])
    dv = defaultValFactory;
    da = dimensionArr
    if len(da) == 1:
        return [dv() for _ in range(da[0])]
    else:
        return [makeArr(dv, da[1:]) for _ in range(da[0])]


def queryInteractive(a, b, c):
    print('? {} {} {}'.format(a, b, c))
    sys.stdout.flush()
    return int(input())


def answerInteractive(ansArr):
    print('! {}'.format(' '.join([str(x) for x in ansArr])))
    sys.stdout.flush()


inf = float('inf')

for _abc in range(1):
    main()
