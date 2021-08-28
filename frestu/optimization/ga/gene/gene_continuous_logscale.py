import copy

import numpy as np

from frestu.optimization.ga.gene.gene_abstract import GeneAbstract


class GeneContinuousLogscale(GeneAbstract):

    def __init__(
            self, minimum, maximum, random_realization=True,
            dimension=1, mutate_probability=0.01):
        super().__init__(dimension, mutate_probability)
        self.__minimum = minimum
        self.__maximum = maximum
        self.__random_realization = random_realization
        self.values = None
    
    @property
    def minimum(self):
        return self.__minimum

    @property
    def maximum(self):
        return self.__maximum

    def mutate(self):
        mutated_position = np.random.uniform(
            low=0.0, high=1.0, size=self.dimension) < self.mutate_probability
        mutated_values = self.__realize_random()

        # 突然変異が起きた成分を書き換え
        self.values[mutated_position] = mutated_values[mutated_position]
        return self

    def crossover(self, gene_partner, **kwargs):
        fitness_self = kwargs['fitness_self']
        fitness_partner = kwargs['fitness_partner']
        learning_rate = kwargs['learning_rate']

        amount_of_change = 10 ** (
            learning_rate
            * (np.log10(gene_partner.values) - np.log10(self.values))
            * np.sign(fitness_partner - fitness_self))

        # 自身の values を上書きすると、ある世代交代内で同じ個体が親に選ばれた場合、
        # 既に crossover 後の values が使われてしまうので、コピーしている。
        gene_child = copy.copy(self)
        gene_child.values = self.values + amount_of_change
        return gene_child

    def realize(self):
        if self.__random_realization:
            self.values = self.__realize_random()
            return self

        self.values = self.__realize_uniform()
        return self

    def __realize_random(self):
        return 10 ** np.random.uniform(
            low=np.log10(self.minimum), high=np.log10(self.maximum),
            size=self.dimension)
    
    def __realize_uniform(self):
        return np.logspace(
            start=np.log10(self.minimum), stop=np.log10(self.maximum),
            num=self.dimension)