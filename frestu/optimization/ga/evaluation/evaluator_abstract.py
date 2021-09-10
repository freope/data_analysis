from abc import abstractmethod, ABC


class EvaluatorAbstract(ABC):
    
    def __init__(self):
        self.__observers = []
    
    def add_observer(self, observer):
        self.__observers.append(observer)

    def delete_observer(self, observer):
        self.__observers.remove(observer)

    def notify_observers(self):
        for observer in self.__observers:
            observer.observe(self)
    
    # @abstractmethod
    # def evaluate(self, chromsome):
    #     pass