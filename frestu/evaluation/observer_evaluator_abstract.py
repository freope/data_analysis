from abc import abstractmethod, ABC


class ObserverEvaluatorAbstract(ABC):

    @abstractmethod
    def observe(self, evaluator):
        pass