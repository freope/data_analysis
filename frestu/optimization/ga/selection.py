import random

import numpy as np


def select_roulette(items):
    """
    ルーレット選択を行う。

    Parameters
    ----------
    items : list of number
        数値が入った list や ndarray

    Returns
    -------
    ix_selected : int
        items で与えられたリストをソートした後の、選択された要素のインデックス

    Notes
    -----
    全て同じ値だったら計算できないという問題がある。
    また、最悪の個体は選択されない。

    Examples
    --------
    >>> lst = [-3, 7, 1, 0]
    >>> select_roulette(lst)
    """
    items = np.array(items)

    minimum = items.min()
    items_scaled = items - minimum
    sum_items_scaled = items_scaled.sum()
    if (sum_items_scaled == 0):
        raise ValueError('sum_items_scaled should not be zero.')
    items_scaled = items_scaled / sum_items_scaled
    
    items_scaled.sort()
    items_scaled = items_scaled[::-1]

    r = random.random()
    for ix_selected, val in enumerate(items_scaled):
        r -= val
        if r < 0:
            return ix_selected


def select_ranking(items):
    n = len(items)

    # range(n) だと最悪の個体も選ばれない。
    items_scaled = np.array(range(1, n+1))
    items_scaled = items_scaled / items_scaled.sum()

    items_scaled.sort()
    items_scaled = items_scaled[::-1]

    r = random.random()
    for ix_selected, val in enumerate(items_scaled):
        r -= val
        if r < 0:
            return ix_selected


def select_tournament(lst):
    pass