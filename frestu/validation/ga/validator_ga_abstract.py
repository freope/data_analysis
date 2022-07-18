import json
import os

from frestu.optimization.ga import Population
from frestu.optimization.ga import Individual
from frestu.validation import ValidatorAbstract


class ValidatorGaAbstract(ValidatorAbstract):

    def __init__(
            self,
            chromosome_prototype,
            select,
            pop_size, n_eletes, gen_max, patience,
            async_evaluation='task',
            prefix_fitness='fitness_', prefix_chromosome='chromosome_'):
        super().__init__()
        self.__chromosome_prototype = chromosome_prototype
        self.__select = select
        self.__pop_size = pop_size
        self.__n_eletes = n_eletes
        self.__gen_max = gen_max
        self.__patience = patience
        self.__async_evaluation = async_evaluation
        self.__prefix_fitness = prefix_fitness
        self.__prefix_chromosome = prefix_chromosome
        self.population = None

    def __fname_chromosome(self, i_gen):
        return f'{self.__prefix_chromosome}{i_gen}.pkl'

    def __fname_fitness(self, i_gen):
        return f'{self.__prefix_fitness}{i_gen}.txt'

    def __fname_fitness_last(self, i_gen):
        return f'{self.__prefix_chromosome}{i_gen}_last.pkl'

    def _fname_fitness_pred(self):
        return f'{self.__prefix_fitness}pred.csv'

    def fit(self, evaluate, dpath):
        individual_prototype = Individual.create(
            self.__chromosome_prototype,
            evaluate)

        self.population = Population.create(
            individual_prototype,
            select=self.__select,
            pop_size=self.__pop_size,
            n_eletes=self.__n_eletes).realize()

        # 第 0 世代の計算
        best_gen = 0
        i_gen = 0

        self.population.evaluate(self.__async_evaluation)

        # 各個体の適応度を保存
        path = os.path.join(dpath, self.__fname_fitness(i_gen))
        with open(path, 'wt') as outfile:
            fitnesses = [ind.fitness for ind in self.population.individuals]
            outfile.write(json.dumps(fitnesses))

        # 各個体の染色体を保存
        best_fitness = self.population.individuals[0].fitness
        self.population.save(path=os.path.join(
            dpath, self.__fname_chromosome(i_gen)))

        # 第 1 世代以降を計算
        for i_gen in range(1, self.__gen_max):
            self.population.alternate()
            self.population.mutate()
            self.population.evaluate()
            self.population.reshuffle(
                self.__pop_size // 2, self.__async_evaluation)

            # 各個体の適応度を保存
            path = os.path.join(dpath, self.__fname_fitness(i_gen))
            with open(path, 'wt') as outfile:
                fitnesses = [ind.fitness for ind in self.population.individuals]
                outfile.write(json.dumps(fitnesses))

            # 最良個体の適応度が前世代に比べ上がった場合、各個体の染色体を保存
            best_generation_fitness = self.population.individuals[0].fitness
            if best_fitness < best_generation_fitness:
                best_fitness = best_generation_fitness
                best_gen = i_gen
                self.population.save(path=os.path.join(
                    dpath, self.__fname_chromosome(i_gen)))

            # 世代交代を繰り返しても、指定回数、最良個体の適応度が上がらなければ終了
            if self.__patience < i_gen - best_gen:
                self.population.save(path=os.path.join(
                    dpath, self.__fname_fitness_last(i_gen)))
                break