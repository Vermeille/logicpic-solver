import os
import time
import sys
from configparser import ConfigParser

config = ConfigParser()
config.read(sys.argv[1])

rows_constraints = config.get('rows', 'data')
cols_constraints = config.get('cols', 'data')

rows_constraints = rows_constraints.strip().split('/')
rows_constraints = [([int(y) for y in x.strip().split(' ')])
                    for x in rows_constraints]
nb_rows = len(rows_constraints)

cols_constraints = cols_constraints.strip().split('/')
cols_constraints = [([int(y) for y in x.strip().split(' ')])
                    for x in cols_constraints]
nb_cols = len(cols_constraints)

grid = [[' ' for i in range(nb_cols)] for i in range(nb_rows)]


# Print the grid` g`
def print_grid(g):
    print('+', end='')
    print('-' * len(grid[0]), end='+\n')
    for r in grid:
        print('|', end='')
        for c in r:
            print(c, end='')
        print('|')
    print('+', end='')
    print('-' * len(grid[0]), end='+\n')


# Generate all possible combinations of length `length` with constraints
# `constraints`
def all_combinations(length, constraints):
    # Recursively enumerate all possible combinations.
    # `t`: current vector generated
    # `i`: current write position in the vector
    # `nb` constraints vector
    # `i_nb`: currently treated constraint
    def all_combinations_rec(t, i, nb, i_nb):
        if i == len(t):
            if i_nb == len(nb):
                return [t.copy()]
            return []
        elif i_nb == len(nb):
            t[i:] = ['.'] * (len(t) - i)
            return all_combinations_rec(t, len(t), nb, len(nb))
        else:
            occ = nb[i_nb]
            t[i] = '.'
            l = all_combinations_rec(t, i + 1, nb, i_nb)
            if len(t) >= i + occ + 1:
                t[i:i + occ] = ['#'] * occ
                t[i + occ] = '.'
                l += all_combinations_rec(t, i + occ + 1, nb, i_nb + 1)
            elif len(t) == i + occ:
                t[i:i + occ] = ['#'] * occ
                l += all_combinations_rec(t, i + occ, nb, i_nb + 1)
            return l

    vec = [' '] * length
    return all_combinations_rec(vec, 0, constraints, 0)


# return if the vector `v` fits without conflicts in the `i`th row of the grid
# `g`
def is_valid_row(g, v, i):
    for x in zip(v, g[i]):
        if x[1] == ' ':
            continue
        if x[0] != x[1]:
            return False
    return True


# Write the vector `v` on the `i`th row of `g`
def write_row(g, v, i):
    changed = []
    for j in range(len(v)):
        if v[j] == ' ':
            continue
        if g[i][j] != v[j]:
            g[i][j] = v[j]
            changed.append(('c', j))
    if len(changed) != 0:
        changed.append(('r', i))
    return changed


# return if the vector `v` fits without conflicts in the `i`th column of the
# grid `g`
def is_valid_col(g, v, i):
    for j, x in enumerate(v):
        if g[j][i] == ' ':
            continue
        if x != g[j][i]:
            return False
    return True


# Write the vector `v` on the `i`th column of `g`
def write_col(g, v, i):
    changed = []
    for j, x in enumerate(v):
        if x == ' ':
            continue
        if g[j][i] == ' ':
            g[j][i] = x
            changed.append(('r', j))
        elif g[j][i] != x:
            assert False
    if len(changed) != 0:
        changed.append(('c', i))
    return changed


# return a vector containing only the common elements of `v1` and `v2`, writing
# a blank otherwise
def union(v1, v2):
    for i in range(len(v1)):
        if v1[i] != v2[i]:
            v1[i] = ' '
    return v1


todo = ([('r', i) for i in range(nb_rows)] + [('c', i) for i in range(nb_cols)])

while todo:
    cur = todo[-1]
    os.system('clear')
    print_grid(grid)
    if cur[0] == 'r':
        res = all_combinations(nb_cols, rows_constraints[cur[1]])
        t = []
        for r in res:
            if is_valid_row(grid, r, cur[1]):
                if len(t) == 0:
                    t = r
                else:
                    t = union(t, r)
        if len(t) != 0:
            todo += write_row(grid, t, cur[1])

    elif cur[0] == 'c':
        res = all_combinations(nb_rows, cols_constraints[cur[1]])
        t = []
        for r in res:
            if is_valid_col(grid, r, cur[1]):
                if len(t) == 0:
                    t = r
                else:
                    t = union(t, r)
        if len(t) != 0:
            todo += write_col(grid, t, cur[1])

    todo.pop()
    time.sleep(0.05)

os.system('clear')
print_grid(grid)
