#!/usr/bin/env python
# coding: utf-8


from datetime import datetime as dt
import os
import sys

import numpy as np

sys.path.append(os.path.abspath('..'))
from frestu.optimization.ga import Population
from frestu.optimization.ga import Individual
from frestu.optimization.ga.gene import GeneDiscrete
from frestu.optimization.ga.crossover import crossover_uniform
from frestu.optimization.ga.selection import select_ranking


## パラメータ設定
N = 50
SELECT = select_ranking
POP_SIZE = 1000
N_ELETES = 3
GEN_MAX = 100000
PATIENCE = 1000


## 遺伝子の設計
gene_selection = GeneDiscrete(
    candidates=[0, 1],
    crossover=crossover_uniform,
    dimension=N-1)

chromosome_prototype = {
    'selection': gene_selection,
}


# 遺伝子の翻訳関数
def translate_chromosome(chrom):
    gene = chrom['selection']
    
    params = {
        'selection': gene.values
    }
    
    return params


# 遺伝子の評価関数
def evaluate(chrom):
    params = translate_chromosome(chrom)

    sum_1 = 1 + np.sqrt(np.where(params['selection'] == 0)[0] + 2).sum()
    sum_2 = np.sqrt(np.where(params['selection'] == 1)[0] + 2).sum()
    
    fitness = -np.abs(sum_1 - sum_2)

    return fitness


# 個体の設計
individual_prototype = Individual.create(
    chromosome_prototype,
    evaluate)


# 集合の設計
population = Population.create(
    individual_prototype,
    select=SELECT,
    pop_size=POP_SIZE,
    n_eletes=N_ELETES).realize()


# 第 0 世代の計算
best_gen = 0
i_gen = 0

population.evaluate('_task')
best_fitness = population.individuals[0].fitness

print('TIME: {}'.format(dt.now().strftime('%Y/%m/%d %H:%M:%S')))
print(f'GENERATION: {i_gen}')
print(f'BEST_FITNESS: {best_fitness}')
print('----')


# 第 1 世代以降を計算
for i_gen in range(1, GEN_MAX):
    population.alternate()
    population.mutate()
    population.evaluate('_task')
    population.reshuffle(POP_SIZE//2, '_task')
    
    best_generation_fitness = population.individuals[0].fitness
    if best_fitness < best_generation_fitness:
        best_fitness = best_generation_fitness
        best_gen = i_gen
        print('TIME: {}'.format(dt.now().strftime('%Y/%m/%d %H:%M:%S')))
        print(f'GENERATION: {i_gen}')
        print(f'BEST_FITNESS: {best_fitness}')
        print('----')

    # 世代交代を繰り返しても、指定回数、最良個体の適応度が上がらなければ終了
    if PATIENCE < i_gen - best_gen:
        break
