# Use Python 3

from scipy.optimize import linprog

n = 2 # number of variables : x_1, x_2, ..., x_n
m = 3 # number of constraints
c = [3.0, 5.0] # coefficients of objective fucntion
A = [[1.0, 10.0], [2.0, 4.0], [12.0, 2.0]] # constraints coefficients matrix
b = [17, 18, 20] # right handside of inequalities

minus_c = [-x for x in c]

'''
linprog minimize an objective function c^T * x subject to A_ub * x <= b_ub
if we want to maximize your objective function (which is probably our case)
we have to minimize minus_c^T * x.
After solving minimization problem we can simply use same values to maximize
original objective function.
'''
res = linprog(c=minus_c, A_ub=A, b_ub=b)
print(res)
print('maximum = ', -res.fun)
print('x = ', res.x)
