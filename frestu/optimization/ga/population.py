import asyncio
import copy
import pickle


class Population:
    
    def __init__(self, individuals, select, n_eletes=1):
        self.individuals = individuals
        self.__select = select
        self.__n_eletes = n_eletes
        self.__pop_size = len(individuals)

    def alternate(self):
        """
        各個体の適応度に応じて、世代交代を行う。

        Notes
        -----
        事前に self.evaluate() を実行して、self.individuals 内の個体の
        適応度を算出し、適応度降順に並びかえておく必要がある。

        Examples
        --------
        >>> population.alternate()
        """
        # 次世代の個体群
        next_individuals = []

        # エリート保存戦略
        for i in range(self.__n_eletes):
            next_individuals.append(self.individuals[i])

        # 選択に用いる適応度
        fitnesses = [individual.fitness for individual in self.individuals]

        for i in range(self.__n_eletes, self.__pop_size):
            # 親を選択
            parent = self.individuals[self.__select(fitnesses)]
            partner = self.individuals[self.__select(fitnesses)]
            # 交叉
            child = parent.crossover(partner)
            next_individuals.append(child)

        # 世代交代
        self.individuals = next_individuals

    def mutate(self):
        # エリートにも突然変異が起き得る
        for individual in self.individuals:
            individual.mutate()

    def realize(self):
        for individual in self.individuals:
            individual.realize()
        return self
    
    def reshuffle(self, n_subordinates, async_evaluation=None):
        # self.individuals は事前にソートされている必要がある。
        subordinates = self.individuals[n_subordinates:]

        for subordinate in subordinates:
            subordinate.realize()

        if async_evaluation == 'task':
            self.__evaluate_with_async_tasks(subordinates)
        elif async_evaluation == 'coroutine':
            self.__evaluate_with_async_coroutines(subordinates)
        else:
            self.__evaluate(subordinates)

    def evaluate(self, async_evaluation=None):
        if async_evaluation == 'task':
            self.__evaluate_with_async_tasks(self.individuals)
        elif async_evaluation == 'coroutine':
            self.__evaluate_with_async_coroutines(self.individuals)
        else:
            self.__evaluate(self.individuals)
    
    def save(self, path):
        chromosomes = [individual.dump() for individual in self.individuals]
        with open(path, 'wb') as file:
            pickle.dump(chromosomes, file)

    def load(self, path):
        with open(path, 'rb') as file:
            chromosomes = pickle.load(file)
        for individual, chromosome in zip(self.individuals, chromosomes):
            individual.load(chromosome)

    def __evaluate(self, individuals):
        for individual in individuals:
            individual.evaluate()
        # 評価後に必ずソート
        self.__sort_individuals()

    def __evaluate_with_async_coroutines(self, individuals):
        loop = asyncio.get_event_loop()
        async def evaluate_async():
            async def _evaluate(ind):
                await loop.run_in_executor(None, ind.evaluate)
            coroutines = [_evaluate(ind) for ind in individuals]
            await asyncio.gather(*coroutines)
        loop.run_until_complete(evaluate_async())
        # 評価後に必ずソート
        self.__sort_individuals()

    def __evaluate_with_async_tasks(self, individuals):
        loop = asyncio.get_event_loop()
        async def evaluate_async():
            async def _evaluate(ind):
                await loop.run_in_executor(None, ind.evaluate)
            tasks = [asyncio.create_task(_evaluate(ind))
                     for ind in individuals]
            for task in tasks:
                await task
        loop.run_until_complete(evaluate_async())
        # 評価後に必ずソート
        self.__sort_individuals()

    def __sort_individuals(self):
        # 適応度が大きい順に並べ替え
        self.individuals.sort(key=lambda x: -x.fitness)

    @classmethod
    def create(cls, individual_prototype, select, pop_size, n_eletes=1):
        individuals = [
            copy.deepcopy(individual_prototype) for _ in range(pop_size)]
        return cls(individuals, select, n_eletes)