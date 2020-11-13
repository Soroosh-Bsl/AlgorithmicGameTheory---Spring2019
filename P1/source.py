from itertools import chain, combinations

from scipy.optimize import linprog
import numpy as np


def powerset(the_list):
    return list(map(list, chain.from_iterable(combinations(the_list, n) for n in range(len(the_list) + 1))))


def create_support_dependant_equalities(table, support_first, support_second, m, n):
    A_eq = []
    C_eq = []
    for i in range(len(support_first)):
        action = support_first[i]
        eq = [-1.0]
        eq += [0.0 for k in range(n + 1)]
        eq += [table[action][k][0] if k in support_second else 0.0 for k in range(m)]
        A_eq.append(eq)
        C_eq += [0]

    for i in range(len(support_second)):
        action = support_second[i]
        eq = [0.0]
        eq += [table[k][action][1] if k in support_first else 0.0 for k in range(n)]
        eq += [-1.0]
        eq += [0.0 for k in range(m)]
        A_eq.append(eq)
        C_eq += [0]

    for i in range(n):
        if i not in support_first:
            eq = [0.0 for k in range(m+n+2)]
            eq[i+1] = 1.0
            A_eq.append(eq)
            C_eq += [0]

    for i in range(m):
        if i not in support_second:
            eq = [0.0 for k in range(m + n + 2)]
            eq[i + n + 2] = 1.0
            A_eq.append(eq)
            C_eq += [0]

    return A_eq, C_eq


def create_support_dependant_inequalities(table, support_first, support_second, m, n):
    A_ub = []
    C_ub = []
    for i in range(n):
        if i not in support_first:
            action = i
            eq = [-1.0]
            eq += [0.0 for k in range(n+1)]
            eq += [table[action][k][0] if k in support_second else 0.0 for k in range(m)]
            A_ub.append(eq)
            C_ub += [0]

    for i in range(m):
        if i not in support_second:
            action = i
            eq = [0.0]
            eq += [table[k][action][1] if k in support_first else 0.0 for k in range(n)]
            eq += [-1.0]
            eq += [0.0 for k in range(m)]
            A_ub.append(eq)
            C_ub += [0]

    eq = [0.0 for k in range(m+n+2)]
    for i in range(n):
        if i in support_first:
            eq[i+1] = -1.0
    A_ub.append(eq)
    C_ub += [0]

    eq = [0.0 for k in range(m + n + 2)]
    for i in range(m):
        if i in support_second:
            eq[i + n + 2] = -1.0
    A_ub.append(eq)
    C_ub += [0]

    return A_ub, C_ub


def find_mixed_nash_equilibrium(table, all_nash_equilibriums):
    n = len(table)
    m = len(table[0])

    #x0 = v row player, x1 to xm = p row player, x(m+1) = v col player, x(m+2) to x(m+n+1) = p col player
    c = [-1.0 for i in range(m+n+2)]
    A_eq, C_eq = [], []

    eq = [0.0]
    eq += [1.0 for k in range(n)]
    eq += [0.0 for k in range(m+1)]
    A_eq.append(eq)
    C_eq += [1]

    eq = [0.0 for k in range(n + 2)]
    eq += [1.0 for k in range(m)]
    A_eq.append(eq)
    C_eq += [1]

    power_first = powerset(list(range(n)))
    power_second = powerset(list(range(m)))

    for i in range(1, len(power_first)):
        for j in range(1, len(power_second)):
            failed = False
            for k in range(len(all_nash_equilibriums)):
                if (all_nash_equilibriums[k][0]-1) in power_first[i] and (all_nash_equilibriums[k][1]-1) in power_second[j]:
                    failed = True
                    break
            if failed:
                continue
            support_first = power_first[i]
            support_second = power_second[j]
            finalA_eq, finalC_eq = create_support_dependant_equalities(table, support_first, support_second, m, n)
            finalA_eq += A_eq
            finalC_eq += C_eq
            A_ub, C_ub = create_support_dependant_inequalities(table, support_first, support_second, m, n)

            res = linprog(c=c, A_ub=np.array(A_ub), b_ub=C_ub, A_eq=finalA_eq, b_eq=finalC_eq)
            # print(res)
            if res.success:
                p1_strategy = list(res.x[1:n+1])
                p2_strategy = list(res.x[n+2:])
                return p1_strategy, p2_strategy


