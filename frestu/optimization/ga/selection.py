import random

import numpy as np


def select_roulette(sortable):
    sortable = np.array(sortable)

    minimum = sortable.min()
    
    sortable_scaled = sortable - minimum
    sortable_scaled = sortable_scaled / sortable_scaled.sum()
    
    sortable_scaled.sort()
    sortable_scaled = sortable_scaled[::-1]

    r = random.random()
    for ix_selected, val in enumerate(sortable_scaled):
        r -= val
        if r < 0:
            return ix_selected


def select_ranking(sortable):
    n = len(sortable)
    
    sortable_scaled = np.array(range(n))
    sortable_scaled = sortable_scaled / sortable_scaled.sum()

    sortable_scaled.sort()
    sortable_scaled = sortable_scaled[::-1]

    r = random.random()
    for ix_selected, val in enumerate(sortable_scaled):
        r -= val
        if r < 0:
            return ix_selected


def select_tournament(lst):
    pass