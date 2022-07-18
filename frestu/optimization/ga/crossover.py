import copy
import random

import numpy as np


def crossover_n_point(vec_1, vec_2, n_point):
    size = min(vec_1.shape[0], vec_2.shape[0])
    n_max = size - 1
    
    if n_max < n_point:
        raise ValueError(f'n_point should be {n_max} or less.')
    
    # 非復元抽出
    separating_positions = sorted(random.sample(range(1, size), k=n_point))
    separating_positions.insert(0, 0)
    separating_positions.append(size)

    booleans = [True, False]
    # vec_1 と vec_2 の順序の区別を無くす
    random.shuffle(booleans)
    
    exchanging_positions = np.full(size, booleans[0])
    exchanging_times = len(separating_positions) // 2

    for i in range(exchanging_times):
        ix = i * 2
        start = separating_positions[ix]
        stop = separating_positions[ix+1]
        exchanging_positions[start:stop] = booleans[1]
    
    # 要素が文字列の場合、以下では文字列が短くなり、エラーとなり得るので注意
    # vec = copy.copy(vec_1)
    # vec[exchanging_positions] = vec_2[exchanging_positions]
    # よって以下のようにした
    vec = np.full(size, None)
    vec[~exchanging_positions] = vec_1[~exchanging_positions]
    vec[exchanging_positions] = vec_2[exchanging_positions]
    
    return vec


def crossover_uniform(vec_1, vec_2):
    size = min(vec_1.shape[0], vec_2.shape[0])

    # 復元抽出
    exchanging_positions = np.array(random.choices([True, False], k=size))
 
    # 要素が文字列の場合、以下では文字列が短くなり、エラーとなり得るので注意
    # vec = copy.copy(vec_1)
    # vec[exchanging_positions] = vec_2[exchanging_positions]
    # よって以下のようにした
    vec = np.full(size, None)
    vec[~exchanging_positions] = vec_1[~exchanging_positions]
    vec[exchanging_positions] = vec_2[exchanging_positions]

    return vec


def crossover_partially_mapped():
    pass


def crossover_order():
    pass


def crossover_order_based():
    pass


def crossover_subtour_exchange():
    pass