def find_nash_equilibrium(table):
    output = []

    best_cols = []
    for i in range(len(table)):
        best_response = float('-inf')
        best_col_for_this_row = [False for k in range(len(table[i]))]
        for j in range(len(table[i])):
            if table[i][j][1] > best_response:
                best_response = table[i][j][1]
        for j in range(len(table[i])):
            if table[i][j][1] >= best_response:
                best_col_for_this_row[j] = True
        best_cols.append(best_col_for_this_row)

    best_rows = []
    for j in range(len(table[0])):
        best_response = float('-inf')
        best_row_for_this_col = [False for k in range(len(table))]
        for i in range(len(table)):
            if table[i][j][0] > best_response:
                best_response = table[i][j][0]
        for i in range(len(table)):
            if table[i][j][0] >= best_response:
                best_row_for_this_col[i] = True
        best_rows.append(best_row_for_this_col)

    for i in range(len(table)):
        for j in range(len(table[0])):
            if best_cols[i][j] and best_rows[j][i]:
                output.append([i+1, j+1])
    return output


def main(table):
    all_nash_equilibriums = find_nash_equilibrium(table)
    p1_mixed_strategy , p2_mixed_strategy = find_mixed_nash_equilibrium(table, all_nash_equilibriums)
    print([all_nash_equilibriums, p1_mixed_strategy, p2_mixed_strategy])
    return [all_nash_equilibriums, p1_mixed_strategy, p2_mixed_strategy]


# main([[[3, 4], [7, 6], [1, 5]], [[2, 4], [1, 4], [2, 6]]])
# main([[[3, 1], [1, 2]],[[2, 3], [3, 4]],[[2, 4], [3, 1]]])

# main([[[3, 2], [2, 2], [3, 1]], [[2, 4], [3, 1], [1, 3]], [[3, 1], [3, 3], [2, 4]], [[4, 4], [3, 3], [3, 1]]])
# main([[[3, 1], [3, 3], [2, 3], [2, 1]], [[3, 4], [3, 1], [1, 4], [3, 2]], [[3, 1], [3, 2], [4, 2], [2, 4]]])
# main([[[3, 2], [4, 1]], [[4, 2], [3, 4]], [[3, 1], [4, 3]]])
#main([[[3, 2], [3, 4], [3, 2]], [[3, 3], [1, 2], [3, 4]], [[3, 3], [3, 4], [1, 1]]])
# main([[[1, 4], [4, 3], [3, 3], [4, 1]], [[4, 4], [1, 3], [3, 1], [2, 4]], [[4, 2], [4, 2], [4, 3], [3, 4]]])
# main([[[2, 1], [4, 2], [1, 2]], [[1, 1], [1, 4], [3, 4]], [[2, 3], [4, 3], [2, 3]], [[3, 4], [4, 3], [1, 1]]])
# main([[[4, 4], [2, 3], [3, 4], [4, 1]], [[1, 3], [3, 2], [4, 3], [3, 4]], [[4, 1], [2, 3], [1, 2], [3, 3]]])
# main([[[3, 4], [1, 4], [1, 2], [3, 3]], [[3, 2], [4, 2], [2, 4], [3, 3]]])
# main([[[2, 1], [3, 2], [1, 3]], [[2, 4], [2, 1], [4, 1]], [[1, 4], [3, 3], [1, 1]]])
# main([[[1, 2], [4, 3], [2, 3]], [[1, 4], [2, 3], [3, 3]], [[2, 1], [4, 1], [2, 2]]])
