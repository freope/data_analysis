import copy


class Individual:
    
    def __init__(self, chromosome, evaluator, learning_rate=0.5):
        self.chromosome = chromosome
        self.evaluator = evaluator
        self.fitness = None
        self.learning_rate = learning_rate
        
    def crossover(self, parent_female, parent_male):
        for gene_name, gene_female in parent_female.chromosome.items():
            gene_male = parent_male.chromosome[gene_name]
            self.chromosome[gene_name] = gene_female.crossover(
                gene_male,
                fitness_self=self.parent_female.fitness,
                fitness_partner=self.parent_male.fitness,
                learning_rate=self.learning_rate)
    
    def mutate(self):
        for gene in chromosome.values():
            gene.mutate()

    def evaluate(self):
        self.fitness = self.evaluator(self.chromosome)

    def save(self):
        pass
    
    @classmethod
    def create(cls, chromosome_prototype, evaluator):
        chromosome = copy.deepcopy(chromosome_prototype)
        # 各 gene の values に値を設定する
        for gene in chromosome.values():
            gene.realize()
        return cls(chromosome, evaluator)