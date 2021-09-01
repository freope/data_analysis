import copy


class Individual:
    
    def __init__(self, chromosome, evaluate, learning_rate=1.5):
        self.chromosome = chromosome
        self.__evaluate = evaluate
        self.learning_rate = learning_rate
        self.__fitness = None

    @property
    def fitness(self):
        return self.__fitness    

    def mutate(self):
        for gene in chromosome.values():
            gene.mutate()

    def crossover(self, partner):
        chromosome_child = dict([
            (gene_name, None) for gene_name in self.chromosome.keys()])

        for gene_name, gene in self.chromosome.items():
            gene_partner = partner.chromosome[gene_name]
            chromosome_child[gene_name] = gene.crossover(
                gene_partner,
                fitness_self=self.fitness,
                fitness_partner=partner.fitness,
                learning_rate=self.learning_rate)

        # 自身の chromosome を上書きすると、ある世代交代内で同じ個体が親に選ばれた
        # 場合、既に crossover 後の chromosome が使われてしまうので、コピーしている。
        child = copy.copy(self)
        child.chromosome = chromosome_child
        return child

    def realize(self):
        # 各 gene の values に値を設定する
        for gene in self.chromosome.values():
            gene.realize()
        return self

    def evaluate(self):
        self.__fitness = self.__evaluate(self.chromosome)
    
    @classmethod
    def create(cls, chromosome_prototype, evaluate, learning_rate=1.5):
        # copy でなく deepcopy でなければならないことに注意
        chromosome = copy.deepcopy(chromosome_prototype)
        return cls(chromosome, evaluate, learning_rate)