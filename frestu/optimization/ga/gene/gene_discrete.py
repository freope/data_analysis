import copy
import random

import numpy as np

from frestu.optimization.ga.gene.gene_abstract import GeneAbstract


class GeneDiscrete(GeneAbstract):

    def __init__(
            self, candidates, crossover, duplicate=True,
            dimension=1, mutate_probability=0.01):
        if not(duplicate) and len(candidates) < dimension:
            # 重複を許さず、候補数より次元数が多い場合は、エラー
            raise ValueError('dimension should be len(candidates) or less')
        super().__init__(dimension, mutate_probability)
        self.__candidates = candidates
        self.__crossover = crossover
        self.__duplicate = duplicate
        self.values = None

    @property
    def candidates(self):
        return self.__candidates
    
    def mutate(self):
        if self.__duplicate:
            # 重複を許す場合
            self.__mutate_duplicate()
            return self

        # 重複を許さない場合
        self.__mutate_not_duplicate()
        return self

    def __mutate_duplicate(self):
        mutated_position = np.random.uniform(
            low=0.0, high=1.0, size=self.dimension) < self.mutate_probability
        mutated_values = self.__choice()

        # 要素が文字列の場合、以下では文字列が短くなり、エラーとなり得るので注意
        # self.values[mutated_position] = mutated_values[mutated_position]
        # よって以下のようにした
        size = len(self.values)
        values = np.full(size, None)
        values[~mutated_position] = self.values[~mutated_position]
        values[mutated_position] = mutated_values[mutated_position]
        self.values = values
    
    def __mutate_not_duplicate(self):
        mutated_position = np.random.uniform(
            low=0.0, high=1.0, size=self.dimension) < self.mutate_probability

        # 要素が文字列の場合、以下では文字列が短くなり、エラーとなり得るので注意
        # self.values[mutated_position] = np.random.permutation(
        #     self.values[mutated_position])
        # よって以下のようにした
        size = len(self.values)
        values = np.full(size, None)
        values[~mutated_position] = self.values[~mutated_position]
        values[mutated_position] = np.random.permutation(
            self.values[mutated_position])
        self.values = values

    def crossover(self, gene_partner, **kwargs):
        child_values = self.__crossover(self.values, gene_partner.values)
        # 自身の values を上書きすると、ある世代交代内で同じ個体が親に選ばれた場合、
        # 既に crossover 後の values が使われてしまうので、コピーしている。
        gene_child = copy.copy(self)
        gene_child.values = child_values
        return gene_child

    def realize(self):
        self.values = self.__choice()
        return self
    
    def __choice(self):
        if self.__duplicate:
            # 重複を許す場合
            return self.__choice_duplicate()

        # 重複を許さないので、candidates のサイズが dimension より大きい必要がある。
        return self.__choice_not_duplicate()
    
    def __choice_duplicate(self):
        return np.array(random.choices(self.candidates, k=self.dimension))
    
    def __choice_not_duplicate(self):
        return np.array(random.sample(self.candidates, self.dimension))