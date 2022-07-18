from abc import abstractmethod, ABC


class ExtractorFeatureAbstract(ABC):

    @abstractmethod
    def extract(self):
        pass