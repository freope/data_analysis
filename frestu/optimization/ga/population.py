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

        # NOTE: 並列化で早くできる 
        for i in range(self.__n_eletes, self.__pop_size):
            # 親を選択
            parent = self.__select_parent()
            partner = self.__select_parent()
            # 交叉
            child = parent.crossover(partner)
            next_individuals.append(child)

        # 世代交代
        self.individuals = next_individuals

    def mutate(self):
        # NOTE: 並列化で早くできる 
        for individual in self.individuals:
            individual.mutate()

    def realize(self):
        # NOTE: 並列化で早くできる 
        for individual in self.individuals:
            individual.realize()
        return self

    def evaluate(self):
        # NOTE: 並列化で早くできる 
        for individual in self.individuals:
            individual.evaluate()
        # 適応度が大きい順に並べ替え
        self.individuals.sort(key=lambda x: -x.fitness)

    def show_result(self, show_result):
        show_result(self.individuals)        
    
    def save(self, path):
        chromosomes = [
            dict([
                (gene_name, gene.values)
                for gene_name, gene in individual.chromosome.items()])
            for individual in self.individuals]
        with open(path, 'wb') as file:
            pickle.dump(chromosomes, file)

    def load(self, path, individual_prototype):
        with open(path, 'rb') as file:
            chromosomes = pickle.load(file)
        individuals = []
        for chromosome in chromosomes:
            # deepcopy でなければならない
            individual = copy.deepcopy(individual_prototype)
            for gene_name, gene_value in chromosome.items():
                individual.chromosome[gene_name].values = gene_value
            individuals.append(individual)
        self.individuals = individuals

    def __select_parent(self):
        # self.individuals は事前にソートされている必要がある。
        fitnesses = [individual.fitness for individual in self.individuals]
        ix_selected = self.__select(fitnesses)
        return self.individuals[ix_selected]
    
    @classmethod
    def create(cls, individual_prototype, select, pop_size):
        # TODO: chromosome が使いまわされていないことを確認
        individuals = [
            copy.deepcopy(individual_prototype) for _ in range(pop_size)]
        return cls(individuals, select)