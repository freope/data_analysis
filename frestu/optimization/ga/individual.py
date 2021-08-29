import copy


class Individual:
    
    def __init__(self, chromosome, evaluator, learning_rate=1.5):
        self.chromosome = chromosome
        self.evaluator = evaluator
        self.learning_rate = learning_rate
        self.__fitness = None

    @property
    def fitness(self):
        return self.__fitness    

    def crossover(self, parent_female, parent_male):
        for gene_name, gene_female in parent_female.chromosome.items():
            gene_male = parent_male.chromosome[gene_name]
            self.chromosome[gene_name] = gene_female.crossover(
                gene_male,
                fitness_self=parent_female.fitness,
                fitness_partner=parent_male.fitness,
                learning_rate=self.learning_rate)
    
    def mutate(self):
        for gene in chromosome.values():
            gene.mutate()

    def evaluate(self):
        self.__fitness = self.evaluator(self.chromosome)

    def save(self):
        pass
    
    @classmethod
    def create(cls, chromosome_prototype, evaluator, learning_rate=1.5):
        chromosome = copy.deepcopy(chromosome_prototype)
        # 各 gene の values に値を設定する
        for gene in chromosome.values():
            gene.realize()
        return cls(chromosome, evaluator, learning_rate)