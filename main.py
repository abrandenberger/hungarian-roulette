from math import comb
from fractions import Fraction
import matplotlib.pyplot as plt

MAX_VAL = 100
PRINT = True
PRINT_FRACS = False # if True, print the fractions, else print the floats 
# if n is larger than 50 or so the fractions will be too large to print

def one_round_prob(n, k):
    # probability of k guys surviving the first round starting with n guys
    # n >= 2 and k >= 0
    total_sum = 0
    for l in range(k, n - 1):
        num = (-1) ** (l - k) * comb(l, k) * comb(n, l) * (n - l) ** l * (n - l - 1) ** (n - l)
        denom = (n - 1) ** n
        term = Fraction(num, denom)
        # print('l=', l, 'term=', term)
        total_sum += term
    return total_sum

# store in an array of Fraction objects 
results_X_nk = [[0],[0]] 
# make results[0] and results[1] dummy values to make indexing easier
# P[X_n = k] is stored in results[n][k]

if PRINT: print('******* Computing P[X_n = k] for n >= 2 *******')
for n in range(2, MAX_VAL): 
    results_row_n = []
    if PRINT: print(f"** n = {n} **")
    for k in range(n-1): 
        result = one_round_prob(n, k)
        results_row_n.append(result)
        if PRINT and PRINT_FRACS: print(result, end=" ")
    if PRINT: print('')
    results_X_nk.append(results_row_n)

# print(results)

# now do the recursion for the probability of one man left standing
probs = [0, 1]
probs_float = [0, 1.0]
if PRINT: 
    print('******* Computing probability of one man standing ******')
for n in range(2, MAX_VAL):
    prob = 0
    for k in range(n-1):
        prob += results_X_nk[n][k] * probs[k]
    probs.append(prob)
    probs_float.append(float(prob))
    if PRINT_FRACS: print('n=', n, ':', probs[n], '==>', probs_float[n])
    else: print('n=', n, ':', probs_float[n])

        
plt.figure()
plt.plot(probs_float)
plt.show()