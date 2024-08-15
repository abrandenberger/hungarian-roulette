from math import comb
from fractions import Fraction
import matplotlib.pyplot as plt
import json 

MAX_VAL = 320
PRINT = True
PRINT_FRACS = False # if True, print the fractions, else print the floats 
# if n is larger than 50 or so the fractions will be too large to print
EXISTING = 250

X_nk_path = 'results_X_nk_250.json'
probs_path = 'probs_250.json'
probs_float_path = 'probs_float_250.json' 
new_X_nk_path = 'results_X_nk_250_320.json'
new_probs_path = 'probs_250_320.json'
new_probs_float_path = 'probs_float_250_320.json'

COMPUTE_XNK = True
COMPUTE_PROBS = True 
# if COMPUTE_PROBS True but COMPUTE_XNK is False, need MAX_VAL to match the length of saved results

def save_results(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def convert_to_fractions_list_list(data):
    return [[Fraction(*tup) for tup in row] for row in data]

def convert_to_fractions_list(data):
    return [Fraction(*tup) for tup in data]

def load_results(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

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

def compute_X_nk (MIN_VAL=2, MAX_VAL=MAX_VAL):
    # # results_X_nk is a 2D array where results_X_nk[n][k] is of type Fraction
    # # P[X_n = k] is stored in results_X_nk[n][k]
    # results_X_nk = [[0],[0]] # an array of Fraction objects 
    # # make results[0] and results[1] dummy values to make indexing easier
    results = []
    if PRINT: print('******* Computing P[X_n = k] for n >= 2 *******')
    for n in range(MIN_VAL, MAX_VAL): 
        results_row_n = []
        if PRINT: print(f"** n = {n} **")
        for k in range(n-1): 
            result = one_round_prob(n, k)
            results_row_n.append(result)
            if PRINT and PRINT_FRACS: print(result, end=" ")
        if PRINT: print('')
        results.append(results_row_n)
    
    return results
    # print(results)

def compute_probability(MIN_VAL=2, MAX_VAL=MAX_VAL, old_probs=None, old_probs_float=None): 
    # now do the recursion for the probability of one man left standing
    # probs is a list of Fraction objects 
    if old_probs is None:
        probs = [0, 1]
    else: 
        probs = old_probs
    if old_probs_float is None:
        probs_float = [0, 1.0]
    else: 
        probs_float = old_probs_float
    if PRINT: 
        print('******* Computing probability of one man standing ******')
    for n in range(MIN_VAL, MAX_VAL):
        prob = 0
        for k in range(n-1):
            prob += results_X_nk[n][k] * probs[k]
        probs.append(prob)
        probs_float.append(float(prob))
        if PRINT_FRACS: print('n=', n, ':', probs[n], '==>', probs_float[n])
        else: print('n=', n, ':', probs_float[n])
    return probs, probs_float

if COMPUTE_XNK: # usually here
    if EXISTING <= 2: 
        # results_X_nk is a 2D array where results_X_nk[n][k] is of type Fraction
        # P[X_n = k] is stored in results_X_nk[n][k]
        old_results_X_nk = [[0],[0]] # an array of Fraction objects 
        # make results[0] and results[1] dummy values to make indexing easier
    else:
        old_results_X_nk = convert_to_fractions_list_list(load_results(X_nk_path))
    more_results_X_nk = compute_X_nk(len(old_results_X_nk), MAX_VAL)
    more_results_X_nk_tuples = [[frac.as_integer_ratio() for frac in row] for row in more_results_X_nk]
    save_results(new_X_nk_path, more_results_X_nk_tuples)
    results_X_nk = old_results_X_nk + more_results_X_nk
elif COMPUTE_PROBS: 
    old_results_X_nk = convert_to_fractions_list_list(load_results(X_nk_path))
    new_results_X_nk = convert_to_fractions_list_list(load_results(new_X_nk_path))
    results_X_nk = old_results_X_nk + new_results_X_nk

if COMPUTE_PROBS: # usually here
    old_probs = convert_to_fractions_list(load_results(probs_path))
    print('len(old_probs)', len(old_probs))
    old_probs_float = load_results(probs_float_path)
    probs, probs_float = compute_probability(len(old_probs), MAX_VAL, old_probs, old_probs_float)
    
    # save only the new ones
    new_probs = probs[EXISTING:]
    new_probs_float = probs_float[EXISTING:]
    new_probs_tuples = [frac.as_integer_ratio() for frac in new_probs]
    save_results(new_probs_path, new_probs_tuples)
    save_results(new_probs_float_path, new_probs_float)
else: 
    probs = convert_to_fractions_list(load_results(probs_path))
    probs_float = load_results(probs_float_path)

plt.figure()
plt.minorticks_on() # add a fine mesh grid 
plt.grid(which='both')
plt.axhline(y=0.5, color='r', linestyle='--') # add a y line at 0.5 
plt.plot(probs_float)
plt.show()