from abc import abstractmethod, ABC


class ObserverOptimizerAbstract(ABC):

    @abstractmethod
    def observe(self, optimizer):
        pass