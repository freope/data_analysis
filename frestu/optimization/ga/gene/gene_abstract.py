from abc import abstractmethod, ABC


class GeneAbstract(ABC):
    
    def __init__(self, dimension=1, mutate_probability=0.01):
        self.__dimension = dimension
        self.__mutate_probability = mutate_probability
    
    @property
    def dimension(self):
        return self.__dimension
    
    @property
    def mutate_probability(self):
        return self.__mutate_probability

    @mutate_probability.setter
    def mutate_probability(self, probability):
        if (probability < 0 or 1 < probability):
            raise ValueError('probability should be between 0 and 1')
        self.__mutate_probability = probability

    @abstractmethod
    def mutate(self):
        pass

    @abstractmethod
    def crossover(self):
        pass

    @abstractmethod
    def realize(self):
        pass