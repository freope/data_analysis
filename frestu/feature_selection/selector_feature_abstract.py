from abc import abstractmethod, ABC


class SelectorFeatureAbstract(ABC):

    @abstractmethod
    def select(self):
        pass