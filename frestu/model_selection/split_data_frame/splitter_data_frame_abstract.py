from abc import abstractmethod, ABC


class SplitterDataFrameAbstract(ABC):

    @abstractmethod
    def split(self):
        pass