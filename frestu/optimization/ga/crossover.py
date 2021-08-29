import copy
import random

import numpy as np


def crossover_n_point(vec1, vec2, n_point):
    size = min(vec1.shape[0], vec2.shape[0])
    max_n = size - 1
    
    if max_n < n_point:
        raise ValueError(f'n_point should be {max_n} or less.')
    
    separating_positions = sorted(random.sample(range(1, size), k=n_point))
    separating_positions.insert(0, 0)
    separating_positions.append(size)
        
    booleans =[True, False]
    # vec1 と vec2 の順序の区別を無くす
    random.shuffle(booleans)
    
    exchanging_positions = np.full(size, booleans[0])
    exchanging_times = len(separating_positions) // 2

    for i in range(exchanging_times):
        ix = i * 2
        start = separating_positions[ix]
        stop = separating_positions[ix+1]
        exchanging_positions[start:stop] = booleans[1]
    
    vec = copy.copy(vec1)
    vec[exchanging_positions] = vec2[exchanging_positions]
    
    return vec


def crossover_uniform(vec1, vec2):
    size = min(vec1.shape[0], vec2.shape[0])
    exchanging_positions = np.array(random.choices([True, False], k=size))
    
    vec = copy.copy(vec1)
    vec[exchanging_positions] = vec2[exchanging_positions]
    
    return vec


def crossover_partially_mapped():
    pass


def crossover_order():
    pass


def crossover_order_based():
    pass


def crossover_subtour_exchange():
    pass