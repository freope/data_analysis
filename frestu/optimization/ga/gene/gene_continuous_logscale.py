import copy

import numpy as np

from frestu.optimization.ga.gene import GeneContinuous


class GeneContinuousLogscale(GeneContinuous):

    def __init__(
            self, minimum, maximum, random_realization=True,
            dimension=1, mutate_probability=0.01):
        super().__init__(
            minimum, maximum, random_realization, dimension, mutate_probability)
    
    def crossover(self, gene_partner, **kwargs):
        fitness_self = kwargs['fitness_self']
        fitness_partner = kwargs['fitness_partner']
        learning_rate = kwargs['learning_rate']

        amount_of_change = learning_rate \
            * (np.log10(gene_partner.values) - np.log10(self.values)) \
            * np.sign(fitness_partner - fitness_self)
        child_values = 10 ** (np.log10(self.values) + amount_of_change)

        # 最小値以上最大以下に制限する
        child_values[child_values < self.minimum] = self.minimum
        child_values[self.maximum < child_values] = self.maximum

        # 自身の values を上書きすると、ある世代交代内で同じ個体が親に選ばれた場合、
        # 既に crossover 後の values が使われてしまうので、コピーしている。
        gene_child = copy.copy(self)
        gene_child.values = child_values
        return gene_child

    def _realize_random(self):
        return 10 ** np.random.uniform(
            low=np.log10(self.minimum), high=np.log10(self.maximum),
            size=self.dimension)
    
    def _realize_sequential(self):
        return np.logspace(
            start=np.log10(self.minimum), stop=np.log10(self.maximum),
            num=self.dimension)