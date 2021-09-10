from abc import abstractmethod, ABC


class ObserverAbstract(ABC):

    @abstractmethod
    def observe(self, evaluator):
        pass