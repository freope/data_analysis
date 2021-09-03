import random

import numpy as np


def select_roulette(sortable):
    """
    ルーレット選択を行う。

    Parameters
    ----------
    sortable : list of number
        数値が入った list や ndarray

    Returns
    -------
    ix_selected : int
        sortable で与えられたリストをソートした後の、選択された要素のインデックス

    Notes
    -----
    全て同じ値だったら計算できないという問題がある。
    また、最悪の個体は選択されない。

    Examples
    --------
    >>> lst = [-3, 7, 1, 0]
    >>> select_roulette(lst)
    """
    sortable = np.array(sortable)

    minimum = sortable.min()
    sortable_scaled = sortable - minimum
    sortable_scaled_sum = sortable_scaled.sum()
    if (sortable_scaled_sum == 0):
        raise ValueError('sortable_scaled_sum should not be zero.')
    sortable_scaled = sortable_scaled / sortable_scaled_sum
    
    sortable_scaled.sort()
    sortable_scaled = sortable_scaled[::-1]

    r = random.random()
    for ix_selected, val in enumerate(sortable_scaled):
        r -= val
        if r < 0:
            return ix_selected


def select_ranking(sortable):
    n = len(sortable)

    # range(n) だと最悪の個体も選ばれない。
    sortable_scaled = np.array(range(1, n+1))
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