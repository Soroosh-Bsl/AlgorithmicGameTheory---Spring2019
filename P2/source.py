import numpy as np
from scipy.optimize import linprog
import sys
sys.setrecursionlimit(100000)


def main(table):
    n = len(table)
    m = len(table[0])
    for k in range(m):
        A_eq, A_ub = [], []
        B_eq, B_ub = [], []
        for z in range(n):
            a_ub = [-table[z][w][1] for w in range(m)] + [1]
            b_ub = -table[z][k][1]
            A_ub.append(a_ub)
            B_ub.append(b_ub)
        for w in range(m):
            a_ub = [0 if x != w else -1 for x in range(m + 1)]
            b_ub = 0
            A_ub.append(a_ub)
            B_ub.append(b_ub)
        A_ub.append([0 for x in range(m)] + [-1])
        B_ub.append(-0.001)
        A_eq.append([1 if x == k else 0 for x in range(m + 1)])
        B_eq.append(0)
        A_eq.append([1 for x in range(m)] + [0])
        B_eq.append(1)
        res = linprog(c=[0 for x in range(m)] + [-1], A_ub=A_ub, b_ub=B_ub, A_eq=A_eq, b_eq=B_eq)

        if res.success:
            return main(np.ndarray.tolist(np.delete(np.array(table), k, axis=1)))

    for j in range(n):
        A_eq, A_ub = [], []
        B_eq, B_ub = [], []
        for z in range(m):
            a_ub = [-table[w][z][0] for w in range(n)] + [1]
            b_ub = -table[j][z][0]
            A_ub.append(a_ub)
            B_ub.append(b_ub)
        for w in range(n):
            a_ub = [0 if x != w else -1 for x in range(n + 1)]
            b_ub = 0
            A_ub.append(a_ub)
            B_ub.append(b_ub)
        A_ub.append([0 for x in range(n)] + [-1])
        B_ub.append(-0.001)
        A_eq.append([1 if x == j else 0 for x in range(n + 1)])
        B_eq.append(0)
        A_eq.append([1 for x in range(n)] + [0])
        B_eq.append(1)
        res = linprog(c=[0 for x in range(n)] + [-1], A_ub=A_ub, b_ub=B_ub, A_eq=A_eq, b_eq=B_eq)

        if res.success:
            return main(np.ndarray.tolist(np.delete(np.array(table), j, axis=0)))

    return table
