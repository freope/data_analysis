class Population:
    
    def __init__(self, individuals, select, n_eletes=1):
        self.individuals = individuals
        self.__select = select
        self.__n_eletes = n_eletes
        self.__pop_size = len(individuals)
    
    def alternate(self):
        """
        Notes
        -----
        事前に self.evaluate() を実行して、self.individuals 内の個体の
        適応度を算出し、適応度降順に並びかえておく必要がある。
        """
        # 次世代の個体群
        next_individuals = []

        # エリート保存戦略
        for i in range(self.__n_eletes):
            next_individuals.append(self.individuals[i])

        for i in range(self.__n_eletes, self.__pop_size):
            # 親を選択
            parent = self.__select_parent()
            partner = self.__select_parent()
            # 交叉
            child = parent.crossover(partner)
            next_individuals.append(child)

        # 世代交代
        self.individuals = next_individuals

    def can_alternate(self):
        pass

    def mutate(self):
        for individual in self.individuals:
            individual.mutate()

    def evaluate(self):
        # NOTE: 並列化で早くできる 
        for individual in self.individuals:
            individual.evaluate()
        self.__sort()

    def show_result(self, show_result):
        show_result(self.individual)        
    
    def save_generation(self, path):
        pass
    
    def load_generation(self, path):
        pass

    def __select_parent(self):
        # self.individuals は事前にソートされている必要がある。
        fitnesses = [individual.fitness for individual in self.individuals]
        ix_selected = self.__select(fitnesses)
        return self.individuals[ix_selected]
        
    def __sort(self):
        # 適応度が大きい順に並べ替え
        pass
    
    @classmethod
    def create(cls, individual_prototype, select, pop_size):
        # TODO: chromosome が使いまわされていないことを確認
        individuals = [
            copy.deepcopy(individual_prototype) for _ in range(pop_size)]
        return cls(individuals, select)